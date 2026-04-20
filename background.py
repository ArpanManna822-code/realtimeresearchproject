import pygame
import random
from config import *

class Star:

    def __init__(self):

        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

        self.speed = random.uniform(0.2, 1.0)

        self.size = random.randint(1,3)

    def update(self):

        self.y += self.speed

        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (80,80,120),
            (int(self.x), int(self.y)),
            self.size
        )


class Background:

    def __init__(self):

        self.stars = [Star() for _ in range(120)]

    def update(self):

        for star in self.stars:
            star.update()

    def draw(self, screen):

        for star in self.stars:
            star.draw(screen)