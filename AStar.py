import math 
import heapq

# no need for class- we need grid as a class along with node and maybe edge classes bc we will be passing a 'grid' class to both a* and theta*
class AStar():
    def __init__(self, rows, cols, blockSize, start, end, nodes, blocked): 
        self.rows = rows
        self.cols = cols
        self.blockSize = blockSize
        self.nodes = nodes
        self.blocked = blocked
        self.start = start
        self.end = end

        # We should also add start to the fringe. What should we be heapifying based off of though?
        # https://stackoverflow.com/questions/11989178/how-to-heapify-by-field-from-custom-objects

    # for now this is done inline
    # def hscore(node, end): 
    #     return math.sqrt(2) * min(abs(node[0] - end[0]), abs((node[1] - end[1]))) + max(abs(node[0] - end[0]), abs(node[1] - end[1])) - min(abs(node[0]-end[0]), abs(node[1] - end[1]))
        
    def aStar(start, end, nodes):
        closed = set()
        path = []
        # [(fscore, (x,y))]
        fringe = []
        
        heapq.heapify(fringe)
        cost = dict()
        parents = dict()

        cost[start] = 0
        parents[start] = start
        heapq.heappush(fringe, (0, start))

        while fringe:
            curr_node = heapq.heappop(fringe)[1]
            curr_node.hscore = math.sqrt(2) * min(abs(curr_node.x - end.x), abs((curr_node.y - end.y))) + max(abs(curr_node.x - end.x), abs(curr_node.y - end.y)) - min(abs(curr_node.x-end.x), abs(curr_node.y - end.y))
            
            if curr_node == end:
                for i in range(len(nodes)):
                    for j in range(len(nodes[i])):
                        if (i, j) in cost:
                            nodes[i][j].gscore = cost[(i,j)]
                        nodes[i][j].fscore = nodes[i][j].gscore + nodes[i][j].hscore
                
                while curr_node!=start:
                    curr_node = parents[curr_node]
                    path.append(curr_node)
                path.append(curr_node) # to append start point

                break
        
            nodes[curr_node.x][curr_node.y].visited = True
            for i in range(curr_node.x-1, curr_node.x+2):
                for j in range(curr_node.y-1, curr_node.y+2):
                    neighbour = nodes[i][j]
                    # neighbour is in grid, not the current node and unvisited
                    if ((i>=0 and j>=0) and (i<=len(nodes[0]) and j<=len(nodes)) and (i!=j) and (neighbour.visited == False)):
                        if neighbour not in fringe:
                            cost[neighbour] = float('inf')
                            parents[neighbour] = None

                        # update_vertex(curr_node, neighbour)
                        distance = math.dist((curr_node.x, curr_node.y), (neighbour.x, neighbour.y))
                        if distance + cost[curr_node] < cost[neighbour]:
                            parents[neighbour] = curr_node
                            if neighbour in fringe:
                                fringe.remove((neighbour.fscore, neighbour))
                            heapq.heappush(fringe, (neighbour.fscore, neighbour))
        # if path is empty list we can say no path found
        return path