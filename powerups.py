import random
from config import *

POWERUPS = [
    "bomb",
    "clear_row",
    "score_boost",
    "slow_time"
]

def activate_powerup(engine):

    power = random.choice(POWERUPS)

    engine.powerup_message = power.upper().replace("_"," ")
    engine.powerup_timer = 120

    if power == "bomb":
        bomb(engine)

    elif power == "clear_row":
        clear_row(engine)

    elif power == "score_boost":
        score_boost(engine)

    elif power == "slow_time":
        slow_time(engine)


def bomb(engine):

    center_x = COLS // 2
    center_y = ROWS // 2

    for y in range(center_y - 2, center_y + 3):
        for x in range(center_x - 2, center_x + 3):

            if 0 <= x < COLS and 0 <= y < ROWS:
                engine.board.grid[y][x] = 0

    engine.particles.spawn_explosion(
        BOARD_X + BOARD_WIDTH // 2,
        BOARD_Y + BOARD_HEIGHT // 2
    )


def clear_row(engine):

    row = random.randint(0, ROWS - 1)

    for x in range(COLS):
        engine.board.grid[row][x] = 0

    engine.score += 150


def score_boost(engine):

    engine.score += 500


def slow_time(engine):

    engine.speed += 200