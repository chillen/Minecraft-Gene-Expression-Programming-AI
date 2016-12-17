# This file contains the info needed to parse a string of functions and
# terminals and convert it into a runnable malmo program. Currently,
# I'm doing it dumbly and using a second set of terminals than the one
# I have before (should be a keyset of this terminal list for the GEP)
# but it's a quick hackjob and I accept that.

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

# Launch the parsing 
def parse(p, agent, terms):
    sliced = p[1:]
    iflte(sliced[0],sliced[1],sliced[2],sliced[3],sliced,agent,terms)

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