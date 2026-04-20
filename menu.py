import pygame
from config import *

class Button:

    def __init__(self, text, x, y, w, h):

        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

        self.font = pygame.font.SysFont("Segoe UI", 28)

    def draw(self, screen):

        mouse = pygame.mouse.get_pos()

        color = (80,80,200)

        if self.rect.collidepoint(mouse):
            color = (120,120,255)

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=10
        )

        label = self.font.render(self.text, True, (255,255,255))

        screen.blit(
            label,
            (
                self.rect.centerx - label.get_width() // 2,
                self.rect.centery - label.get_height() // 2
            )
        )

    def clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                return True

        return False


class Menu:

    def __init__(self, screen):

        self.screen = screen

        self.title_font = pygame.font.SysFont("Segoe UI", 64)

        center_x = SCREEN_WIDTH // 2

        self.start_btn = Button(
            "Start Game",
            center_x - 120,
            SCREEN_HEIGHT // 2,
            240,
            60
        )

        self.leader_btn = Button(
            "Leaderboard",
            center_x - 120,
            SCREEN_HEIGHT // 2 + 90,
            240,
            60
        )

        self.quit_btn = Button(
            "Quit",
            center_x - 120,
            SCREEN_HEIGHT // 2 + 180,
            240,
            60
        )


    def handle_event(self, event):

        if self.start_btn.clicked(event):
            return "start"

        if self.leader_btn.clicked(event):
            return "leaderboard"

        if self.quit_btn.clicked(event):
            return "quit"

        return None


    def draw(self):

        title = self.title_font.render(
            "POWER TETRIS",
            True,
            (255,255,255)
        )

        self.screen.blit(
            title,
            (
                SCREEN_WIDTH//2 - title.get_width()//2,
                SCREEN_HEIGHT//2 - 200
            )
        )

        self.start_btn.draw(self.screen)
        self.leader_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)