import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000


def main():
    global SCREEN
    randomBlockedSet = randomBlocked(1000, 500, 50) ## Check these numbers and make sure they match drawGrid
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawGrid(randomBlockedSet)
        pygame.display.update()

def randomBlocked(rows, cols, blockSize): 
    blocked = set()
    numCells = int((rows/blockSize * cols/blockSize) * 0.1)
    for i in range(numCells): 
        randX = random.randrange(0, rows, blockSize)
        randY = random.randrange(0, cols, blockSize)
        pair = (randX, randY)
        blocked.add(pair)
    return blocked

def drawGrid(randomBlockedSet):
    blockSize = 50 # Change this to 10 so dimensions are correct. 
    rows = 1000 # 1000
    cols = 500 # 500
    print(randomBlockedSet)
    for y in range(0, cols, blockSize):
        for x in range(0, rows, blockSize):
            rect = pygame.Rect(y, x, blockSize, blockSize)
            if((x, y) in randomBlockedSet):
                pygame.draw.rect(SCREEN, BLACK, rect)
            else: 
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
            pygame.draw.line(SCREEN, BLACK, (y ,x), (y + blockSize, x + blockSize))
            pygame.draw.line(SCREEN, BLACK, (y + blockSize, x - blockSize), (y - blockSize, x + blockSize))


    


main()