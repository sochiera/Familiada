import pygame

from config import SCREEN_W, SCREEN_H

# Scale factors relative to the 1920×1080 base design
_sx = SCREEN_W / 1920
_sy = SCREEN_H / 1080

# Uniform scale for fonts (preserve readability on non-16:9 screens)
FONT_SCALE = min(_sx, _sy)


def scale_x(v: float) -> int:
    return int(v * _sx)


def scale_y(v: float) -> int:
    return int(v * _sy)


# Board panel (centered horizontally, upper portion of screen)
BOARD_LEFT   = scale_x(360)
BOARD_TOP    = scale_y(100)
BOARD_WIDTH  = scale_x(1200)
BOARD_HEIGHT = scale_y(825)  # 11 rows + SUMA line + padding

ROW_HEIGHT      = scale_y(65)
ROW_PADDING_TOP = scale_y(20)
ROWS = 11

# Width of the score click zone on the right edge of each row.
# Clicking this area reveals the score (step 2 of two-step reveal).
SCORE_COL_WIDTH = scale_x(110)

# 3 X-zones per side (outside the board panel)
X_ZONE_W = scale_x(130)
X_ZONE_H = scale_y(130)
LEFT_X_ZONES = [
    pygame.Rect(scale_x(200), scale_y(220), X_ZONE_W, X_ZONE_H),
    pygame.Rect(scale_x(200), scale_y(390), X_ZONE_W, X_ZONE_H),
    pygame.Rect(scale_x(200), scale_y(560), X_ZONE_W, X_ZONE_H),
]
RIGHT_X_ZONES = [
    pygame.Rect(scale_x(1590), scale_y(220), X_ZONE_W, X_ZONE_H),
    pygame.Rect(scale_x(1590), scale_y(390), X_ZONE_W, X_ZONE_H),
    pygame.Rect(scale_x(1590), scale_y(560), X_ZONE_W, X_ZONE_H),
]

# Single large X on the outermost side of each XXX panel.
_BIG_X_Y = LEFT_X_ZONES[0].top
_BIG_X_H = LEFT_X_ZONES[2].bottom - _BIG_X_Y
LEFT_BIG_X_RECT  = pygame.Rect(scale_x(200) - X_ZONE_W, _BIG_X_Y, X_ZONE_W, _BIG_X_H)
RIGHT_BIG_X_RECT = pygame.Rect(scale_x(1590) + X_ZONE_W, _BIG_X_Y, X_ZONE_W, _BIG_X_H)

# Team score counters (bottom corners)
TEAM1_RECT = pygame.Rect(scale_x(60),   scale_y(900), scale_x(300), scale_y(140))
TEAM2_RECT = pygame.Rect(scale_x(1560), scale_y(900), scale_x(300), scale_y(140))

# Undo button (top-right corner, unobtrusive)
COFNIJ_RECT = pygame.Rect(scale_x(1740), scale_y(20), scale_x(160), scale_y(55))

# Colors (green-on-black retro theme)
BLACK        = (0,   0,   0)
GREEN        = (0,   230, 0)
GREEN_DIM    = (0,   90,  0)
GREEN_BORDER = (0,   200, 0)
RED          = (220, 0,   0)
WHITE        = (255, 255, 255)
YELLOW       = (255, 220, 0)

# SUMA label vertical position (below the last row)
SUMA_Y = BOARD_TOP + ROW_PADDING_TOP + ROWS * ROW_HEIGHT + scale_y(20)


def get_row_text_rect(row_index: int) -> pygame.Rect:
    """Left part of a row: clicking reveals the word (step 1)."""
    y = BOARD_TOP + ROW_PADDING_TOP + row_index * ROW_HEIGHT
    return pygame.Rect(BOARD_LEFT, y, BOARD_WIDTH - SCORE_COL_WIDTH, ROW_HEIGHT)


def get_row_score_rect(row_index: int) -> pygame.Rect:
    """Right part of a row: clicking reveals the score (step 2)."""
    y = BOARD_TOP + ROW_PADDING_TOP + row_index * ROW_HEIGHT
    return pygame.Rect(
        BOARD_LEFT + BOARD_WIDTH - SCORE_COL_WIDTH, y,
        SCORE_COL_WIDTH, ROW_HEIGHT,
    )
