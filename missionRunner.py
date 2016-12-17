###################################
#  Beginnings of GEP implementation for Malmo
# 
# Currently, the program will run 50 agents on 2 scenarios. The fitness is the sum 
# of unobserved locations visited; death, stagnation, and collisions have yet to be 
# added. 
# 
# PyGEP is generating chromosomes and those chromosomes are fed into the parser in programming.py
# The PyGEP fitness is simply running a simulation and seeing what the fitness it reports is.
# 
# While the incremental maps are here and loaded in, it will only test against increment zero 
#
# The big thing holding me back is time to run; I can't really tell if my population improves over time.
###################################

import MalmoPython
import json
import logging
import math
import os
import random
import sys
import time
from sets import Set
from collections import defaultdict
import missions as m
import programming
from pygep import Chromosome
from pygep.chromosome import symbol
from pygep import *
from pygep.functions.linkers import sum_linker
import time

def run_programming(s):
  agent = s.agent
  program = s.genes[0]
  observations = ""
  
  sumFitness = 0
  # Only functioning for 0'th increment
  #for mission in missions[0]: uncomment this to do the first increment
  mission = missions[0][0]
  visited = Set([])
  agent.startMission( mission, client_pool, MalmoPython.MissionRecordSpec(), 0, 'Agent '+str(program))

  print "Waiting for the mission to start...",
  world_state = agent.peekWorldState()
  while not world_state.has_mission_begun:
      sys.stdout.write(".")
      time.sleep(0.1)
      world_state = agent.peekWorldState()
      for error in world_state.errors:
          print "Error:",error.text
  print

  prev = []
  max_stag = 10
  S = 0
  D = 0
  while agent.peekWorldState().is_mission_running:
    world_state = agent.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text                
        observations = json.loads(msg)     
        x = observations.get(u'XPos')  
        y = observations.get(u'YPos')   
        z = observations.get(u'ZPos') 
        if len(prev) < max_stag: prev.append(x + y + z)
        else: 
          if prev.count(x + y + z) == max_stag:
            S = 50
          if prev.count(x + y + z) < len(prev):
            prev = []
          if len(prev) > 0:
            prev.pop()
          prev.insert(0, x + y + z)
        visited.add(x + y + z)
        parse_program(program, agent, observations)
  sumFitness += len(visited)^2 - S - D
  if len(visited) == 1:
    sumFitness -= 100
  
  print "Calculated fitness... ", sumFitness
  time.sleep(0.5)
  return sumFitness

def parse_program(p, agent, observations):
      # Find the direction they are facing and setup our looking terminals
      ground = observations.get(u'ground', 0) 
      floor = observations.get(u'floor', 0) 
      ahead = observations.get(u'ahead', 0) 
      yaw   = observations.get(u'Yaw', 0)
      d = 0
      if yaw == 90:
        d = 3
      if yaw == 180:
        d = 1
      if yaw == -90 or yaw == 270:
        d = 5
      if yaw == 0:
        d = 7

      term = programming.terminals
      term["D"] = ground[d]
      term["K"] = ahead[d]
      term["U"] = floor[d] 

      programming.parse(p, agent, term)

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
start_time = time.time()
# -- set up the mission --

popsize = 50
num_clients = 1 # Multi-clienting currently disabled because weird things happening with timing
num_generations = 100
missions = []

# Looking is determined by the direction the agent is facing and setup in the procedure

for mission_increment in m.mission_files:
  increment = []
  for mission in mission_increment:
    with open(mission, 'r') as f:
        print "Loading mission from %s" % mission
        mission_xml = f.read()
        increment.append(MalmoPython.MissionSpec(mission_xml, True))
  missions.append(increment)

client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10002) )

iflte_op = symbol('I')(lambda w, x, y, z: y if w == x else z)

class Simulator(Chromosome):
  functions = (iflte_op,)
  terminals = 'F', 'B', 'L', 'R'
  agent = MalmoPython.AgentHost()

  def _fitness(self):
    return run_programming(self)

p = Population(Simulator, popsize, 6, 1, sum_linker)
print("--- Generated Population ---\n")
print p

for _ in xrange(num_generations):
  if p.best.solved:
    break
  print p
  print "BEST FOUND SO FAR: ", p.best
  print "BEST FOUND SO FITNESS: ", p.best.fitness
  p.cycle()

print("FINISHED SIMULATION\n\n")
print "BEST FOUND: ", p.best
print "FITNESS: ", p.best.fitness
print "RUNTIME: ", (time.time() - start_time), " seconds"