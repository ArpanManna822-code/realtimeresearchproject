import pygame
import random
from config import *

class Particle:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.vx = random.uniform(-2,2)
        self.vy = random.uniform(-4,-1)

        self.life = random.randint(30,50)

        self.color = color


    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.2

        self.life -= 1


    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            4
        )


class ParticleSystem:

    def __init__(self):

        self.particles = []


    def spawn_line_clear(self):

        center_x = BOARD_X + BOARD_WIDTH // 2
        center_y = BOARD_Y + BOARD_HEIGHT // 2

        for i in range(40):

            color = random.choice(BLOCK_COLORS)

            self.particles.append(
                Particle(center_x, center_y, color)
            )


    def spawn_explosion(self, x, y):

        for i in range(25):

            color = random.choice(BLOCK_COLORS)

            self.particles.append(
                Particle(x, y, color)
            )


    def update(self):

        for p in self.particles[:]:

            p.update()

            if p.life <= 0:
                self.particles.remove(p)


    def draw(self, screen):

        for p in self.particles:
            p.draw(screen)