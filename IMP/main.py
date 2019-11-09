import pygame
import creatures
import board

(WIDTH, HEIGHT) = (1000, 800)
BACKGROUND_COLOR = (255,255,255) # white

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('NATURAL SELECTION SIMULATION')
screen.fill(BACKGROUND_COLOR)

env_board = board.Board(WIDTH, HEIGHT)
env_board.render(screen)

# when the end of code is reached
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
