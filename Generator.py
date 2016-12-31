import pygame
import random
import pickle
import os.path
import sys
from Cell import Cell

if len(sys.argv) < 2:
    exit()

sys.setrecursionlimit(10000000)

pygame.init()
size = [800,800]
screen = pygame.display.set_mode(size)

CELL_NUM = 0
CELL_SIZE = 0
CELLS = []
UNVISITED = []
VISITED = []
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class MazeGenerator:

    def __init__(self):
        for x in range(CELL_NUM):
            for y in range(CELL_NUM):
                c = Cell(x, y)
                CELLS.append(c)  # An index can be made by CELLS[x*CELL_NUM + y]
                UNVISITED.append(c)
        self.current_cell = UNVISITED[0]
        self.current_cell.visited = True
        self.current_cell.color = BLACK
        self.longestPath = 1
        self.currentPath = 1
        self.start = CELLS[0]
        self.end = CELLS[0]
        self.saved = False
        screen.fill(BLACK)
        for c in CELLS:
            c.draw(screen, CELL_SIZE)

    def doMazeGen(self):
        neigh = self.current_cell.getAdjacentTiles(CELLS, CELL_NUM, CELL_SIZE)
        ret = []
        if len(neigh) > 0:
            r = random.randint(0, len(neigh) - 1)
            nextCell = neigh[r]
            nextCell.visited = True
            ret.append(self.current_cell)
            ret.append(nextCell)
            if nextCell.x < self.current_cell.x:
                self.current_cell.left = False
                nextCell.right = False
            elif nextCell.x > self.current_cell.x:
                self.current_cell.right = False
                nextCell.left = False
            elif nextCell.y < self.current_cell.y:
                self.current_cell.top = False
                nextCell.bottom = False
            else:
                self.current_cell.bottom = False
                nextCell.top = False
            self.current_cell = nextCell
            self.current_cell.color = BLACK
            VISITED.append(self.current_cell)
            del UNVISITED[UNVISITED.index(self.current_cell)]
            self.currentPath += 1
        else:
            if self.currentPath > self.longestPath:
                self.longestPath = self.currentPath
                self.end.color = BLACK
                ret.append(self.end)
                self.end = self.current_cell
                self.end.color = GREEN
                self.start.color = RED
                ret.append(self.end)
                ret.append(self.start)
            try:
                while len(neigh)<1:
                    self.current_cell = VISITED.pop()
                    self.currentPath -= 1
                    neigh = self.current_cell.getAdjacentTiles(CELLS, CELL_NUM, CELL_SIZE)
            except (IndexError):
                UNVISITED.clear()
        return ret

def save():
    i = 1
    while os.path.isfile("maze" + str(i) + ".mz"):
        i+=1
    pickle.dump(CELLS, open("maze" + str(i) + ".mz", "wb"))

def load(file):
    return pickle.load(open(file, "rb"))

def main():
    generator = MazeGenerator()
    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick()
        if len(UNVISITED) > 0:
            cells = generator.doMazeGen()
            for c in cells:
               c.draw(screen, CELL_SIZE)
        elif not generator.saved:
            save()
            generator.saved = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()

if __name__ == "__main__":
    CELL_NUM = int(sys.argv[1])
    CELL_SIZE = int(size[0]/CELL_NUM)
    main()