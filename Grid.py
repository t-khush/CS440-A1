

import sys
import pygame
import random
from AStar import AStar
from ThetaStar import ThetaStar
from helper import Node

BLACK = (0, 0, 0)
GREEN= (0,255,0)
RED= (255,0,0)
WHITE = (255, 255, 255)
PURPLE= (62.7,12.5,94.1)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 500
ROWS = 1000 #1000 
COLS = 500 #500 
BLOCKSIZE = 10 # 10
Textfile= False

#for text files only
startVertex=(0,0)
endVertex=(0,0)
blockedCells=dict()

#for which path is needed
#for now its for text file
wantA= False
wantT= False



if len(sys.argv)>1:
    file1= sys.argv[1]
    pathSetting= sys.argv[2]
    Textfile= True
    with open(file1, 'r') as f:
        #since we have orgin at (0,0), we have to move
        #the values by one
        line = f.readline().strip().split()
        startVertex = (int(line[0])-1 , int(line[1]) -1) 

        line = f.readline().strip().split()
        endVertex = (int(line[0])-1 , int(line[1])-1 )

        line = f.readline().strip().split()
        COLS = int(line[0])*100
        ROWS = int(line[1])*100
       

        #Getting the blocked cells
        for line in f.readlines():
            split = line.strip().split()
            if (int(split[2])==1):
                blockedCells[(int(split[1]) -1, int(split[0])-1 )] = int(split[2])
           
    if (pathSetting== "astar"):
        wantA= True
    if (pathSetting== "thetastar"):
        wantT= True

def main():

    # for x in range(0, int(ROWS/BLOCKSIZE)):
    #     for y in range(0, int(COLS/BLOCKSIZE)):
    #         print("x: {}, y: {}".format(x,y))
    nodes = genNodes()
    global SCREEN

    #if file was detected
    if Textfile:

        tStart= nodes[startVertex[1]][startVertex[0]]
        tEnd= nodes[endVertex[1]][endVertex[0]]
        tBlockedSet= setBlocked(blockedCells)


        blocked_edges = genEdges(tBlockedSet)


        pygame.init()
        SCREEN= pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        SCREEN.fill(WHITE)
        drawGrid(tBlockedSet, tStart, tEnd)
        nodesDict = dict()
        if wantA:
            Apath = AStar(tStart, tEnd, nodes, blocked_edges)[0]
            nodesDict = AStar(tStart, tEnd, nodes, blocked_edges)[1]

        # Configure blocked vertices for ThetaStar
        if wantT:
            for coordinate in tBlockedSet: 
                nodes[coordinate[0]][coordinate[1]].blocked = True

            Tpath = ThetaStar(tStart, tEnd, nodes, blocked_edges)[0]
            nodesDict = ThetaStar(tStart, tEnd, nodes, blocked_edges)[1]

        run1= True

        while run1:
            for event in pygame.event.get():
                if event.type== pygame.MOUSEBUTTONDOWN:
                    if(roundedPos(pygame.mouse.get_pos()) in nodesDict):
                        node = aStarNodesDict[roundedPos(pygame.mouse.get_pos())]
                        print(node.__str__())
                        print("G score: " + str(node.gscore))
                        print("F score: " + str(node.fscore))
                        print("H score: " + str(node.hscore))
                if event.type == pygame.QUIT:
                    run = False
            if wantA:
                drawPath(Apath, SCREEN,1)
            if wantT:
                drawPath(Tpath,SCREEN,0)
            pygame.display.update()
    else:
        #if file was not detected
        randomBlockedSet = randomBlocked(ROWS, COLS, BLOCKSIZE) ## Check these numbers and make sure they match drawGrid
        start = randomVertex(ROWS, COLS, BLOCKSIZE, nodes)
        randomStart = nodes[start[0]][start[1]]
        end = randomVertex(ROWS, COLS, BLOCKSIZE, nodes)
        randomEnd = nodes[end[0]][end[1]]

        
        blocked_edges = genEdges(randomBlockedSet)

        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREEN.fill(WHITE)
        drawGrid(randomBlockedSet, randomStart, randomEnd)

        # UNCOMMENT BELOW FOR A* 
        #  aStar = AStar(randomStart, randomEnd, nodes, blocked_edges)
        # path = aStar[0]
        # nodesDict = aStar[1]
    

        # Configure blocked vertices for ThetaStar
        for coordinate in randomBlockedSet: 
            nodes[coordinate[0]][coordinate[1]].blocked = True

        # UNCOMMENT BELOW FOR THETASTAR
        thetaStar = ThetaStar(randomStart, randomEnd, nodes, blocked_edges)
        path = thetaStar[0]
        nodesDict = thetaStar[1]
        run = True
        i = 0
        while run:
            for event in pygame.event.get():
                if event.type== pygame.MOUSEBUTTONDOWN:
                    if(roundedPos(pygame.mouse.get_pos()) in nodesDict):
                        node = nodesDict[roundedPos(pygame.mouse.get_pos())]
                        print(node.__str__())
                        print("G score: " + str(node.gscore))
                        print("F score: " + str(node.fscore))
                        print("H score: " + str(node.hscore))
                if event.type == pygame.QUIT:
                    run = False
            # drawPath(aStarPath, SCREEN, 1)
            drawPath(path, SCREEN, 1)            
            pygame.display.update()

def roundedPos(position): 
    return (round(position[1]/BLOCKSIZE)), round(position[0]/BLOCKSIZE)

