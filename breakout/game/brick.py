"""
Brick: a single block. Three types:

- NORMAL:      destroyed after 1 hit
- STRONG:      needs several hits; colour fades as it takes damage
- UNBREAKABLE: never destroyed, just bounces the ball
"""

import pygame

NORMAL = "normal"
STRONG = "strong"
UNBREAKABLE = "unbreakable"

STRONG_HITS = 3

# Base colours per type
COLOR_NORMAL = (220, 90, 90)        # red
COLOR_STRONG_FULL = (70, 120, 255)  # deep blue at full health
COLOR_STRONG_WEAK = (170, 200, 255) # pale blue when nearly broken
COLOR_UNBREAKABLE = (130, 130, 140) # steel grey


class Brick:
    def __init__(self, x, y, width, height, brick_type=NORMAL):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type
        if brick_type == STRONG:
            self.max_hits = STRONG_HITS
        else:
            self.max_hits = 1
        self.hits_remaining = self.max_hits

    @property
    def breakable(self):
        return self.brick_type != UNBREAKABLE

    def hit(self):
        """
        Register a hit. Returns True if this hit destroyed the brick.
        Unbreakable bricks ignore hits entirely.
        """
        if not self.breakable:
            return False
        self.hits_remaining -= 1
        return self.hits_remaining <= 0

    @property
    def color(self):
        if self.brick_type == UNBREAKABLE:
            return COLOR_UNBREAKABLE
        if self.brick_type == STRONG:
            # Blend from full colour to weak colour as damage accumulates.
            t = 1 - (self.hits_remaining - 1) / max(1, self.max_hits - 1)
            return tuple(
                int(a + (b - a) * t) for a, b in zip(COLOR_STRONG_FULL, COLOR_STRONG_WEAK)
            )
        return COLOR_NORMAL

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
