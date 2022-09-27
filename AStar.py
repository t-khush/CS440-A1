import math 
import heapq

# just dumping everything from grid.py we can remove unused stuff later
def AStar(start, end, nodes, blocked_edges):
    path = []
    fringe = []    # [(fscore, (x,y))]
    start.gscore= 0.0
    heapq.heapify(fringe)
    cost = dict()
    parents = dict()

    # cost: node: float
    cost[(start.x, start.y)] = 0
    parents[(start.x, start.y)] = start
    heapq.heappush(fringe, (0, start))
    path_length = 0.0
    
    while len(fringe) != 0:
        s = heapq.heappop(fringe)
        curr_node = s[1]
        curr_node.hscore = hscore(curr_node, end)
        if curr_node.x == end.x and curr_node.y == end.y:
            # print("test1")
            path_length = curr_node.gscore
            # closed.add((start.x, start.y))
            start.closed = True
            for i in range(len(nodes)):
                for j in range(len(nodes[i])):
                    if (i, j) in cost: #(i, j) in cost
                        nodes[i][j].gscore = cost[(i,j)]
                    else: 
                        nodes[i][j].gscore = 0
                    nodes[i][j].fscore = nodes[i][j].gscore + nodes[i][j].hscore
            
            curr = curr_node
            parent = parents[(curr.x, curr.y)]
            while(curr.x != start.x or curr.y != start.y): 
                path.append(curr)
                curr = parent
                parent = parents[(parent.x, parent.y)]
            path.append(curr)
            # path.append(parent)
            # print("test2")
            # path.append(start)
            break

        # closed.add((curr_node.x, curr_node.y))
        curr_node.visited = True
        # if(curr_node is start): 
            # closed.add((curr_node.x, curr_node.y))
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if(i<0 or j < 0 or i >= len(nodes) or j>=len(nodes[0])): 
                    continue
                elif nodes[i][j].visited == True:
                    continue
                else: 
                    neighbour = nodes[i][j]
                    if ((curr_node.x, curr_node.y), (neighbour.x, neighbour.y)) not in blocked_edges:
                        if checkInFringe(neighbour, fringe) is False:
                            cost[(neighbour.x, neighbour.y)] = float('inf')
                            parents[(neighbour.x, neighbour.y)] = None
                        update_vertex(curr_node, cost, parents, neighbour, fringe)

    # reversing path to help user easily track the path from start to end
    path.reverse()
    print("AStar Start: {} {}  End: {} {}  Path Length: {}".format(start.x, start.y, end.x, end.y, path_length))
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