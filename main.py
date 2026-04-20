import pygame
from config import *
from engine import GameEngine
from leaderboard import init_db

pygame.init()

init_db()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN
)

pygame.display.set_caption("Power Tetris")

clock = pygame.time.Clock()

game = GameEngine(screen)

running = True

while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_F11:
                running = False

        game.handle_event(event)

    game.update(dt)

    game.draw()

    pygame.display.update()

pygame.quit()