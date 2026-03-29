from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Answer:
    rank: int
    text: str    # already uppercased by data.py
    points: int


@dataclass(frozen=True)
class Round:
    answers: tuple  # tuple of exactly 6 Answer objects


@dataclass(frozen=True)
class GameState:
    rounds:      tuple  # tuple of Round objects (all rounds, never mutated)
    round_index: int
    revealed:    tuple  # tuple of 6 bool — True means answer is shown
    x_left:      tuple  # tuple of 3 bool — left-side X marks
    x_right:     tuple  # tuple of 3 bool — right-side X marks
    team1_score: int
    team2_score: int
    phase:       str    # "playing" | "gameover"


def make_initial_state(rounds: list) -> GameState:
    return GameState(
        rounds=tuple(rounds),
        round_index=0,
        revealed=(False,) * 6,
        x_left=(False, False, False),
        x_right=(False, False, False),
        team1_score=0,
        team2_score=0,
        phase="playing",
    )


def compute_suma(state: GameState) -> int:
    """Return sum of points for all currently revealed answers."""
    round_ = state.rounds[state.round_index]
    return sum(
        ans.points
        for ans, rev in zip(round_.answers, state.revealed)
        if rev
    )


def action_reveal_answer(state: GameState, row: int) -> GameState:
    """Reveal answer at row (0-based). No-op if already revealed."""
    if state.revealed[row]:
        return state
    lst = list(state.revealed)
    lst[row] = True
    return replace(state, revealed=tuple(lst))


def action_add_x_left(state: GameState, zone: int) -> GameState:
    """Mark left X zone zone (0-based). No-op if already filled."""
    if state.x_left[zone]:
        return state
    lst = list(state.x_left)
    lst[zone] = True
    return replace(state, x_left=tuple(lst))


def action_add_x_right(state: GameState, zone: int) -> GameState:
    """Mark right X zone zone (0-based). No-op if already filled."""
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
        revealed=(False,) * 6,
        x_left=(False, False, False),
        x_right=(False, False, False),
        team1_score=t1,
        team2_score=t2,
        phase="playing",
    )
