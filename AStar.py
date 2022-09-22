import math 
import heapq
from helper import Edge, Node
import pygame 

# just dumping everything from grid.py we can remove unused stuff later
def AStar(start, end, nodes, edges, blocked, screen):
    path = []
    fringe = []    # [(fscore, (x,y))]
    
    heapq.heapify(fringe)
    cost = dict()
    parents = dict()

    # cost: node: float
    cost[(start.x, start.y)] = 0
    parents[start] = start
    heapq.heappush(fringe, (0, start))
    while len(fringe) != 0:
        for (x, y) in fringe:
            print(str(y.x)+" " +str(y.y))
        
        s = heapq.heappop(fringe)
        curr_node = s[1]
        curr_node.hscore = hscore(curr_node, end)
        if curr_node.x == end.x and curr_node.y == end.y:
            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if (i, j) in cost: #(i, j) in cost
                        nodes[i][j].gscore = cost[(i,j)]
                    else: 
                        nodes[i][j].gscore = 0
                    nodes[i][j].fscore = nodes[i][j].gscore + nodes[i][j].hscore
            
            curr = curr_node
            parent = parents[curr]

            while(curr.x != start.x and curr.y != start.y): 
                path.append(curr)
                curr = parent
                parent = parents[parent]
            path.append(curr)
            path.append(parent)
            break
        curr_node.visited = True
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if(i<0 or j < 0 or i >= len(nodes) or j>=len(nodes[0])): 
                    continue
                elif nodes[i][j].visited is True:
                    continue
                else: 
                    neighbour = nodes[i][j]
                    if (neighbour.fscore, neighbour) not in fringe:
                        cost[(neighbour.x, neighbour.y)] = float('inf')
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
    if distance + curr_node.gscore < neighbour.gscore:
        neighbour.gscore = distance + curr_node.gscore
        cost[(neighbour.x, neighbour.y)] = neighbour.gscore
        parents[neighbour] = curr_node
        if (neighbour.fscore, neighbour) in fringe:
            fringe.remove((neighbour.fscore, neighbour))
        heapq.heappush(fringe, (neighbour.fscore, neighbour))

def drawPath(path, screen):
    for i in range(1, len(path) -1): 
        drawLine(screen, path[i-1], path[i])

def drawLine(screen, start, end): 
    pygame.draw.line(screen, (0, 0, 255), (start.x, start.y), (end.x, end.y))
