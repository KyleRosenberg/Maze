import sys
import pygame
import pickle
from Cell import Cell
from Generator import load

if len(sys.argv) < 2:
    exit()

pygame.init()
size = [800,800]
screen = pygame.display.set_mode(size)

CELLS = load(sys.argv[1])
CELL_NUM = int(len(CELLS) ** (.5))
CELL_SIZE = int(size[0] / CELL_NUM)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Node(Cell):

    def __init__(self, cell):
        Cell.__init__(self, cell.x, cell.y)
        self.top = cell.top
        self.bottom = cell.bottom
        self.left = cell.left
        self.right = cell.right
        self.visited = cell.visited
        self.color = cell.color
        self.G = 0
        self.F = 0
        self.H = 0
        self.Parent = None

    def getG(self):
        g = self.G
        if self.Parent is not None:
            g += self.Parent.getG()
        return g

    def setValues(self, parent, end):
        self.Parent = parent
        self.G = 10
        self.H = (abs(end.x - self.x) + abs(end.y - self.y))*10
        self.F = self.getG() + self.H

    def getNodePath(self):
        if self.Parent is None:
            return [self]
        else:
            return self.Parent.getNodePath() + [self]

class MazeSolver:

    def __init__(self):
        self.open = []
        self.closed = []
        self.NODES = []
        for i in range(len(CELLS)):
            c = CELLS[i]
            n = Node(c)
            self.NODES.append(n)
        self.current_cell = self.NODES[0]
        self.current_cell.Parent = None
        self.end_cell = self.getEndCell()
        for c in self.NODES:
            c.draw(screen, CELL_SIZE)

    def getEndCell(self):
        for c in self.NODES:
            if c.color == GREEN:
                return c
        return None

    def getReachableCells(self, cell):
        adj = Cell.getAdjacentTiles(cell, self.NODES, CELL_NUM, CELL_SIZE, False)
        ret = []
        for a in adj:
            if a.x<cell.x:
                if not a.right and not cell.left and not a in self.closed:
                    ret.append(a)
            elif a.x>cell.x:
                if not a.left and not cell.right and not a in self.closed:
                    ret.append(a)
            elif a.y<cell.y:
                if not a.bottom and not cell.top and not a in self.closed:
                    ret.append(a)
            elif a.y>cell.y:
                if not a.top and not cell.bottom and not a in self.closed:
                    ret.append(a)
        return ret

    def solve(self):
        self.open.append(self.current_cell)
        while self.end_cell not in self.closed:
            reachable = self.getReachableCells(self.current_cell)
            self.closed.append(self.current_cell)
            self.open.remove(self.current_cell)
            smallestF = 2**31-1
            next = None
            for node in reachable:
                if node in self.open:
                    oldParentG = node.getG()
                    newParentG = self.current_cell.getG() + node.G
                    if newParentG < oldParentG:
                        node.setValues(self.current_cell, self.end_cell)
                else:
                    self.open.append(node)
                    node.setValues(self.current_cell, self.end_cell)
                if node.F < smallestF:
                    smallestF = node.F
                    next = node
            if next is None:
                for n in self.open:
                    if n.F < smallestF:
                        smallestF = n.F
                        next = n
            self.current_cell = next
            if self.current_cell not in self.closed:
                self.open.append(self.current_cell)
            if self.current_cell == self.end_cell:
                self.closed.append(self.end_cell)
                return self.end_cell.getNodePath()

def main():
    done = False
    clock = pygame.time.Clock()
    solver = MazeSolver()
    solved = solver.solve()
    draw = 1
    while not done:
        clock.tick()

        c = solved[draw]
        pc = solved[draw-1]
        pygame.draw.line(screen, BLUE, pc.getCenter(CELL_SIZE), c.getCenter(CELL_SIZE), 1)

        draw += 1
        if draw >= len(solved):
            draw = len(solved) - 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()

if __name__ == "__main__":
    main()