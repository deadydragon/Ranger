import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

sizy = input().split()
side = int(sizy[1]) - 1
N = int(sizy[0])
K = int(sizy[1])

pygame.init()
size = width, height = N * K * 3 * 2, N * K * 3 * 2
screen = pygame.display.set_mode(size)


def draw():
    screen.fill((0, 0, 0))
    for i in range(K):
        pygame.draw.circle(screen, BLUE, (K * N * 3, K * N * 3), ((K - i) * N * 3))
        pygame.draw.circle(screen, GREEN, (K * N * 3, K * N * 3), ((K - i) * N * 3) - N)
        pygame.draw.circle(screen, RED, (K * N * 3, K * N * 3), ((K - i) * N * 3) - N * 2)
    pygame.display.flip()


while pygame.event.wait().type != pygame.QUIT:
    draw()

pygame.quit()