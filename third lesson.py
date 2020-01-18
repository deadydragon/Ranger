import pygame

WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.step = False
        self.cell_type = [[0] * width for _ in range(height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, a=None, b=None):
        for i in range(self.height):
            for j in range(self.width):
                f = (self.left + self.cell_size * j, self.top + self.cell_size * i)
                pygame.draw.rect(screen, WHITE, (
                    self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size), 1)
                self.board[i][j] = f
        if a is not None:
            if self.step:
                if self.cell_type[b][a]:
                    pass
                else:
                    pygame.draw.line(screen, BLUE,
                                     [self.left + self.cell_size * a + 2, self.top + self.cell_size * b + 2],
                                     [self.left + self.cell_size * (a + 1) - 2,
                                      self.top + self.cell_size * (b + 1) - 2], 2)
                    pygame.draw.line(screen, BLUE,
                                     [self.left + self.cell_size * (a + 1) - 2, self.top + self.cell_size * b + 2],
                                     [self.left + self.cell_size * a + 2, self.top + self.cell_size * (b + 1) - 2], 2)
                    self.cell_type[b][a] = 1
                    self.step = False
            else:
                if self.cell_type[b][a]:
                    pass
                else:
                    pygame.draw.circle(screen, RED, (
                        self.left + self.cell_size * a + self.cell_size // 2,
                        self.top + self.cell_size * b + self.cell_size // 2), self.cell_size // 2 - 2, 2)
                    self.cell_type[b][a] = 1
                    self.step = True

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
            self.render(cell_coords[0], cell_coords[1])
            pygame.display.flip()
        else:
            pass


pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

running = True
board = Board(5, 7)

screen.fill((0, 0, 0))
board.render()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_left_click(event.pos)
            # elif event.button == 3:
            #    board.get_right_click(event.pos)
    pygame.display.flip()
