import math 

def h(sx, sy, sx_goal, sy_goal): 
    return math.sqrt(2) * min(abs(sx - sx_goal), abs((sy - sy_goal))) + max(abs(sx - sx_goal), abs(sy - sy_goal)) - min(abs(sx-sx_goal), abs(sy - sy_goal))
    