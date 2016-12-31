import pygame

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True
        self.visited = False
        self.color = BLUE

    def getCenter(self, CELL_SIZE):
        return [self.x*CELL_SIZE + CELL_SIZE/2, self.y*CELL_SIZE + CELL_SIZE/2]

    def draw(self, screen, CELL_SIZE):
        pygame.draw.rect(screen, self.color, [self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE])
        if self.top:
            pygame.draw.line(screen, WHITE, [self.x*CELL_SIZE, self.y*CELL_SIZE], [self.x*CELL_SIZE+CELL_SIZE, self.y*CELL_SIZE], 1)
        if self.bottom:
            pygame.draw.line(screen, WHITE, [self.x*CELL_SIZE, self.y*CELL_SIZE+CELL_SIZE], [self.x*CELL_SIZE+CELL_SIZE, self.y*CELL_SIZE+CELL_SIZE], 1)
        if self.left:
            pygame.draw.line(screen, WHITE, [self.x*CELL_SIZE, self.y*CELL_SIZE], [self.x*CELL_SIZE, self.y*CELL_SIZE+CELL_SIZE], 1)
        if self.right:
            pygame.draw.line(screen, WHITE, [self.x*CELL_SIZE+CELL_SIZE, self.y*CELL_SIZE], [self.x*CELL_SIZE+CELL_SIZE, self.y*CELL_SIZE+CELL_SIZE], 1)

    def getAdjacentTiles(self, CELLS, CELL_NUM, CELL_SIZE, careVisit=True):
        ret = []
        if self.x-1>=0:
            c = CELLS[(self.x-1)*CELL_NUM + self.y]
            if not (c.visited == careVisit):
                ret.append(c)
        if (self.x+1)*CELL_SIZE<CELL_NUM*CELL_SIZE:
            c = CELLS[(self.x+1)*CELL_NUM + self.y]
            if not (c.visited == careVisit):
                ret.append(c)
        if self.y-1>=0:
            c = CELLS[(self.x)*CELL_NUM + self.y-1]
            if not (c.visited == careVisit):
                ret.append(c)
        if (self.y+1)*CELL_SIZE<CELL_NUM*CELL_SIZE:
            c = CELLS[(self.x)*CELL_NUM + self.y+1]
            if not (c.visited == careVisit):
                ret.append(c)
        return ret