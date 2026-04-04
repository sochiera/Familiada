"""Unit tests for layout.py — TDD cycles."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
pygame.init()

import pytest
from layout import (
    BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, ROW_HEIGHT, ROW_PADDING_TOP,
    SCORE_COL_WIDTH,
    get_row_text_rect, get_row_score_rect,
    LEFT_X_ZONES, RIGHT_X_ZONES,
    TEAM1_RECT, TEAM2_RECT, COFNIJ_RECT,
)


# ---------------------------------------------------------------------------
# Cykl 14: get_row_text_rect
# ---------------------------------------------------------------------------

def test_row_text_rect_y_position_row0():
    rect = get_row_text_rect(0)
    expected_y = BOARD_TOP + ROW_PADDING_TOP
    assert rect.y == expected_y


def test_row_text_rect_y_position_row3():
    rect = get_row_text_rect(3)
    expected_y = BOARD_TOP + ROW_PADDING_TOP + 3 * ROW_HEIGHT
    assert rect.y == expected_y


def test_row_text_rect_x_starts_at_board_left():
    rect = get_row_text_rect(0)
    assert rect.x == BOARD_LEFT


def test_row_text_rect_width_leaves_room_for_score():
    rect = get_row_text_rect(0)
    assert rect.width == BOARD_WIDTH - SCORE_COL_WIDTH


def test_row_text_rect_height_equals_row_height():
    rect = get_row_text_rect(0)
    assert rect.height == ROW_HEIGHT


# ---------------------------------------------------------------------------
# Cykl 15: get_row_score_rect
# ---------------------------------------------------------------------------

def test_row_score_rect_starts_after_text():
    text_rect = get_row_text_rect(0)
    score_rect = get_row_score_rect(0)
    assert score_rect.x == text_rect.x + text_rect.width


def test_row_score_rect_width_is_score_col_width():
    rect = get_row_score_rect(0)
    assert rect.width == SCORE_COL_WIDTH


def test_row_score_rect_same_y_as_text():
    assert get_row_score_rect(2).y == get_row_text_rect(2).y


def test_row_text_and_score_rects_are_adjacent():
    """Text rect right edge should be exactly score rect left edge."""
    for i in range(6):
        t = get_row_text_rect(i)
        s = get_row_score_rect(i)
        assert t.right == s.left, f"Row {i}: gap between text and score rects"


# ---------------------------------------------------------------------------
# Cykl 15b: stałe Recty (X-zones, team, undo)
# ---------------------------------------------------------------------------

def test_left_x_zones_count():
    assert len(LEFT_X_ZONES) == 3


def test_right_x_zones_count():
    assert len(RIGHT_X_ZONES) == 3


def test_team_rects_on_opposite_sides():
    assert TEAM1_RECT.x < TEAM2_RECT.x


def test_cofnij_rect_in_top_right():
    """Undo button should be in the upper-right area of the screen."""
    from layout import SCREEN_W, SCREEN_H
    assert COFNIJ_RECT.x > SCREEN_W * 0.8
    assert COFNIJ_RECT.y < SCREEN_H * 0.1
