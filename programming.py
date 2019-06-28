# This file contains the info needed to parse a string of functions and
# terminals and convert it into a runnable malmo program. Currently,
# I'm doing it dumbly and using a second set of terminals than the one
# I have before (should be a keyset of this terminal list for the GEP)
# but it's a quick hackjob and I accept that.

from sets import Set

action_map = {}
action_map["F"] = "move 1"
action_map["B"] = "move -1"
action_map["L"] = "turn -1"
action_map["R"] = "turn 1"
action_map["0"] = "turn 0"

block_map = {}
block_map["F"] = "sandstone"
block_map["B"] = "stone"
block_map["L"] = "lava"
block_map["R"] = "air"

view_map = {}

def parse(p, agent, term):
    view_map["F"] = term["F"]
    view_map["B"] = term["B"]
    view_map["L"] = term["L"]
    view_map["R"] = term["R"]
    iflte(p,agent)

def iflte(p,agent):
    w = p[0]
    x = p[1]
    y = p[2]
    z = p[3]
    # Check for lambdas, and resolve
    # If w is an if, just resolve it and return
    # IFBL.RRLBasdasd
    if type(w) != type("string"):
        iflte(p[4:], agent)
        return
    if type(x) != type("string"):
        iflte(p[4:], agent)
        return
    z_in = 4
    # Check if y is a lambda; if it is, z would start at 8, not 4
    if type(y) != type("string"):
        z_in = 8
    if w == "0" or x == "0" or view_map[w] == block_map[x]:
        if type(y) != type("string"):    
            iflte(p[4:], agent)
            return
        agent.sendCommand(action_map[y])
    else:
        if type(z) != type("string"):    
            iflte(p[z_in:], agent)
            return
        agent.sendCommand(action_map[z])