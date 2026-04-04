from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Answer:
    rank: int
    text: str    # already uppercased by data.py
    points: int


@dataclass(frozen=True)
class Round:
    question: str   # pytanie wyświetlane nad tablicą
    answers: tuple  # tuple of exactly 10 Answer objects


@dataclass(frozen=True)
class GameState:
    rounds:      tuple  # tuple of Round objects (all rounds, never mutated)
    round_index: int
    # 0 = hidden, 1 = word visible (score still hidden), 2 = fully revealed
    revealed:    tuple  # tuple of 10 int
    x_left:      tuple  # tuple of 3 bool — left-side X marks
    x_right:     tuple  # tuple of 3 bool — right-side X marks
    team1_score: int
    team2_score: int
    phase:       str    # "playing" | "gameover"


def make_initial_state(rounds: list) -> GameState:
    return GameState(
        rounds=tuple(rounds),
        round_index=0,
        revealed=(0,) * 10,
        x_left=(False, False, False),
        x_right=(False, False, False),
        team1_score=0,
        team2_score=0,
        phase="playing",
    )


def compute_suma(state: GameState) -> int:
    """Return sum of points for all fully revealed answers (state 2 only)."""
    round_ = state.rounds[state.round_index]
    return sum(
        ans.points
        for ans, rev in zip(round_.answers, state.revealed)
        if rev == 2
    )


def action_reveal_full(state: GameState, row: int) -> GameState:
    """Show both word and score immediately (0 → 2). No-op if already >= 1."""
    if state.revealed[row] >= 1:
        return state
    lst = list(state.revealed)
    lst[row] = 2
    return replace(state, revealed=tuple(lst))


def action_reveal_score(state: GameState, row: int) -> GameState:
    """Show the score for a row whose word is already visible (1 → 2). No-op otherwise."""
    if state.revealed[row] != 1:
        return state
    lst = list(state.revealed)
    lst[row] = 2
    return replace(state, revealed=tuple(lst))


def action_add_x_left(state: GameState, zone: int) -> GameState:
    """Mark left X zone (0-based). No-op if already filled."""
    if state.x_left[zone]:
        return state
    lst = list(state.x_left)
    lst[zone] = True
    return replace(state, x_left=tuple(lst))


def action_add_x_right(state: GameState, zone: int) -> GameState:
    """Mark right X zone (0-based). No-op if already filled."""
    if state.x_right[zone]:
        return state
    lst = list(state.x_right)
    lst[zone] = True
    return replace(state, x_right=tuple(lst))


def action_transfer_to_team(state: GameState, team: int) -> GameState:
    """
    Add current SUMA to team (1 or 2). Advance to next round (clearing the
    board) or switch to gameover phase if no more rounds remain.
    """
    suma = compute_suma(state)
    t1 = state.team1_score + (suma if team == 1 else 0)
    t2 = state.team2_score + (suma if team == 2 else 0)
    next_round = state.round_index + 1

    if next_round >= len(state.rounds):
        return replace(state, team1_score=t1, team2_score=t2, phase="gameover")

    return replace(
        state,
        round_index=next_round,
        revealed=(0,) * 10,
        x_left=(False, False, False),
        x_right=(False, False, False),
        team1_score=t1,
        team2_score=t2,
        phase="playing",
    )
