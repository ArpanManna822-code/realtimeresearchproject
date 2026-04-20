import pygame
from config import *
from leaderboard import load_scores

class UI:

    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.SysFont("Segoe UI", 24)
        self.big_font = pygame.font.SysFont("Segoe UI", 48)

    def draw_board(self, grid):

        for y in range(ROWS):
            for x in range(COLS):

                rect = pygame.Rect(
                    BOARD_X + x * GRID_SIZE,
                    BOARD_Y + y * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE
                )

                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

                if grid[y][x]:

                    pygame.draw.rect(
                        self.screen,
                        grid[y][x],
                        rect.inflate(-2, -2),
                        border_radius=6
                    )

                    glow = rect.inflate(6,6)

                    pygame.draw.rect(
                        self.screen,
                        grid[y][x],
                        glow,
                        2,
                        border_radius=8
                    )


    def draw_piece(self, piece):

        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):

                if cell:

                    rect = pygame.Rect(
                        BOARD_X + (piece.x + j) * GRID_SIZE,
                        BOARD_Y + (int(piece.y) + i) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )

                    pygame.draw.rect(
                        self.screen,
                        piece.color,
                        rect.inflate(-2, -2),
                        border_radius=6
                    )


    def draw_ghost(self, piece, ghost_y):

        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):

                if cell:

                    rect = pygame.Rect(
                        BOARD_X + (piece.x + j) * GRID_SIZE,
                        BOARD_Y + (ghost_y + i) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )

                    pygame.draw.rect(
                        self.screen,
                        (120,120,120),
                        rect.inflate(-6,-6),
                        2
                    )


    def draw_next(self, queue):

        panel_x = BOARD_X + BOARD_WIDTH + 50
        panel_y = BOARD_Y

        title = self.font.render("Next", True, (255,255,255))
        self.screen.blit(title, (panel_x, panel_y))

        for idx, piece in enumerate(queue):

            for i,row in enumerate(piece.shape):
                for j,cell in enumerate(row):

                    if cell:

                        rect = pygame.Rect(
                            panel_x + j*25,
                            panel_y + 40 + idx*80 + i*25,
                            25,
                            25
                        )

                        pygame.draw.rect(
                            self.screen,
                            piece.color,
                            rect,
                            border_radius=5
                        )


    def draw_stats(self, score, lines, level):

        x = BOARD_X - 200
        y = BOARD_Y

        score_text = self.font.render(f"Score: {score}", True, (255,255,255))
        lines_text = self.font.render(f"Lines: {lines}", True, (255,255,255))
        level_text = self.font.render(f"Level: {level}", True, (255,255,255))

        self.screen.blit(score_text, (x, y))
        self.screen.blit(lines_text, (x, y + 40))
        self.screen.blit(level_text, (x, y + 80))


    def draw_pause(self):

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0,0,0))

        self.screen.blit(overlay,(0,0))

        text = self.big_font.render("PAUSED", True, (255,255,255))
        sub = self.font.render("ESC = Resume | M = Menu", True, (200,200,200))

        self.screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(sub, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 + 10))


    def draw_gameover(self, score):

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0,0,0))

        self.screen.blit(overlay,(0,0))

        text = self.big_font.render("GAME OVER", True, (255,80,80))
        score_text = self.font.render(f"Score: {score}", True, (255,255,255))
        sub = self.font.render("R = Restart | M = Menu", True, (200,200,200))

        self.screen.blit(text, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 60))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2))
        self.screen.blit(sub, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 40))


    def draw_leaderboard(self):

        scores = load_scores()

        title = self.big_font.render("Leaderboard", True, (255,255,255))
        self.screen.blit(title,(SCREEN_WIDTH//2 - 150,100))

        y = 200

        for entry in scores:

            text = self.font.render(
                f"{entry['name']}   {entry['score']}",
                True,
                (200,200,200)
            )

            self.screen.blit(text,(SCREEN_WIDTH//2 - 100,y))

            y += 40

        hint = self.font.render("Press any key to return", True, (180,180,180))
        self.screen.blit(hint,(SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT - 120))

    def draw_hold(self, piece):

        if piece is None:
            return

        panel_x = BOARD_X - 180
        panel_y = BOARD_Y

        title = self.font.render("Hold", True, (255,255,255))

        self.screen.blit(title, (panel_x, panel_y))

        for i,row in enumerate(piece.shape):
            for j,cell in enumerate(row):

                if cell:

                    rect = pygame.Rect(
                        panel_x + j*25,
                        panel_y + 40 + i*25,
                        25,
                        25
                    )

                    pygame.draw.rect(
                        self.screen,
                        piece.color,
                        rect,
                        border_radius=5
                    )

    def draw_combo(self, combo):

        if combo <= 1:
            return

        text = self.font.render(
            f"Combo x{combo}",
            True,
            (255,220,120)
        )

        self.screen.blit(
            text,
            (BOARD_X + BOARD_WIDTH + 50, BOARD_Y + 200)
        )

    def draw_powerup(self, message, timer):

        if timer <= 0:
            return
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(40)
        overlay.fill((255,200,80))

        self.screen.blit(overlay,(0,0))

        text = self.big_font.render(
            f"{message}!",
            True,
            (255,200,50)
        )

        self.screen.blit(
            text,
            (
                SCREEN_WIDTH//2 - text.get_width()//2,
                BOARD_Y - 60
            )
        )

    def draw_name_entry(self, name, score):

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0,0,0))

        self.screen.blit(overlay,(0,0))

        title = self.big_font.render("NEW HIGH SCORE!", True, (255,220,80))
        score_text = self.font.render(f"Score: {score}", True, (255,255,255))
        prompt = self.font.render("Enter Your Name:", True, (200,200,200))

        name_text = self.big_font.render(name + "_", True, (255,255,255))

        self.screen.blit(title,(SCREEN_WIDTH//2 - 200,200))
        self.screen.blit(score_text,(SCREEN_WIDTH//2 - 80,260))
        self.screen.blit(prompt,(SCREEN_WIDTH//2 - 120,330))
        self.screen.blit(name_text,(SCREEN_WIDTH//2 - name_text.get_width()//2,380))