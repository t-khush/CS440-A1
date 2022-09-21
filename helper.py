class Node: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.hscore = float(0)
        self.gscore = float(0)
        self.fscore = float(0)
    
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

class Edge:
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.blocked = False
        