import math 

class AStar:
    def __init__(self, rows, cols, blockSize, start, end, nodes, blocked): 
        self.rows = rows
        self.cols = cols
        self.blockSize = blockSize
        self.nodes = nodes
        self.blocked = blocked
        self.start = start
        self.end = end

        
    def h(self, sx, sy): 
        sx_goal = self.end[0]
        sy_goal = self.end[1]
        return math.sqrt(2) * min(abs(sx - sx_goal), abs((sy - sy_goal))) + max(abs(sx - sx_goal), abs(sy - sy_goal)) - min(abs(sx-sx_goal), abs(sy - sy_goal))
