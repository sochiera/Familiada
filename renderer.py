import pathlib

import pygame

from layout import (
    SCREEN_W, SCREEN_H,
    BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT,
    ROW_HEIGHT, ROW_PADDING_TOP, ROWS,
    LEFT_X_ZONES, RIGHT_X_ZONES,
    TEAM1_RECT, TEAM2_RECT,
    COFNIJ_RECT, SUMA_Y,
    BLACK, GREEN, GREEN_DIM, GREEN_BORDER, RED, YELLOW,
)
from state import compute_suma

# Total character width of the "rank + text + dots" portion of a row string.
# With a monospace font this keeps all rows the same pixel width.
BODY_CHARS = 34


def load_fonts() -> dict:
    """
    Resolve the best available monospace/retro font and return a dict of
    pygame.Font objects at the sizes used by the renderer.

    Priority:
      1. fonts/VT323-Regular.ttf  (bundled — guaranteed retro LED look)
      2. System fonts: vt323, pressstart2p, couriernew, courier,
                       ubuntumono, dejavusansmono
      3. pygame default font (always available, last resort)
    """
    candidates = [
        ("file", "fonts/VT323-Regular.ttf"),
        ("sys",  "vt323"),
        ("sys",  "pressstart2p"),
        ("sys",  "couriernew"),
        ("sys",  "courier"),
        ("sys",  "ubuntumono"),
        ("sys",  "dejavusansmono"),
    ]

    resolved_path = None
    for kind, name in candidates:
        if kind == "file":
            p = pathlib.Path(name)
            if p.exists():
                resolved_path = str(p)
                break
        else:
            match = pygame.font.match_font(name)
            if match:
                resolved_path = match
                break

    if not resolved_path:
        resolved_path = pygame.font.get_default_font()

    def F(size: int) -> pygame.font.Font:
        return pygame.font.Font(resolved_path, size)

    return {
        "board": F(52),   # answer rows
        "score": F(64),   # team score numbers
        "label": F(42),   # SUMA label, team labels
        "x":     F(180),  # large X mark
        "small": F(30),   # COFNIJ button, hints
    }


def build_row_string(rank: int, text: str, points) -> str:
    """
    Build a fixed-width row string: "rank text....dots pts"
    points=None means unrevealed (shown as "--").

    Because the font is monospace, every row occupies the same pixel width
    regardless of whether the answer is revealed, so the board never shifts.
    """
    pts = f"{points:>3}" if points is not None else " --"

    rank_str = str(rank)
    if text:
        # space after rank, space before dots
        inner_width = BODY_CHARS - len(rank_str) - 1  # rank + space
        # text + space + dots must fit in inner_width
        dots_count = max(0, inner_width - len(text) - 1)
        body = f"{rank_str} {text} {'.' * dots_count}"
    else:
        dots_count = BODY_CHARS - len(rank_str) - 1
        body = f"{rank_str} {'.' * dots_count}"

    body = body[:BODY_CHARS]  # hard-truncate to prevent overflow
    return f"{body} {pts}"


def draw_background(surface: pygame.Surface) -> None:
    surface.fill(BLACK)


def draw_board_panel(surface: pygame.Surface, state, fonts: dict) -> None:
    # Border
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)
    pygame.draw.rect(surface, GREEN_BORDER, board_rect, 4)

    # 6 answer rows
    round_ = state.rounds[state.round_index]
    for i, ans in enumerate(round_.answers):
        revealed = state.revealed[i]
        text = ans.text if revealed else ""
        points = ans.points if revealed else None
        row_str = build_row_string(ans.rank, text, points)
        surf = fonts["board"].render(row_str, True, GREEN)
        y = BOARD_TOP + ROW_PADDING_TOP + i * ROW_HEIGHT
        surface.blit(surf, (BOARD_LEFT + 20, y + (ROW_HEIGHT - surf.get_height()) // 2))

    # SUMA line
    suma = compute_suma(state)
    suma_surf = fonts["label"].render(f"SUMA  {suma}", True, GREEN)
    suma_rect = suma_surf.get_rect(center=(BOARD_LEFT + BOARD_WIDTH // 2, SUMA_Y))
    surface.blit(suma_surf, suma_rect)


def draw_x_zones(surface: pygame.Surface, state, fonts: dict) -> None:
    for i, rect in enumerate(LEFT_X_ZONES):
        pygame.draw.rect(surface, GREEN_DIM, rect, 2)
        if state.x_left[i]:
            x_surf = fonts["x"].render("X", True, RED)
            surface.blit(x_surf, x_surf.get_rect(center=rect.center))

    for i, rect in enumerate(RIGHT_X_ZONES):
        pygame.draw.rect(surface, GREEN_DIM, rect, 2)
        if state.x_right[i]:
            x_surf = fonts["x"].render("X", True, RED)
            surface.blit(x_surf, x_surf.get_rect(center=rect.center))


def draw_team_scores(surface: pygame.Surface, state, fonts: dict) -> None:
    for rect, label, score in [
        (TEAM1_RECT, "DRUŻYNA 1", state.team1_score),
        (TEAM2_RECT, "DRUŻYNA 2", state.team2_score),
    ]:
        pygame.draw.rect(surface, GREEN_BORDER, rect, 3)
        lbl = fonts["small"].render(label, True, GREEN_DIM)
        surface.blit(lbl, lbl.get_rect(centerx=rect.centerx, top=rect.top + 8))
        scr = fonts["score"].render(str(score), True, GREEN)
        surface.blit(scr, scr.get_rect(center=(rect.centerx, rect.centery + 10)))


def draw_cofnij(surface: pygame.Surface, fonts: dict, history_len: int) -> None:
    color = GREEN if history_len > 0 else GREEN_DIM
    pygame.draw.rect(surface, color, COFNIJ_RECT, 2)
    surf = fonts["small"].render("COFNIJ", True, color)
    surface.blit(surf, surf.get_rect(center=COFNIJ_RECT.center))


def draw_gameover(surface: pygame.Surface, state, fonts: dict) -> None:
    title = fonts["score"].render("KONIEC GRY", True, YELLOW)
    surface.blit(title, title.get_rect(center=(SCREEN_W // 2, 380)))

    t1 = fonts["label"].render(f"DRUŻYNA 1:  {state.team1_score}", True, GREEN)
    t2 = fonts["label"].render(f"DRUŻYNA 2:  {state.team2_score}", True, GREEN)
    surface.blit(t1, t1.get_rect(center=(SCREEN_W // 2, 500)))
    surface.blit(t2, t2.get_rect(center=(SCREEN_W // 2, 580)))

    hint = fonts["small"].render("Kliknij aby zagrać ponownie", True, GREEN_DIM)
    surface.blit(hint, hint.get_rect(center=(SCREEN_W // 2, 700)))


def render_frame(
    surface: pygame.Surface,
    state,
    fonts: dict,
    history_len: int,
) -> None:
    draw_background(surface)
    if state.phase == "gameover":
        draw_gameover(surface, state, fonts)
    else:
        draw_board_panel(surface, state, fonts)
        draw_x_zones(surface, state, fonts)
        draw_team_scores(surface, state, fonts)
    draw_cofnij(surface, fonts, history_len)
    pygame.display.flip()
