import os
import random

cols = 100
rows = 50
dirpath = 'grids'
# first create 'grids' directory if it doesn't exist already
if (os.path.exists(os.path.join(os.getcwd(), dirpath)) is False):
    os.mkdir('grids')

def main():
    # generate 50 grids of size 100 x 50
    # only generates 1 test rn, change it to 50 for all test cases
    for i in range(1):
        goal = randomVertex()
        end = randomVertex()
        blocked_set = randomBlockedSet()
        file_path = os.path.join(dirpath, f'test_case_{i+1}.txt')
        with open(file_path, mode='w') as f:
            f.write(f'{goal[0]} {goal[1]}\n')
            f.write(f'{end[0]} {end[1]}\n')
            f.write(f'{cols} {rows}\n')

            for i in range(1, cols):
                for j in range (1, rows):
                    if (i,j) in  blocked_set:
                        f.write(f'{i} {j} {1}\n')
                    else:
                        f.write(f'{i} {j} {0}\n')

def randomVertex():
    # vertex can be 101,51 so we want 101 and 51 in range
    randX = random.randrange(1, cols+2)
    randY = random.randrange(1, rows+2)
    return (randX, randY)

def randomBlockedSet():
    blocked_set = set()
    # 10% of total cells
    numCells = rows*cols*0.1
    while len(blocked_set) != numCells:
        randX = random.randrange(1, cols+1)
        randY = random.randrange(1, rows+1)
        blocked_set.add((randX, randY))
    print("\n", blocked_set, "\n")
    return blocked_set

main()