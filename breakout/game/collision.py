"""
collision: ball-vs-brick collision handling.
"""


def handle_ball_brick_collision(ball, brick):
    """
    If the ball overlaps the brick, bounce it off and return True.

    The bounce axis is chosen by the smallest overlap: if the ball
    entered through the top/bottom we flip vy, through a side we flip vx.
    """
    ball_rect = ball.get_rect()
    brick_rect = brick.get_rect()
    if not ball_rect.colliderect(brick_rect):
        return False

    overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
    overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)

    if overlap_x < overlap_y:
        # Side hit: push the ball out horizontally and reverse vx.
        if ball.x < brick_rect.centerx:
            ball.x = brick_rect.left - ball.radius
            ball.vx = -abs(ball.vx)
        else:
            ball.x = brick_rect.right + ball.radius
            ball.vx = abs(ball.vx)
    else:
        # Top/bottom hit: push the ball out vertically and reverse vy.
        if ball.y < brick_rect.centery:
            ball.y = brick_rect.top - ball.radius
            ball.vy = -abs(ball.vy)
        else:
            ball.y = brick_rect.bottom + ball.radius
            ball.vy = abs(ball.vy)
    return True
