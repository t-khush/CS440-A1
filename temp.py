import math 
import heapq
from helper import Edge, Node
import pygame 

# just dumping everything from grid.py we can remove unused stuff later
def AStar(start, end, nodes, edges, blocked, screen):
    closed = set()
    path = []
    # [(fscore, (x,y))]
    fringe = []
    
    heapq.heapify(fringe)
    cost = dict()
    parents = dict()

    # cost: node: float
    cost[start] = 0
    parents[start] = start
    heapq.heappush(fringe, (0, start))
    while fringe:
        s = heapq.heappop(fringe)
        curr_node = s[1]
        curr_node.hscore = hscore(curr_node, end)
        
        if curr_node.x == end.x and curr_node.y == end.y:
            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if nodes[i][j] in cost: #(i, j) in cost
                        nodes[i][j].gscore = cost[nodes[i][j]]
                    nodes[i][j].fscore = nodes[i][j].gscore + nodes[i][j].hscore
            
            while curr_node.x == start.x and curr_node.y == start.y:
                curr_node = parents[curr_node]
                path.append(curr_node)
            path.append(curr_node) # to append start point

            break
    
        curr_node.visited = True
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if ((i>=0 and j>=0) and (i<len(nodes) and j<len(nodes[0])) and (i!=curr_node.x or j!=curr_node.y)):
                    neighbour = nodes[i][j]
                    if (neighbour.fscore, neighbour) not in fringe and neighbour.visited is False:
                        cost[neighbour] = float('inf')
                        parents[neighbour] = None

                    update_vertex(curr_node, cost, parents, neighbour, fringe)
                    
    # drawPath(path, screen) ==> Test to see if this works as expected
    # if path is empty list we can say no path found
    for n in path: 
        print(str(n.x) +" " + str(n.y))
    return path

def hscore(curr_node, end): 
    return math.sqrt(2) * min(abs(curr_node.x - end.x), abs((curr_node.y - end.y))) + max(abs(curr_node.x - end.x), abs(curr_node.y - end.y)) - min(abs(curr_node.x-end.x), abs(curr_node.y - end.y))

def update_vertex(curr_node, cost, parents, neighbour, fringe):
    distance = math.dist((curr_node.x, curr_node.y), (neighbour.x, neighbour.y))
    if distance + cost[curr_node] < cost[neighbour]:
        parents[neighbour] = curr_node
        if (neighbour.fscore, neighbour) in fringe:
            fringe.remove((neighbour.fscore, neighbour))
        heapq.heappush(fringe, (neighbour.fscore, neighbour))

def drawPath(path, screen):
    for i in range(1, len(path) -1): 
        drawLine(screen, path[i-1], path[i])

def drawLine(screen, start, end): 
    pygame.draw.line(screen, (0, 0, 255), (start.x, start.y), (end.x, end.y))
