# This is the file that primarily needs to be updated
# Proper parsing and evolution *might* make this start 
# Properly producing results. Ideally, the 
# evolve and parse can be handled by PyGEP but running into
# Issues.

# Temporary fix to get things running at least as a proof of 
# concept - just hardcode strings and run them. It's capable
# of interpreting each symbol appropriately for sending actions
# it just needs to be properly parsed and each generation evolved
# Fitness is handled in the missionRunner for now, but hopefully
# that can be pulled into here as well.

num_clients = 1
num_agents = 2

terminals = {}
terminals["F"] = "move 1"
terminals["B"] = "move -1"
terminals["L"] = "turn -1"
terminals["R"] = "turn 1"
terminals["0"] = ""
terminals["A"] = "air"
terminals["L"] = "lava"
terminals["T"] = "stone"
terminals["S"] = "sandstone"

agent_program = [ "IKAIIKAFRKAFR", "IKAFR"  ]

# Write my own evolutions instead of PyGEP? Maybe just use theirs and format similarly?
def evolve(fitness_array):
    print ("Evolution not implemented.")

# Karva coding; not properly parsing. Having issues tapping into PyGEP. Primarily lit review for now?
# Requires updated terminals because orientation matters.
def parse(p, agent, terms):
    sliced = p[1:]
    iflte(sliced[0],sliced[1],sliced[2],sliced[3],sliced,agent,terms)

# Hey parsing is working decently well! That happened :D Now it's just the core GEP stuff. Mutations
def iflte(w,x,y,z,p,agent,terms):
    # Quickly simplify parsing by slicing appropriate columns
    # If y is an I, then it gets the next 4 params and z gets the next 4 after that
    y_slice = []
    z_slice = []
    if y == "I":
        y_slice = p[4:]
        z_slice = p[8:] # May not be used
    else:
        z_slice = p[4:]
    if terms[w] == terms[x]:
        if y == "I":
            iflte(y_slice[0],y_slice[1],y_slice[2],y_slice[3],y_slice,agent,terms)
        else: 
            agent.sendCommand(terms[y])
    else:
        if z == "I":
            iflte(z_slice[0],z_slice[1],z_slice[2],z_slice[3],z_slice,agent,terms)
        else: 
            agent.sendCommand(terms[z])