import pygame
import random

from config import *
from board import Board
from tetromino import Tetromino, rotate
from leaderboard import save_score
from powerups import activate_powerup
from particles import ParticleSystem
from ui import UI
from menu import Menu
from background import Background

class GameEngine:

    def __init__(self, screen):

        self.screen = screen

        self.board = Board()

        self.ui = UI(screen)

        self.menu = Menu(screen)

        self.particles = ParticleSystem()

        self.score = 0
        self.lines = 0
        self.level = 1

        self.state = "menu"

        self.fall_timer = 0
        self.speed = INITIAL_SPEED

        self.current_piece = self.spawn_piece()

        self.next_queue = [
            self.spawn_piece(),
            self.spawn_piece(),
            self.spawn_piece()
        ]

        self.hold_piece = None
        self.hold_used = False

        self.ghost_y = 0

        self.background = Background()

        self.combo = 0

        self.powerup_message = ""
        self.powerup_timer = 0

        self.move_delay = 120
        self.move_timer = 0

        self.player_name = ""
        self.entering_name = False


    def spawn_piece(self):

        color = random.choice(BLOCK_COLORS)

        return Tetromino(color)


    def reset_game(self):

        self.board = Board()

        self.score = 0
        self.lines = 0
        self.level = 1

        self.speed = INITIAL_SPEED

        self.current_piece = self.spawn_piece()
        self.next_piece = self.spawn_piece()

        self.state = "game"


    def handle_event(self, event):

        if self.state == "menu":

            action = self.menu.handle_event(event)

            if action == "start":
                self.reset_game()

            if action == "leaderboard":
                self.state = "leaderboard"

            if action == "quit":
                pygame.quit()
                exit()


        elif self.state == "leaderboard":

            if event.type == pygame.KEYDOWN:
                self.state = "menu"


        elif self.state == "game":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.state = "pause"

                if event.key == pygame.K_DOWN:
                    self.soft_drop()

                if event.key == pygame.K_SPACE:
                    self.hard_drop()

                if event.key == pygame.K_UP:
                    self.rotate_piece()

                if event.key == pygame.K_c:
                    self.hold()


        elif self.state == "pause":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.state = "game"

                if event.key == pygame.K_m:

                    if self.score > 0:

                        self.player_name = ""
                        self.state = "name_entry"

                    else:
                        self.state = "menu"


        elif self.state == "gameover":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.reset_game()

                if event.key == pygame.K_m:
                    self.state = "menu"

        elif self.state == "name_entry":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if self.player_name.strip() == "":
                        self.player_name = "Player"

                    save_score(self.player_name, self.score)

                    self.state = "leaderboard"

                elif event.key == pygame.K_BACKSPACE:

                    self.player_name = self.player_name[:-1]

                else:

                    if len(self.player_name) < 12:
                        self.player_name += event.unicode


    def move_piece(self, dx):

        if not self.collision(self.current_piece.shape,
                              self.current_piece.x + dx,
                              self.current_piece.y):

            self.current_piece.x += dx


    def soft_drop(self):

        if not self.collision(self.current_piece.shape,
                              self.current_piece.x,
                              self.current_piece.y + 1):

            self.current_piece.y += 1


    def hard_drop(self):

        while not self.collision(self.current_piece.shape,
                                 self.current_piece.x,
                                 self.current_piece.y + 1):

            self.current_piece.y += 1

        self.lock_piece()


    def rotate_piece(self):

        rotated = rotate(self.current_piece.shape)

        if not self.collision(rotated,
                              self.current_piece.x,
                              self.current_piece.y):

            self.current_piece.shape = rotated


    def collision(self, shape, x, y):

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):

                if cell:

                    nx = int(x + j)
                    ny = int(y + i)

                    if nx < 0 or nx >= COLS:
                        return True

                    if ny >= ROWS:
                        return True

                    if ny >= 0 and self.board.grid[ny][nx]:
                        return True

        return False


    def lock_piece(self):

        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):

                if cell:

                    x = int(self.current_piece.x + j)
                    y = int(self.current_piece.y + i)

                    if 0 <= x < COLS and 0 <= y < ROWS:
                        self.board.grid[y][x] = self.current_piece.color


        cleared = self.board.clear_lines()

        if cleared > 0:

            self.combo += 1

            combo_bonus = self.combo * 50

            self.score += cleared * 100 + combo_bonus

            self.lines += cleared

            self.particles.spawn_line_clear()

            activate_powerup(self)

        else:
            self.combo = 0


        self.current_piece = self.next_queue.pop(0)

        self.next_queue.append(self.spawn_piece())

        self.hold_used = False

        if self.collision(self.current_piece.shape,
                          self.current_piece.x,
                          self.current_piece.y):

            self.player_name = ""
            self.entering_name = True
            self.state = "name_entry"


    def update(self, dt):

        if self.state == "game":

            self.fall_timer += dt

            if self.fall_timer > self.speed:

                self.fall_timer = 0

                if not self.collision(self.current_piece.shape,
                                      self.current_piece.x,
                                      self.current_piece.y + 1):

                    self.current_piece.y += 1

                else:

                    self.lock_piece()

            self.update_ghost()

        self.particles.update()

        if self.powerup_timer > 0:
            self.powerup_timer -= 1

        keys = pygame.key.get_pressed()

        self.move_timer += dt

        if self.move_timer > self.move_delay:

            if keys[pygame.K_LEFT]:

                if not self.collision(self.current_piece.shape,
                                    self.current_piece.x - 1,
                                    self.current_piece.y):

                    self.current_piece.x -= 1
                    self.move_timer = 0

            if keys[pygame.K_RIGHT]:

                if not self.collision(self.current_piece.shape,
                                    self.current_piece.x + 1,
                                    self.current_piece.y):

                    self.current_piece.x += 1
                    self.move_timer = 0


    def update_ghost(self):

        ghost_y = self.current_piece.y

        while not self.collision(self.current_piece.shape,
                                 self.current_piece.x,
                                 ghost_y + 1):

            ghost_y += 1

        self.ghost_y = ghost_y


    def draw(self):

        self.screen.fill(BACKGROUND)

        self.background.update()
        self.background.draw(self.screen)

        if self.state == "menu":
            self.menu.draw()

        elif self.state == "leaderboard":
            self.ui.draw_leaderboard()
        
        elif self.state == "name_entry":
            self.ui.draw_name_entry(self.player_name, self.score)

        else:

            self.ui.draw_board(self.board.grid)

            self.ui.draw_ghost(self.current_piece, self.ghost_y)

            self.ui.draw_piece(self.current_piece)

            self.ui.draw_next(self.next_queue)

            self.ui.draw_hold(self.hold_piece)

            self.ui.draw_stats(self.score, self.lines, self.level)

            self.ui.draw_combo(self.combo)

            self.ui.draw_powerup(self.powerup_message, self.powerup_timer)

            self.particles.draw(self.screen)

            if self.state == "pause":
                self.ui.draw_pause()

            if self.state == "gameover":
                self.ui.draw_gameover(self.score)

    def hold(self):

        if self.hold_used:
            return

        if self.hold_piece is None:

            self.hold_piece = self.current_piece
            self.current_piece = self.next_queue.pop(0)

            self.next_queue.append(self.spawn_piece())

        else:

            self.current_piece, self.hold_piece = self.hold_piece, self.current_piece

        self.current_piece.x = 4
        self.current_piece.y = 0

        self.hold_used = True

    