def genNodes():
    nodes = []
    for i in range(0, int(ROWS/BLOCKSIZE)+1):
        row = []
        for j in range(0, int(COLS/BLOCKSIZE)+1):
            node = Node(i, j)
            row.append(node)
        nodes.append(row)
    return nodes

def genEdges(blockedSet):
    # for row in nodes:
    #     for node in row:
    #         print("x: {}, y:{}".format(node.x, node.y))
    #     print()    

    # [(node1, node2)]

    # {
    #   ( (current.x, current.y), (neighbour.x, neighbour.y) ) = "open/blocked"
    # }
    # edges = dict()
    # for row in nodes:
    #     for node in row:
    #         # the loops below run 9 times
    #         for i in range(node.x-1, node.x+2):
    #             for j in range(node.y-1, node.y+2):
    #                 # neighbour is in grid, not the current node
    #                 if ((i>=0 and j>=0) and (i<len(nodes) and j<len(nodes[0])) and (i!=node.x or j!=node.y)):
    #                     # print("i: {}, j:{}".format(i, j))
    #                     # print()
    #                     neighbour = nodes[i][j]
    #                     edges[((node.x, node.y), (neighbour.x, neighbour.y))] = "open"        
            # print("done")
    # ( (n1.x, n1.y), (n2.x, n2.y) )        
    blocked_edges = set()
    for vertex in blockedSet:
        blocked_edges.add(((vertex[0], vertex[1]), (vertex[0]+1, vertex[1]+1)))
        blocked_edges.add(((vertex[0]+1, vertex[1]+1), (vertex[0], vertex[1])))
        
        blocked_edges.add(((vertex[0], vertex[1]+1), (vertex[0]+1, vertex[1])))
        blocked_edges.add(((vertex[0]+1, vertex[1]), (vertex[0], vertex[1]+1)))
        
        # checking block to the right
        if (vertex[0], vertex[1]+1) in blockedSet:
            blocked_edges.add((((vertex[0], vertex[1]+1), (vertex[0]+1, vertex[1]+1))))
            blocked_edges.add((((vertex[0]+1, vertex[1]+1), (vertex[0], vertex[1]+1))))

        # checking block below
        if (vertex[0]+1, vertex[1]) in blockedSet:
            blocked_edges.add((((vertex[0]+1, vertex[1]), (vertex[0]+1, vertex[1]+1))))
            blocked_edges.add((((vertex[0]+1, vertex[1]+1), (vertex[0]+1, vertex[1]))))
        # since we traverse the matrix left to right, top to bottom, no need to check for blocks to left or above

    return blocked_edges

def randomBlocked(rows, cols, blockSize): 
    blocked = set()
    numCells = int((rows/blockSize * cols/blockSize) * 0.1)
    for i in range(numCells): 
        randX = random.randrange(0, int(rows/blockSize))
        randY = random.randrange(0, int(cols/blockSize))
        pair = (randX, randY)
        blocked.add(pair)
    return blocked

#if we already have file of blocked cells
def setBlocked(blockedDict):
    blocked1=set()
    for key in blockedDict:
        blocked1.add(key)
    
    return blocked1


def randomVertex(rows, cols, blockSize, nodes):
    randX = random.randrange(0, int(rows/blockSize)+1)
    randY = random.randrange(0, int(cols/blockSize)+1)
    return (randX, randY)

def drawGrid(randomBlockedSet, randomStart, randomEnd):
    # print(randomBlockedSet)
    for x in range(0, int(ROWS/BLOCKSIZE)):
        for y in range(0, int(COLS/BLOCKSIZE)):
            # print("x: {}, y: {}".format(x,y))
            if((x, y) in randomBlockedSet):
                rect = pygame.Rect(y*BLOCKSIZE, x*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, BLACK, rect)
            
            else:
                rect = pygame.Rect(y*BLOCKSIZE, x*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
            pygame.draw.line(SCREEN, BLACK, (y*BLOCKSIZE ,x*BLOCKSIZE), (y*BLOCKSIZE + BLOCKSIZE, x*BLOCKSIZE + BLOCKSIZE))
            pygame.draw.line(SCREEN, BLACK, (y*BLOCKSIZE + BLOCKSIZE, x*BLOCKSIZE), (y*BLOCKSIZE, x*BLOCKSIZE + BLOCKSIZE))
    
    #(r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
    pygame.draw.circle(SCREEN, (GREEN), (randomStart.y*BLOCKSIZE, randomStart.x*BLOCKSIZE), 5, 5)
    pygame.draw.circle(SCREEN, (RED), (randomEnd.y*BLOCKSIZE, randomEnd.x*BLOCKSIZE), 5, 5)


# def drawLine(start, end): 
#     pygame.draw.line(SCREEN, (0, 0, 255), (start.y*BLOCKSIZE, start.x*BLOCKSIZE), (end.y*BLOCKSIZE, end.x*BLOCKSIZE), 3)

def drawPath(path, screen, number):
    for i in range(0, len(path)-1): 
        if (number==1):
            if (i!=0):
                pygame.draw.circle(SCREEN,(PURPLE), (path[i].y*BLOCKSIZE, path[i].x*BLOCKSIZE), 5, 5)
        drawLine(screen, path[i], path[i+1])

def drawLine(screen, start, end): 
    pygame.draw.line(screen, (0, 0, 255), (start.y * BLOCKSIZE, start.x * BLOCKSIZE), (end.y * BLOCKSIZE, end.x * BLOCKSIZE),max(int(0.2 * BLOCKSIZE), 5))

main()