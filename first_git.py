import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
fps = 50
clock = pygame.time.Clock()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
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

    def render(self, a=None, b=None, color=''):
        for i in range(self.height):
            for j in range(self.width):
                f = (self.left + self.cell_size * j, self.top + self.cell_size * i)
                pygame.draw.rect(screen, WHITE, (
                    self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size), 1)
                self.board[i][j] = f
        if a:
            if color == 'Green':
                pygame.draw.rect(screen, GREEN, (self.left + self.cell_size * a, self.top + self.cell_size * b, self.cell_size - 1, self.cell_size - 1))
                self.cell_type[b][a] = 1
            elif color == 'Black':
                pygame.draw.rect(screen, BLACK, (self.left + self.cell_size * a, self.top + self.cell_size * b, self.cell_size - 1, self.cell_size - 1))
                self.cell_type[b][a] = None

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
            self.render(cell_coords[0], cell_coords[1], 'Green')
            pygame.display.flip()
        else:
            pass

    def on_right_click(self, cell_coords):
        if cell_coords:
            self.render(cell_coords[0], cell_coords[1], 'Black')
            pygame.display.flip()
        else:
            pass

    def alive(self, point, board):
        x, y = point
        counts = self.count_live_neighbors(point, board)
        if counts == 3 or (counts == 2 and point in board):
            return True
        return False

    def count_live_neighbors(self, point, board):
        j = 0
        for i in self.get_neighbors(point):
            if i in board:
                j = j + 1
        return j

    def get_neighbors(self, point):
        x, y = point
        return [((x + j), (y + i)) for i in range(-1, 2) for j in range(-1, 2) if not i == j == 0]

    def play(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.alive((i, j), self.board)




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
            elif event.button == 3:
                board.get_right_click(event.pos)
        while event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.play()
    pygame.display.flip()
    clock.tick(fps)
