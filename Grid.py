import sys
import pygame
import random
from AStar import AStar
from ThetaStar import ThetaStar
from helper import Node
from memory_profiler import profile

BLACK = (0, 0, 0)
GREEN= (0,255,0)
RED= (255,0,0)
WHITE = (255, 255, 255)
PURPLE= (62.7,12.5,94.1)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000
ROWS = 500 #1000 
COLS = 1000 #500 
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

pathSetting= sys.argv[1]
if (pathSetting== "astar"):
    wantA= True
if (pathSetting== "thetastar"):
    wantT= True

if len(sys.argv)==3:
    file1= sys.argv[2]
    Textfile= True
    with open(file1, 'r') as f:
        #since we have orgin at (0,0), we have to move
        #the values by one
        line = f.readline().strip().split()
        startVertex = (int(line[0])-1 , int(line[1]) -1) 

        line = f.readline().strip().split()
        endVertex = (int(line[0])-1 , int(line[1])-1 )

        line = f.readline().strip().split()
        BLOCKSIZE = 10
        COLS = int(line[0])*BLOCKSIZE
        ROWS = int(line[1])*BLOCKSIZE
        

        #Getting the blocked cells
        for line in f.readlines():
            split = line.strip().split()
            if (int(split[2])==1):
                blockedCells[(int(split[1]) -1, int(split[0])-1 )] = int(split[2])

# @profile # uncomment for measuring memory use. The global variables and other things before main are miniscule and can be ignored for code simplicity
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
        path = []
        nodesDict = dict()
        if wantA:
            Apath = AStar(tStart, tEnd, nodes, blocked_edges)
            path = Apath[0]
            nodesDict = Apath[1]

        # Configure blocked vertices for ThetaStar
        if wantT:
            for coordinate in tBlockedSet: 
                nodes[coordinate[0]][coordinate[1]].blocked = True

            Tpath = ThetaStar(tStart, tEnd, nodes, blocked_edges)
            path = Tpath[0]
            nodesDict = Tpath[1]

        run = True
        while run:
            for event in pygame.event.get():
                if event.type== pygame.MOUSEBUTTONDOWN:
                    if(roundedPos(pygame.mouse.get_pos()) in nodesDict):
                        node = nodesDict[roundedPos(pygame.mouse.get_pos())]
                        print("(",(node.y)+1,",",(node.x)+1,")")
                        print("G score: " + str(node.gscore))
                        print("F score: " + str(node.fscore))
                        print("H score: " + str(node.hscore))
                if event.type == pygame.QUIT:
                    run = False
            # drawPath(aStarPath, SCREEN, 1)
            drawPath(path, SCREEN, 1)            
            pygame.display.update()
            # break -> use this break when testing runtime or running analyzer bc user doesn't have to click on close to move onto next test case
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

        path = []
        nodesDict = dict()
        if wantA:
            Apath = AStar(randomStart, randomEnd, nodes, blocked_edges)
            path = Apath[0]
            nodesDict = Apath[1]
        if wantT:
            for coordinate in randomBlockedSet: 
                nodes[coordinate[0]][coordinate[1]].blocked = True

            Tpath = ThetaStar(randomStart, randomEnd, nodes, blocked_edges)
            path = Tpath[0]
            nodesDict = Tpath[1]

        run = True
        while run:
            for event in pygame.event.get():
                if event.type== pygame.MOUSEBUTTONDOWN:
                    if(roundedPos(pygame.mouse.get_pos()) in nodesDict):
                        node = nodesDict[roundedPos(pygame.mouse.get_pos())]
                        print("(",(node.y)+1,",",(node.x)+1,")")
                        print("G score: " + str(node.gscore))
                        print("F score: " + str(node.fscore))
                        print("H score: " + str(node.hscore))
                if event.type == pygame.QUIT:
                    run = False
            # drawPath(aStarPath, SCREEN, 1)
            drawPath(path, SCREEN, 1)            
            pygame.display.update()
            # break

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
    while len(blocked) != numCells: 
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
        drawLine(screen, path[i], path[i+1])
        if (number==1):
            if (i!=0):
                pygame.draw.circle(SCREEN,(PURPLE), (path[i].y*BLOCKSIZE, path[i].x*BLOCKSIZE), 4, 4)

def drawLine(screen, start, end): 
    pygame.draw.line(screen, (0, 0, 255), (start.y * BLOCKSIZE, start.x * BLOCKSIZE), (end.y * BLOCKSIZE, end.x * BLOCKSIZE),max(int(0.075 * BLOCKSIZE), 5))

main()