###################################
#  Beginnings of GEP implementation for Malmo
#  Can run parallel, but only occasionally (timing issues)
#  Removed PyGEP for now, which means there isn't proper karva
#  coding being parsed, just single line commands
#  Having a tough time getting PyGEP to work with robots, especially
#  with the lack of documentation
#  
# Anyways, requires joblib for parallel runs, but that's been commented
# out as distributed runs are very unstable right now. Requires Malmo
# to be installed according to the github repo. Requires a Malmo Minecraft
# client to be launched at one of the client_pool addresses/ports. 
# 
# Currently, the program will run the programs of n agents and calculate how many
# steps they took into unique positions. Death, stagnation, and collision are not
# yet factors. I removed all signs of PyGEP for now and was unsuccessful in getting
# my own parse tree up quickly to replace it, so it's currently just hardcoded programs
# with no evolution, so not doing anything interesting.
# 
# There is some parsing, but it's largely untested. It seems to work out for the most part.
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
#from joblib import Parallel, delayed

def run_programming(index):
  agent = agents[index]
  
  sumFitness = 0
  # Only functioning for 0'th increment
  for mission in missions[0]:
    visited = Set([])
    agent.startMission( mission, client_pool, MalmoPython.MissionRecordSpec(), 0, 'Agent ' + str(index) )

    print "Waiting for the mission to start",
    world_state = agent.peekWorldState()
    while not world_state.has_mission_begun:
        sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent.peekWorldState()
        for error in world_state.errors:
            print "Error:",error.text
    print

    # Run each mission according to index programmin
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
          visited.add(x + y + z)
          parse_program(programming.agent_program[index], agent, observations)
    sumFitness += len(visited)
    time.sleep(1)
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

# -- set up the mission --

num_agents = programming.num_agents
num_clients = programming.num_clients
num_generations = 3
missions = []
agents = []

# Looking is determined by the direction the agent is facing and setup in the procedure

for mission_increment in m.mission_files:
  increment = []
  for mission in mission_increment:
    with open(mission, 'r') as f:
        print "Loading mission from %s" % mission
        mission_xml = f.read()
        increment.append(MalmoPython.MissionSpec(mission_xml, True))
  missions.append(increment)

for i in range(num_agents):
  agents.append(MalmoPython.AgentHost())

client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10002) )

# This is the simple, one client after another run_programming
for i in range(num_generations):
  fitness = []
  for j in range(num_agents):
    fitness.append(run_programming(j))
  print "-----------------------"
  print "Gen " + str(i)
  print fitness
  print "-----------------------"
  programming.evolve(fitness)

# Uncomment for parallel + multiclient runs
# if __name__ == '__main__':
#   out = []
#   out = Parallel(num_clients)(delayed(run_programming)(i) for i in range(num_agents))
#   print out 
