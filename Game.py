import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
A = '59484536727466346764'
B = ''
C = ''


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        x = 0
        for i in range(1, self.height):
            self.board[i][0] = A[x]
            x += 1
        for i in range(1, self.width):
            self.board[0][i] = A[x]
            x += 1
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.cell_type = [[0] * width for _ in range(height)]

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, a=None, b=None, type=''):
        for i in range(self.height):
            for j in range(self.width):
                f = (self.left + self.cell_size * j, self.top + self.cell_size * i)
                pygame.draw.rect(screen, WHITE, (
                    self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size), 1)
                self.board[i][j] = f
        if a and b:
            if type and self.cell_type[b][a] == 0:
                pygame.draw.line(screen, BLUE,
                                 [self.left + self.cell_size * a + 2, self.top + self.cell_size * b + 2],
                                 [self.left + self.cell_size * (a + 1) - 2,
                                  self.top + self.cell_size * (b + 1) - 2], 2)
                pygame.draw.line(screen, BLUE,
                                 [self.left + self.cell_size * (a + 1) - 2, self.top + self.cell_size * b + 2],
                                 [self.left + self.cell_size * a + 2, self.top + self.cell_size * (b + 1) - 2], 2)
                self.cell_type[b][a] = 1
            else:
                if self.cell_type[b][a] == 0:
                    pygame.draw.rect(screen, RED, (
                    self.left + self.cell_size * a, self.top + self.cell_size * b, self.cell_size - 1,
                    self.cell_size - 1))
                    self.cell_type[b][a] = 1
                elif self.cell_type[b][a] == 1:
                    pygame.draw.rect(screen, BLACK, (
                    self.left + self.cell_size * a, self.top + self.cell_size * b, self.cell_size - 1,
                    self.cell_size - 1))
                    self.cell_type[b][a] = 0

    def get_left_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_left_click(cell)

    def get_right_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_right_click(cell)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] > self.board[-1][-1][0] + self.cell_size or mouse_pos[1] > self.board[-1][-1][
            1] + self.cell_size:
            return None
        for i in range(self.height):
            for j in range(self.width):
                if (mouse_pos[0] < self.board[i][j][0] + self.cell_size) and (
                        mouse_pos[1] < self.board[i][j][1] + self.cell_size):
                    cell = ((self.board[i][j][0] - self.left) // self.cell_size,
                            (self.board[i][j][1] - self.top) // self.cell_size)
                    return cell

    def on_left_click(self, cell_coords):
        if cell_coords:
            self.render(cell_coords[0], cell_coords[1])
            pygame.display.flip()
        else:
            pass

    def on_right_click(self, cell_coords):
        if cell_coords:
            self.render(cell_coords[0], cell_coords[1], 'cross')
            pygame.display.flip()
        else:
            pass


pygame.init()
board = Board(11, 11)
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

running = True

screen.fill((0, 0, 0))
board.render()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_left_click(event.pos)
            if event.button == 3:
                board.get_right_click(event.pos)
    pygame.display.flip()
