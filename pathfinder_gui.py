import pygame
import math
from queue import PriorityQueue

# setting the size of the windows that will open up upon running the program
# want it to be a square, thus only the one dimension is needed to initialize
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm - by Samir") 

# initialize RGB colour codes that will be used later on
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 33, 243)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:

    def __init__(self, row, col, width, total_rows):

        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = BLACK # ** Change this to dark mode, Onyx for example 
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        
        return self.row, self.col
    
    def is_closed(self):

        return self.colour == RED
    
    def is_open(self):

        return self.colour == GREEN
    
    def is_barrier(self):

        return self.colour == WHITE # ** Change this to white
    
    def is_start(self):

        return self.colour == ORANGE
    
    def is_end(self): 
        
        return self.colour == TURQUOISE # ** maybe use more retro or pastel colours 
    
    def reset(self):

        self.colour = BLACK # ** Again change to dark theme

    def make_start(self):

        self.colour = ORANGE 

    def make_closed(self):

        self.colour = RED

    def make_open(self):

        self.colour = GREEN

    def make_barrier(self):

        self.colour = WHITE # ** Change to WHITE

    def make_end(self):

        self.colour = TURQUOISE

    def make_path(self):

        self.colour = BLUE

    def draw(self, win):
        
        # draws a rectangle 
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):

        self.neighbours = []
        
        # check if it can move down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            
            self.neighbours.append(grid[self.row + 1][self.col])
        
        # check if it can move up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            
            self.neighbours.append(grid[self.row - 1][self.col])

        # check if it can move right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            
            self.neighbours.append(grid[self.row][self.col + 1])

        # check if it can move left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            
            self.neighbours.append(grid[self.row][self.col - 1])

        
    def __lt__(self, other):

        # __lt__ is less than

        return False
    
# define the heurestic function
def heurestic(p1, p2):

    # using manhattan distance which is an "L" shape distance 
    # not diagonal

    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2,) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):

    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # so that when the end node is reached, it is not automatically 
    # assumed that that is the best path
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heurestic(start.get_pos(), end.get_pos())


    open_set_hash = {start} # check if anything is in the priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
           
           reconstruct_path(came_from, end, draw)
           end.make_end()
           
           return True

        for neighbour in current.neighbours:
            
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + heurestic(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
             
        draw()

        if current != start:
            current.make_closed()

    return False # did not find a path


def make_grid(rows, width):

    grid = []
    gap = width // rows

    for i in range(rows):
        
        grid.append([])
        for j in range(rows):

            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

# draw the lined in the grid
def draw_grid_lines(win, rows, width):

    gap = width // rows

    for i in range(rows):

        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # ** Change GREY to Light Grey 

        for j in range(rows):

            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # ** Change GREY

def draw(win, grid, rows, width):

    win.fill(WHITE) # ** Change maybe

    for row in grid:

        for node in row:

            node.draw(win)

    draw_grid_lines(win, rows, width)
    pygame.display.update()

# a function that will allow the user to click and create a maze like structure in the grid
def get_position_clicked(pos, rows, width): 
    
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):

    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    
    while run:
        
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_position_clicked(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()
                
                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                
                pos = pygame.mouse.get_pos()
                row, col = get_position_clicked(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None

                elif node == end:
                    end = None
                    
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE and start and end:
                    
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c: #clears the grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)

