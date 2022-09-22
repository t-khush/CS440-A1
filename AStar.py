import math 
import heapq
from helper import Edge, Node
import pygame 

# just dumping everything from grid.py we can remove unused stuff later
def AStar(start, end, nodes, edges, blocked, screen):
    path = []
    closed = set()
    fringe = []    # [(fscore, (x,y))]
    start.gscore= 0.0
    heapq.heapify(fringe)
    cost = dict()
    parents = dict()

    # cost: node: float
    cost[(start.x, start.y)] = 0
    parents[(start.x, start.y)] = start
    heapq.heappush(fringe, (0, start))
    while len(fringe) != 0:
        # print(closed)
        s = heapq.heappop(fringe)
        curr_node = s[1]
        curr_node.hscore = hscore(curr_node, end)
        if curr_node.x == end.x and curr_node.y == end.y:
            # print("test1")
            closed.add((start.x, start.y))
            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if (i, j) in cost: #(i, j) in cost
                        nodes[i][j].gscore = cost[(i,j)]
                    else: 
                        nodes[i][j].gscore = 0
                    nodes[i][j].fscore = nodes[i][j].gscore + nodes[i][j].hscore
            
            curr = curr_node
            parent = parents[(curr.x, curr.y)]
            while(curr.x != start.x and curr.y != start.y): 
                path.append(curr)
                curr = parent
                parent = parents[(parent.x, parent.y)]
            path.append(curr)
            path.append(parent)
            # print("test2")
            # path.append(start)
            break

        closed.add((curr_node.x, curr_node.y))
        if(curr_node is start): 
            closed.add((curr_node.x, curr_node.y))
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if(i<0 or j < 0 or i >= len(nodes) or j>=len(nodes[0])): 
                    continue
                elif (nodes[i][j].x, nodes[i][j].y) in closed:
                    continue
                else: 
                    neighbour = nodes[i][j]
                    if checkInFringe(neighbour, fringe) is False:
                        cost[(neighbour.x, neighbour.y)] = float('inf')
                        parents[(neighbour.x, neighbour.y)] = None
                    update_vertex(curr_node, cost, parents, neighbour, fringe)
    drawPath(path, screen) 
    # if path is empty list we can say no path found
    print("Start: " + str(start.x)+" " + str(start.y) +" End: " + str(end.x) + " " +str(end.y)+" Path Length "  + str(len(path)))
    for n in path: 
        print(str(n.x) +" " + str(n.y))
    return path

def hscore(curr_node, end): 
    return math.sqrt(2) * min(abs(curr_node.x - end.x), abs((curr_node.y - end.y))) + max(abs(curr_node.x - end.x), abs(curr_node.y - end.y)) - min(abs(curr_node.x-end.x), abs(curr_node.y - end.y))

def update_vertex(curr_node, cost, parents, neighbour, fringe):
    distance = math.dist((curr_node.x, curr_node.y), (neighbour.x, neighbour.y))
    # print("curr node: ({},{}), neighbour: ({},{}), fscore: {}, distance: {}".format(curr_node.x, curr_node.y, neighbour.x, neighbour.y, neighbour.fscore, distance))
    if distance + cost[(curr_node.x, curr_node.y)] < cost[(neighbour.x, neighbour.y)]:
        neighbour.gscore = distance + cost[(curr_node.x, curr_node.y)]
        cost[(neighbour.x, neighbour.y)] = neighbour.gscore
        parents[(neighbour.x, neighbour.y)] = curr_node
        if checkInFringe(neighbour, fringe): 
            deleteFromFringe(neighbour, fringe)
            # heapq.heapify(fringe)
        heapq.heappush(fringe, (neighbour.gscore + neighbour.hscore, neighbour))

def drawPath(path, screen):
    for i in range(0, len(path)-1): 
        drawLine(screen, path[i], path[i+1])

def drawLine(screen, start, end): 
    pygame.draw.line(screen, (0, 0, 255), (start.y * 100, start.x * 100), (end.y * 100, end.x * 100),4)

def checkInFringe(neighbour, fringe): 
    for i in range(len(fringe)): 
        if(fringe[i][1].x == neighbour.x and fringe[i][1].y == neighbour.y): 
            return True
    return False 

def deleteFromFringe(neighbour, fringe): 
    for i in range(len(fringe)):
        if(fringe[i][1].x == neighbour.x and fringe[i][1].y == neighbour.y): 
            del fringe[i]
            return
    return