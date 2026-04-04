import pygame

SCREEN_W = 1920
SCREEN_H = 1080

# Board panel (centered horizontally, upper portion of screen)
BOARD_LEFT   = 360
BOARD_TOP    = 100
BOARD_WIDTH  = 1200
BOARD_HEIGHT = 700  # 6 rows + SUMA line + padding

ROW_HEIGHT      = 90
ROW_PADDING_TOP = 30
ROWS = 6

# Width of the score click zone on the right edge of each row.
# Clicking this area reveals the score (step 2 of two-step reveal).
SCORE_COL_WIDTH = 110

# 3 X-zones per side (outside the board panel)
X_ZONE_W = 130
X_ZONE_H = 130
LEFT_X_ZONES = [
    pygame.Rect(200, 220, X_ZONE_W, X_ZONE_H),
    pygame.Rect(200, 390, X_ZONE_W, X_ZONE_H),
    pygame.Rect(200, 560, X_ZONE_W, X_ZONE_H),
]
RIGHT_X_ZONES = [
    pygame.Rect(1590, 220, X_ZONE_W, X_ZONE_H),
    pygame.Rect(1590, 390, X_ZONE_W, X_ZONE_H),
    pygame.Rect(1590, 560, X_ZONE_W, X_ZONE_H),
]

# Single large X on the outermost side of each XXX panel.
# Same width as a small X zone, 3× the height, vertically centred on the 3 zones.
_BIG_X_H = X_ZONE_H * 3          # 390
_BIG_X_Y = 220 + (X_ZONE_H * 3 - _BIG_X_H) // 2  # = 220 (top-aligned with top zone)
LEFT_BIG_X_RECT  = pygame.Rect(200 - X_ZONE_W,       _BIG_X_Y, X_ZONE_W, _BIG_X_H)
RIGHT_BIG_X_RECT = pygame.Rect(1590 + X_ZONE_W,      _BIG_X_Y, X_ZONE_W, _BIG_X_H)

# Team score counters (bottom corners)
TEAM1_RECT = pygame.Rect(60,   900, 300, 140)
TEAM2_RECT = pygame.Rect(1560, 900, 300, 140)

# Undo button (top-right corner, unobtrusive)
COFNIJ_RECT = pygame.Rect(1740, 20, 160, 55)

# Colors (green-on-black retro theme)
BLACK        = (0,   0,   0)
GREEN        = (0,   230, 0)
GREEN_DIM    = (0,   90,  0)
GREEN_BORDER = (0,   200, 0)
RED          = (220, 0,   0)
WHITE        = (255, 255, 255)
YELLOW       = (255, 220, 0)

# SUMA label vertical position (below the 6 rows)
SUMA_Y = BOARD_TOP + ROW_PADDING_TOP + ROWS * ROW_HEIGHT + 20


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
