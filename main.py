import sys

import pygame

from data import load_rounds
from layout import COFNIJ_RECT, LEFT_X_ZONES, RIGHT_X_ZONES
from layout import LEFT_BIG_X_RECT, RIGHT_BIG_X_RECT
from layout import TEAM1_RECT, TEAM2_RECT
from layout import get_row_text_rect, get_row_score_rect
from config import SCREEN_W, SCREEN_H, FULLSCREEN
from renderer import load_fonts, render_frame
from sounds import SoundManager
from state import (
    GameState,
    action_add_x_left,
    action_add_x_right,
    action_add_big_x_left,
    action_add_big_x_right,
    action_reveal_full,
    action_reveal_score,
    action_transfer_to_team,
    make_initial_state,
)

def handle_click(pos: tuple, ctx: dict, push, sounds: SoundManager, rounds: list) -> None:
    """Dispatch a mouse click to the appropriate game action."""
    state: GameState = ctx["state"]

    # Gameover screen — any click restarts the whole game
    if state.phase == "gameover":
        ctx["history"].clear()
        ctx["state"] = make_initial_state(rounds)
        return

    # COFNIJ (undo) — pop the last state from history
    if COFNIJ_RECT.collidepoint(pos):
        if ctx["history"]:
            ctx["state"] = ctx["history"].pop()
        return

    # Answer rows — single-click reveal (word + points at once):
    #   click on text/dots area → reveal word and score (0 → 2)
    #   click on score area     → reveal score if word already shown (1 → 2)
    n_rows = len(state.rounds[state.round_index].answers)
    for i in range(n_rows):
        if get_row_text_rect(i).collidepoint(pos):
            new_state = action_reveal_full(state, i)
            if new_state is not state:
                push(new_state)
                sounds.play_reveal_score()
            return

        if get_row_score_rect(i).collidepoint(pos):
            new_state = action_reveal_score(state, i)
            if new_state is not state:
                push(new_state)
                sounds.play_reveal_score()
            return

    # Left X zones
    for i, rect in enumerate(LEFT_X_ZONES):
        if rect.collidepoint(pos):
            new_state = action_add_x_left(state, i)
            if new_state is not state:
                push(new_state)
                sounds.play_wrong()
            return

    # Right X zones
    for i, rect in enumerate(RIGHT_X_ZONES):
        if rect.collidepoint(pos):
            new_state = action_add_x_right(state, i)
            if new_state is not state:
                push(new_state)
                sounds.play_wrong()
            return

    # Large X panels (outermost)
    if LEFT_BIG_X_RECT.collidepoint(pos):
        new_state = action_add_big_x_left(state)
        if new_state is not state:
            push(new_state)
            sounds.play_wrong()
        return

    if RIGHT_BIG_X_RECT.collidepoint(pos):
        new_state = action_add_big_x_right(state)
        if new_state is not state:
            push(new_state)
            sounds.play_wrong()
        return

    # Team score counters
    if TEAM1_RECT.collidepoint(pos):
        push(action_transfer_to_team(state, 1))
        sounds.play_transfer()
        return

    if TEAM2_RECT.collidepoint(pos):
        push(action_transfer_to_team(state, 2))
        sounds.play_transfer()
        return


def main() -> None:
    pygame.init()
    flags = pygame.FULLSCREEN if FULLSCREEN else 0
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
    pygame.display.set_caption("Familiada")
    clock = pygame.time.Clock()

    sounds = SoundManager()
    fonts = load_fonts()

    rounds = load_rounds("rounds")

    # ctx dict holds mutable game state so closures can update it cleanly
    ctx: dict = {
        "state": make_initial_state(rounds),
        "history": [],
    }

    def push(new_state: GameState) -> None:
        ctx["history"].append(ctx["state"])
        ctx["state"] = new_state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(event.pos, ctx, push, sounds, rounds)

        render_frame(screen, ctx["state"], fonts, len(ctx["history"]))
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
