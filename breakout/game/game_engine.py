"""
GameEngine: owns the paddle, ball, and bricks.

Includes a 3-life system with game over / win states and restart (R),
three brick types (normal, strong, unbreakable), and combo scoring.

Combo scoring:
- Every brick destroyed back-to-back (without losing the ball) raises
  the combo; the multiplier is 1 + combo, capped at MAX_MULTIPLIER.
- Points for a destroyed brick = base points for its type * multiplier.
- Chipping a strong brick (not destroying it) earns a few points at the
  current multiplier but does not raise the combo.
- Losing the ball resets the combo back to x1.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick, NORMAL, STRONG, UNBREAKABLE
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50

STARTING_LIVES = 3

# Level layout: one character per brick.
#   N = normal, S = strong, U = unbreakable
# Unbreakable bricks sit in the top row so they never shield a
# breakable brick from below (which could make a level unwinnable).
LEVEL_LAYOUT = [
    "SUSSSSUS",
    "NNSNNSNN",
    "NNNNNNNN",
    "NNNNNNNN",
]
LAYOUT_TYPES = {"N": NORMAL, "S": STRONG, "U": UNBREAKABLE}

# Scoring
BRICK_POINTS = {NORMAL: 10, STRONG: 30}
CHIP_POINTS = 2
MAX_MULTIPLIER = 8


class GameEngine:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """Start (or restart) a fresh game."""
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.bricks = self._build_bricks()
        self.lives = STARTING_LIVES
        self.game_over = False
        self.won = False
        self.score = 0
        self.combo = 0

    @property
    def multiplier(self):
        return min(1 + self.combo, MAX_MULTIPLIER)

    def _on_brick_destroyed(self, brick):
        self.score += BRICK_POINTS.get(brick.brick_type, 0) * self.multiplier
        self.combo += 1  # next brick is worth more

    def _build_bricks(self):
        bricks = []
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2
        for row, line in enumerate(LEVEL_LAYOUT[:BRICK_ROWS]):
            for col, ch in enumerate(line[:BRICK_COLS]):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)
                bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, LAYOUT_TYPES[ch]))
        return bricks

    def breakable_bricks_left(self):
        return sum(1 for b in self.bricks if b.breakable)

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.paddle.x = WIDTH / 2

    def _lose_life(self):
        self.combo = 0  # missing the ball breaks the combo
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
        else:
            self._reset_ball()

    def handle_input(self, keys_pressed):
        if self.game_over or self.won:
            return
        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed
        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if key == pygame.K_r and (self.game_over or self.won):
            self.reset_game()

    def update(self):
        if self.game_over or self.won:
            return  # freeze the board until the player restarts

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        for brick in self.bricks:
            if handle_ball_brick_collision(self.ball, brick):
                if brick.hit():  # True only when a breakable brick runs out of hits
                    self.bricks.remove(brick)
                    self._on_brick_destroyed(brick)
                elif brick.breakable:
                    self.score += CHIP_POINTS * self.multiplier
                break

        # Unbreakable bricks don't count towards winning.
        if self.breakable_bricks_left() == 0:
            self.won = True

        if self.ball.is_below(HEIGHT):
            self._lose_life()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.paddle, self.ball, self.bricks)
        renderer.draw_hud(surface, font, self.score, self.multiplier,
                          self.breakable_bricks_left(), self.lives)
        if self.game_over:
            renderer.draw_banner(surface, font, f"GAME OVER  Score: {self.score}  (R to restart)")
        elif self.won:
            renderer.draw_banner(surface, font, f"YOU WIN!  Score: {self.score}  (R to replay)")
