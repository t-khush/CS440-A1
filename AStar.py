import math 
import heapq

# just dumping everything from grid.py we can remove unused stuff later
def aStar(start, end, nodes, edges, blocked, screen):
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
        curr_node.hscore = hscore(curr_node, end)
        
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
    
        curr_node.visited = True
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if ((i>=0 and j>=0) and (i<len(nodes[0]) and j<len(nodes)) and (i!=j)):
                    neighbour = nodes[i][j]
                    if neighbour not in fringe and neighbour.visited is False:
                        cost[neighbour] = float('inf')
                        parents[neighbour] = None

                    update_vertex(curr_node, cost, parents, neighbour, fringe)
                    
    # if path is empty list we can say no path found
    return path

def hscore(curr_node, end): 
    return math.sqrt(2) * min(abs(curr_node.x - end.x), abs((curr_node.y - end.y))) + max(abs(curr_node.x - end.x), abs(curr_node.y - end.y)) - min(abs(curr_node.x-end.x), abs(curr_node.y - end.y))

def update_vertex(curr_node, cost, parents, neighbour, fringe):
    distance = math.dist((curr_node.x, curr_node.y), (neighbour.x, neighbour.y))
    if distance + cost[curr_node] < cost[neighbour]:
        parents[neighbour] = curr_node
        if neighbour in fringe:
            fringe.remove((neighbour.fscore, neighbour))
        heapq.heappush(fringe, (neighbour.fscore, neighbour))
