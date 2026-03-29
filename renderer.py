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

# Total character width of the "rank + text/dots" portion (monospace).
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
        "x":     F(200),  # large X — will be scaled down to fit the box
        "small": F(30),   # COFNIJ button, hints
    }


def build_row_string(rank: int, text: str, reveal_state: int, points: int) -> str:
    """
    Build a fixed-width row string.
    reveal_state: 0 = hidden, 1 = word visible (score hidden), 2 = fully revealed.

    Because the font is monospace, every row occupies the same pixel width
    regardless of content, so the board never shifts.
    """
    pts = f"{points:>3}" if reveal_state == 2 else " --"
    display_text = text if reveal_state >= 1 else ""

    rank_str = str(rank)
    if display_text:
        dots_count = max(0, BODY_CHARS - len(rank_str) - 1 - len(display_text) - 1)
        body = f"{rank_str} {display_text} {'.' * dots_count}"
    else:
        dots_count = BODY_CHARS - len(rank_str) - 1
        body = f"{rank_str} {'.' * dots_count}"

    body = body[:BODY_CHARS]  # hard-truncate
    return f"{body} {pts}"


def _draw_x_in_rect(surface: pygame.Surface, rect: pygame.Rect, fonts: dict) -> None:
    """Render a large X scaled to fit inside rect with a small margin."""
    x_surf = fonts["x"].render("X", True, RED)
    margin = 16
    max_w = rect.width - margin
    max_h = rect.height - margin
    scale = min(max_w / x_surf.get_width(), max_h / x_surf.get_height())
    new_w = max(1, int(x_surf.get_width() * scale))
    new_h = max(1, int(x_surf.get_height() * scale))
    scaled = pygame.transform.smoothscale(x_surf, (new_w, new_h))
    surface.blit(scaled, scaled.get_rect(center=rect.center))


def draw_background(surface: pygame.Surface) -> None:
    surface.fill(BLACK)


def draw_board_panel(surface: pygame.Surface, state, fonts: dict) -> None:
    # Border
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)
    pygame.draw.rect(surface, GREEN_BORDER, board_rect, 4)

    # 6 answer rows
    round_ = state.rounds[state.round_index]
    for i, ans in enumerate(round_.answers):
        rev = state.revealed[i]  # 0, 1, or 2
        row_str = build_row_string(ans.rank, ans.text, rev, ans.points)
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
            _draw_x_in_rect(surface, rect, fonts)

    for i, rect in enumerate(RIGHT_X_ZONES):
        pygame.draw.rect(surface, GREEN_DIM, rect, 2)
        if state.x_right[i]:
            _draw_x_in_rect(surface, rect, fonts)


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
