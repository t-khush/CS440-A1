import pygame
import random
from AStar import AStar
from helper import Node, Edge

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
ROWS = 400 #1000 
COLS = 300 #500 
BLOCKSIZE = 100 # 10

def main():

    # for x in range(0, int(ROWS/BLOCKSIZE)):
    #     for y in range(0, int(COLS/BLOCKSIZE)):
    #         print("x: {}, y: {}".format(x,y))

    global SCREEN
    randomBlockedSet = randomBlocked(ROWS, COLS, BLOCKSIZE) ## Check these numbers and make sure they match drawGrid
    randomStart = randomVertex(ROWS, COLS, BLOCKSIZE)
    randomEnd = randomVertex(ROWS, COLS, BLOCKSIZE)

    print(randomBlockedSet)
    print(str(randomStart.x) + " " + str(randomStart.y))
    print(str(randomEnd.x) + " " + str(randomEnd.y))
    
    nodes = genNodes()
    edges = genEdges(nodes, randomBlockedSet)

    # print("Edge count:", len(edges))
    # for edge in edges:
    #     print("n1: {}, n2: {}".format((edge.n1.x, edge.n1.y), (edge.n2.x, edge.n2.y)))
        
    # aStar = AStar(ROWS, COLS, BLOCKSIZE, randomStart, randomEnd, nodes, edges, randomBlockedSet)

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)
    run = True
    i = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawGrid(randomBlockedSet, randomStart, randomEnd)
        AStar(randomStart, randomEnd, genNodes(), genEdges(genNodes(), randomBlockedSet), randomBlockedSet, SCREEN)
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
    for blocked in randomBlockedSet:
        curr_node = nodes[blocked[0]][blocked[1]]
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

def randomVertex(rows, cols, blockSize):
    randX = random.randrange(0, int(rows/blockSize)+1)
    randY = random.randrange(0, int(cols/blockSize)+1)
    return Node(randX, randY)

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

main()