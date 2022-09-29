class Node: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.hscore = float(0)
        self.gscore = float(0)
        self.fscore = float(0)
        self.blocked = False 
    def __str__(self):
        return "("+str(self.x) + " " + str(self.y)+")"
    # We have this function for Node comparison in sets
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.fscore == other.fscore) 
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return (self.fscore < other.fscore)
    def __gt__(self, other):
        return (self.fscore > other.fscore)
    def __le__(self, other):
        return (self < other) or (self == other)
    def __ge__(self, other):
        return (self > other) or (self == other)
        