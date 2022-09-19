class Node: 
    h = -1
    g = -1
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.hscore = 0
        self.gscore = 0
        self.fscore = 0
    
    # We have this function for Node comparison in sets
    def __hash__(self):
        return hash((self.x, self.y))