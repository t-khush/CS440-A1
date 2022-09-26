
import sys
import pygame
import random
from AStar import AStar
from ThetaStar import ThetaStar
from helper import Node, Edge

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
ROWS = 400 #1000 
COLS = 300 #500 
BLOCKSIZE = 100 # 10
Textfile= False

startVertex=(0,0)
endVertex=(0,0)
blockedCells=dict()

if len(sys.argv)>1:
    file1= sys.argv[1]
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

        print(startVertex)
        print(endVertex)
       

        #Getting the blocked cells
        for line in f.readlines():
            split = line.strip().split()
            if (int(split[2])==1):
                blockedCells[(int(split[1]) -1, int(split[0])-1 )] = int(split[2])
           
        
        print(blockedCells)

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

       
        edges = genEdges(nodes, tBlockedSet)


        pygame.init()
        SCREEN= pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        SCREEN.fill(WHITE)
        drawGrid(tBlockedSet, tStart, tEnd)
        path = AStar(tStart, tEnd, nodes, edges, tBlockedSet, SCREEN)
        run1= True

        while run1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            drawPath(path, SCREEN)
            pygame.display.update()
    else:
        #if file was not detected
        randomBlockedSet = randomBlocked(ROWS, COLS, BLOCKSIZE) ## Check these numbers and make sure they match drawGrid
        start = randomVertex(ROWS, COLS, BLOCKSIZE, nodes)
        randomStart = nodes[start[0]][start[1]]
        end = randomVertex(ROWS, COLS, BLOCKSIZE, nodes)
        randomEnd = nodes[end[0]][end[1]]

        print(randomBlockedSet)
        print(str(randomStart.x) + " " + str(randomStart.y))
        print(str(randomEnd.x) + " " + str(randomEnd.y))
        
        
        edges = genEdges(nodes, randomBlockedSet)

        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREEN.fill(WHITE)
        drawGrid(randomBlockedSet, randomStart, randomEnd)
        aStarPath = AStar(randomStart, randomEnd, nodes, edges, randomBlockedSet, SCREEN)
        thetaStarPath = ThetaStar(randomStart, randomEnd, nodes, edges, randomBlockedSet, SCREEN)

        # drawGrid(randomBlockedSet, Node(2,3), Node(2,0))
        # path = AStar(Node(2,3), Node(2,0), genNodes(), genEdges(genNodes(), randomBlockedSet), randomBlockedSet, SCREEN)
        run = True
        i = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            drawPath(aStarPath, SCREEN)
            pygame.display.update()

def genNodes():
    nodes = []
    for i in range(0, int(ROWS/BLOCKSIZE)+1):
        row = []
        for j in range(0, int(COLS/BLOCKSIZE)+1):
            node = Node(i, j)
            row.append(node)
        nodes.append(row)
    return nodes

def genEdges(nodes, randomBlockedSet):
    # for row in nodes:
    #     for node in row:
    #         print("x: {}, y:{}".format(node.x, node.y))
    #     print()    

    # [(node1, node2)]
    edges=[]
    for row in nodes:
        for node in row:
            # the loops below run 9 times
            for i in range(node.x-1, node.x+2):
                for j in range(node.y-1, node.y+2):
                    # neighbour is in grid, not the current node
                    if ((i>=0 and j>=0) and (i<len(nodes) and j<len(nodes[0])) and (i!=node.x or j!=node.y)):
                        # print("i: {}, j:{}".format(i, j))
                        # print()
                        neighbour = nodes[i][j]
                        edge = Edge(node, neighbour)
                        edges.append(edge)          
            # print("done")
    
    # now that edges have been generated, we can use 'randomBlockedSet' to block out edges
    # for blocked in randomBlockedSet:
    #     curr_node = nodes[blocked[0]][blocked[1]]
        # work in progress
    
    
    return edges

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
    pygame.draw.circle(SCREEN, (0,255,0), (randomStart.y*BLOCKSIZE, randomStart.x*BLOCKSIZE), 5, 5)
    pygame.draw.circle(SCREEN, (255,0,0), (randomEnd.y*BLOCKSIZE, randomEnd.x*BLOCKSIZE), 5, 5) 


# def drawLine(start, end): 
#     pygame.draw.line(SCREEN, (0, 0, 255), (start.y*BLOCKSIZE, start.x*BLOCKSIZE), (end.y*BLOCKSIZE, end.x*BLOCKSIZE), 3)

def drawPath(path, screen):
    for i in range(0, len(path)-1): 
        drawLine(screen, path[i], path[i+1])

def drawLine(screen, start, end): 
    pygame.draw.line(screen, (0, 0, 255), (start.y * BLOCKSIZE, start.x * BLOCKSIZE), (end.y * BLOCKSIZE, end.x * BLOCKSIZE),int(0.04 * BLOCKSIZE))

main()