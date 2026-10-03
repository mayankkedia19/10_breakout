"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 640, 520
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (20, 20, 30)
COLOR_PADDLE = (80, 180, 255)
COLOR_BALL = (240, 240, 240)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, paddle, ball, bricks):
    surface.fill(COLOR_BG)
    for brick in bricks:
        pygame.draw.rect(surface, brick.color, brick.get_rect())
        pygame.draw.rect(surface, (10, 10, 15), brick.get_rect(), 1)
    pygame.draw.rect(surface, COLOR_PADDLE, paddle.get_rect(), border_radius=4)
    pygame.draw.circle(surface, COLOR_BALL, (int(ball.x), int(ball.y)), ball.radius)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 60))
    # Dark backing box so the message is readable over the bricks/ball.
    pygame.draw.rect(surface, (0, 0, 0), rect.inflate(30, 20), border_radius=6)
    pygame.draw.rect(surface, (255, 220, 80), rect.inflate(30, 20), 2, border_radius=6)
    surface.blit(surf, rect)


def draw_lives(surface, font, lives):
    """Draw 'Lives:' plus one small ball icon per remaining life, top-right."""
    label = font.render("Lives:", True, COLOR_TEXT)
    icon_r, spacing = 6, 18
    total = label.get_width() + 8 + spacing * 3
    x = surface.get_width() - total - 10
    surface.blit(label, (x, 10))
    cx = x + label.get_width() + 8 + icon_r
    for i in range(3):
        color = (255, 90, 90) if i < lives else (70, 70, 80)
        pygame.draw.circle(surface, color, (cx + i * spacing, 21), icon_r)
