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
        draw_brick(surface, brick)
    pygame.draw.rect(surface, COLOR_PADDLE, paddle.get_rect(), border_radius=4)
    pygame.draw.circle(surface, COLOR_BALL, (int(ball.x), int(ball.y)), ball.radius)


def draw_brick(surface, brick):
    rect = brick.get_rect()
    pygame.draw.rect(surface, brick.color, rect)

    if brick.brick_type == "unbreakable":
        # Metallic look: light top edge, dark bottom edge, rivets in the corners.
        pygame.draw.line(surface, (200, 200, 210), rect.topleft, (rect.right - 1, rect.top), 2)
        pygame.draw.line(surface, (60, 60, 70), (rect.left, rect.bottom - 1),
                         (rect.right - 1, rect.bottom - 1), 2)
        for cx in (rect.left + 6, rect.right - 7):
            for cy in (rect.top + 6, rect.bottom - 7):
                pygame.draw.circle(surface, (80, 80, 90), (cx, cy), 2)
        pygame.draw.rect(surface, (40, 40, 50), rect, 2)
    elif brick.brick_type == "strong":
        # Thick light border plus pips showing hits remaining.
        pygame.draw.rect(surface, (230, 240, 255), rect, 2)
        pip_r, gap = 3, 10
        start = rect.centerx - (brick.hits_remaining - 1) * gap / 2
        for i in range(brick.hits_remaining):
            pygame.draw.circle(surface, (20, 30, 70), (int(start + i * gap), rect.centery), pip_r)
    else:
        pygame.draw.rect(surface, (10, 10, 15), rect, 1)


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
