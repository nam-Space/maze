import pygame
from random import choice
import time


def input_box(prompt):
    input_active = True
    input_text = ''
    input_box_width = 200
    input_box_height = 32
    input_box_x = (pygame.display.get_surface().get_width() - input_box_width) // 2
    input_box_y = (pygame.display.get_surface().get_height() - input_box_height) // 2
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        input_value = int(input_text)
                        input_active = False
                    except ValueError:
                        input_text = ''  # Reset input if not a valid integer
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        sc.fill((30, 30, 30))
        txt_surface = font.render(prompt, True, pygame.Color('white'))
        sc.blit(txt_surface, (input_box_x, input_box_y - 30))
        txt_surface = font.render(input_text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        pygame.draw.rect(sc, color, (input_box_x, input_box_y, width, input_box_height), 2)
        sc.blit(txt_surface, (input_box_x + 5, input_box_y + 5))
        pygame.display.flip()
        clock.tick(30)

    return input_value


pygame.init()
font = pygame.font.Font(None, 32)
sc = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("DFS")

cols = input_box("Nhap so cot (<= 25): ")
rows = input_box("Nhap so hang (<= 13): ")
speed = input_box("Speed (<=60): ")

TILE = 60
WIDTH = cols * TILE
HEIGHT = rows * TILE
RES = (WIDTH, HEIGHT)
sc = pygame.display.set_mode(RES)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self):
        x = self.x * TILE
        y = self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, TILE + y), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)

    def drawCurrentCells(self):
        x = self.x * TILE
        y = self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def drawPathToTarget(self):
        x = self.x * TILE
        y = self.y * TILE
        pygame.draw.rect(sc, pygame.Color('aqua'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def checkCell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.checkCell(self.x, self.y - 1)
        right = self.checkCell(self.x + 1, self.y)
        bottom = self.checkCell(self.x, self.y + 1)
        left = self.checkCell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False


def removeWall(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
startGame = False
endGame = False
start = grid_cells[0]
target = grid_cells[(cols - 1) + (rows - 1) * cols]


def draw_button(text, position, size, color, highlight):
    font = pygame.font.Font(None, 36)
    button = pygame.Rect(position, size)
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button.collidepoint(mouse_pos):
        pygame.draw.rect(sc, highlight, button)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(sc, color, button)

    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=button.center)
    sc.blit(text_surf, text_rect)
    return False


game_started = False


def reset_game():
    global grid_cells, current_cell, stack, startGame, endGame, start, target
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    startGame = False
    endGame = False
    start = grid_cells[0]
    target = grid_cells[(cols - 1) + (rows - 1) * cols]


def DFS(start, target):
    explored = [target]
    frontier = [target]
    dfsPath = {}
    while len(frontier) > 0:
        currCell = frontier.pop()
        if currCell == grid_cells[0]:
            break
        for d in ['top', 'right', 'bottom', 'left']:
            if not currCell.walls[d]:
                if d == 'top':
                    childCell = currCell.checkCell(currCell.x, currCell.y - 1)
                if d == 'right':
                    childCell = currCell.checkCell(currCell.x + 1, currCell.y)
                if d == 'bottom':
                    childCell = currCell.checkCell(currCell.x, currCell.y + 1)
                if d == 'left':
                    childCell = currCell.checkCell(currCell.x - 1, currCell.y)

                if childCell in explored:
                    continue

                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell

    # fwdPath = {}
    start.drawPathToTarget()
    while start != target:
        # fwdPath[dfsPath[start]] = start
        start = dfsPath[start]
        start.drawPathToTarget()
        pygame.display.flip()
        clock.tick(20)

    global endGame
    endGame = True


need_reset = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    sc.fill(pygame.Color('darkslategray'))

    if not game_started:
        if draw_button("Start", (WIDTH / 2 - 100, HEIGHT / 2 - 30), (200, 60), pygame.Color('forestgreen'),
                       pygame.Color('lime')):
            game_started = True
            reset_game()
    else:
        if not endGame:
            [cell.draw() for cell in grid_cells]
            current_cell.visited = True
            current_cell.drawCurrentCells()

            if not startGame:
                next_cell = current_cell.check_neighbors()
                if current_cell == grid_cells[0] and not next_cell:
                    startGame = True

                if next_cell:
                    stack.append(current_cell)
                    next_cell.visited = True
                    removeWall(current_cell, next_cell)
                    current_cell = next_cell
                elif stack:
                    current_cell = stack.pop()
            else:
                DFS(start, target)
                pygame.time.delay(10000)
        else:
            if draw_button("Reset", (WIDTH / 2 - 100, HEIGHT / 2 - 30), (200, 60), pygame.Color('red'),
                           pygame.Color('darkred')):
                need_reset = True

    if need_reset:
        cols = input_box("Nhap so cot (<= 25): ")
        rows = input_box("Nhap so hang (<= 13): ")
        speed = input_box("Speed (<=60): ")
        TILE = 60
        WIDTH = cols * TILE
        HEIGHT = rows * TILE
        RES = (WIDTH, HEIGHT)
        sc = pygame.display.set_mode(RES)
        reset_game()
        need_reset = False

    pygame.display.flip()
    clock.tick(speed)
