import math
import heapq


class ThetaStar():

    def __init__(self,rows,columns,blockSize, start, end, nodes, blocked):
        self.rows=rows
        self.columns= columns
        self.blockSize=blockSize
        self.start=start
        self.end=end
        self.nodes= nodes
        self.blocked=nodes


    def UpdateVertex(currNode,nextNode):
        return


    def thetaStar(start,end,nodes):
        closed = set()
        opened= set()
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
        
            curr_node.visited = True
        for i in range(curr_node.x-1, curr_node.x+2):
            for j in range(curr_node.y-1, curr_node.y+2):
                # neighbour is in grid, not the current node and unvisited
                if ((i>=0 and j>=0) and (i<len(nodes[0]) and j<len(nodes)) and (i!=j)):
                    neighbour = nodes[i][j]
                    if neighbour not in fringe and neighbour.visited is False:
                        cost[neighbour] = float('inf')
                        parents[neighbour] = None

                        # update_vertex(curr_node, neighbour)
                        if LineOfSight(parents[curr_node],nextNode):
                            distance = math.dist((curr_node.x, curr_node.y), (neighbour.x, neighbour.y))
                            if (parents[curr_node]):

                                parents[neighbour]= parents[curr_node]
                                if neighbour in opened:   
                                              
                        else:
                            if distance + cost[curr_node] < cost[neighbour]:
                                parents[neighbour] = curr_node
                                if neighbour in fringe:
                                    fringe.remove((neighbour.fscore, neighbour))
                                heapq.heappush(fringe, (neighbour.fscore, neighbour))
        # if path is empty list we can say no path found
        return path

    #takes in parent(s) and s'
    def LineOfSight(parNode,nextNode):
        x= parNode.x
        y= parNode.y
        x1= nextNode.x
        y1= nextNode.y
        fScore=0
        distanceY= y1-y
        distanceX= x1-x
        if (distanceY < 0):
            distanceY= -(distanceY)
            parNode.y= -1
        else:
            parNode.x=1
        if distanceX<0:
            distanceX= -(distanceX)
            parNode.x=-1
        else:
            parNode.y= 1
        if distanceX>= distanceY:
            while x!=x1:
                f=f+distanceY
                if f>= distanceX:
                    #checks whether cell is blocked, returns true if blocked
                    #need different method to use grid pygame
                    if grid[x+((parNode.x-1)/2), y+ ((parNode.y-1)/2)]:
                        return False
                    y=y+parNode
                    f=f-distanceX
                if ((f!=0) and (grid[x+((parNode.x-1)/2), y+ ((parNode.y-1)/2)])):
                    return False
                if (distanceY ==0) and (grid[x+((parNode.x-1)/2), y]) and (grid[x+((parNode.x-1)/2), y-1]):
                    return False 
                x= x+parNode.x
        else:
            while y!=y1:
                f=f+distanceX
                if f>= distanceY:
                    if grid[x+((parNode.x-1)/2), y+ ((parNode.y-1)/2)]:
                        return False
                    x=x+parNode.x
                    f=f-distanceY
                if (f!=0) and grid[x+ ((parNode.x-1)/2), y+((parNode.y-1)/2)]:
                    return False
                if (distanceX==0) and (grid[x, y+((parNode.y-1)/2)]) and (grid[x-1,y+((parNode.y-1)/2)]):
                     return False
                y=y+parNode.y
        return True
                


    

    

    
