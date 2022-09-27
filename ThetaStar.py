import math
import heapq



def ThetaStar(start, end, nodes, randomBlockedSet):
    path = []
    fringe = []
    start.gscore = 0.0
    heapq.heapify(fringe)
    cost = dict()
    parents = dict()
    cost[(start.x, start.y)] = 0
    parents[(start.x, start.y)] = start
    heapq.heappush(fringe, (0, start))

    while len(fringe) != 0: 
        s = heapq.heappop(fringe)
        curr_node = s[1]
        curr_node.hscore = hscore(curr_node, end)
        if curr_node.x == end.x and curr_node.y == end.y:
            print("reached") 
            start.closed = True
            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if (i,j) in cost: 
                        nodes[i][j].gscore = cost[(i,j)]
                    else: 
                        nodes[i][j].gscore = 0
                    nodes[i][j].fscore = nodes[i][j].gscore + nodes[i][j].hscore
            curr = curr_node
            parent = parents[(curr_node.x, curr_node.y)]
            while(curr.x != start.x or curr.y != start.y): 
                path.append(curr)
                curr = parent
                parent = parents[(parent.x, parent.y)]
            path.append(curr)
            path.append(parent)
            break
        
        curr_node.visited = True
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if(i<0 or j < 0 or i >= len(nodes) or j>=len(nodes[0])): 
                    continue
                elif nodes[i][j].visited == True:
                    continue
                else: 
                    neighbour = nodes[i][j]
                    if checkInFringe(neighbour, fringe) is False:
                        cost[(neighbour.x, neighbour.y)] = float('inf')
                        parents[(neighbour.x, neighbour.y)] = None
                    update_vertex(curr_node, cost, parents, neighbour, fringe, nodes) 
    # if path is empty list we can say no path found
    print("Theta Star Start: " + str(start.x)+" " + str(start.y) +" End: " + str(end.x) + " " +str(end.y)+" Path Length "  + str(len(path)))
    for n in path: 
        print(str(n.x) +" " + str(n.y))
    return path

def update_vertex(curr_node, cost, parents, neighbour, fringe, nodes): 
    distanceFromCurrent = math.dist((curr_node.x, curr_node.y), (neighbour.x, neighbour.y))
    distanceFromCurrentParent = math.dist((parents[(curr_node.x, curr_node.y)].x, parents[(curr_node.x, curr_node.y)].y), (neighbour.x, neighbour.y))
    if line_of_sight(parents[(curr_node.x, curr_node.y)], neighbour, nodes): 
        if cost[(parents[(curr_node.x, curr_node.y)].x, parents[(curr_node.x, curr_node.y)].y)] + distanceFromCurrentParent < cost[(neighbour.x, neighbour.y)]:
            neighbour.gscore = cost[(parents[(curr_node.x, curr_node.y)].x, parents[(curr_node.x, curr_node.y)].y)] + distanceFromCurrentParent
            cost[(neighbour.x, neighbour.y)] = neighbour.gscore
            parents[(neighbour.x, neighbour.y)] = parents[(curr_node.x, curr_node.y)]
            if checkInFringe(neighbour, fringe): 
                deleteFromFringe(neighbour, fringe)
            heapq.heappush(fringe, (neighbour.gscore + neighbour.hscore, neighbour))
        else: 
            if distanceFromCurrent + cost[(curr_node.x, curr_node.y)] < cost[(neighbour.x, neighbour.y)]:
                neighbour.gscore = distanceFromCurrent + cost[(curr_node.x, curr_node.y)]
                cost[(neighbour.x, neighbour.y)] = neighbour.gscore
                parents[(neighbour.x, neighbour.y)] = curr_node
                if checkInFringe(neighbour, fringe): 
                    deleteFromFringe(neighbour, fringe)
                heapq.heappush(fringe, (neighbour.gscore + neighbour.hscore, neighbour))

def line_of_sight(parent, neighbour, nodes):
    x0 = parent.x
    y0 = parent.y
    x1 = neighbour.x
    y1 = neighbour.y
    f = 0 
    dy = y1 - y0
    dx = x1 - x0

    if dy < 0: 
        dy = -1 * dy
        sy = -1 
    else : 
        sy = 1
    if dx < 0: 
        dx = -1 * dx 
        sx = -1
    else: 
        sx = 1
    if dx >= dy: 
        while x0 != x1: 
            f += dy
            if f >= dx: 
                if nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1 )//2)].blocked:
                    return False 
                y0 = y0 + sy 
                f = f - dx
            if f != 0 and nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                return False
            if dy == 0 and nodes[x0 + ((sx - 1)//2)][y0].blocked and nodes[x0 + ((sx - 1)//2)][y0 - 1].blocked:
                return False
            x0 += sx
    else: 
        while y0 != y1: 
            f = f + dx 
            if f >= dy:
                if nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1 )//2)].blocked:
                    return False
                x0 += sx
                f -= dy
            if f != 0 and nodes[x0 + ((sx - 1)//2)][y0 + ((sy - 1)//2)].blocked:
                return False
            if dx == 0 and nodes[x0][y0 + ((sy - 1)//2)].blocked and nodes[x0 - 1][y0 + ((sy - 1)//2)].blocked:
                return False
            y0 += sy
    return True
def hscore(curr_node, end): 
    return math.sqrt(2) * min(abs(curr_node.x - end.x), abs((curr_node.y - end.y))) + max(abs(curr_node.x - end.x), abs(curr_node.y - end.y)) - min(abs(curr_node.x-end.x), abs(curr_node.y - end.y))

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
