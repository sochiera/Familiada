"""Unit tests for state.py — TDD cycles."""
import pytest
from state import (
    Answer, Round, GameState,
    make_initial_state,
    compute_suma,
    action_reveal_full,
    action_reveal_score,
    action_add_x_left,
    action_add_x_right,
    action_transfer_to_team,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_answer(rank=1, text="CHLEB", points=10):
    return Answer(rank=rank, text=text, points=points)


def make_round(n_answers=6):
    answers = tuple(
        Answer(rank=i + 1, text=f"ODP{i+1}", points=(6 - i) * 10)
        for i in range(n_answers)
    )
    return Round(question="Pytanie testowe", answers=answers)


def make_state(n_rounds=2, n_answers=6):
    rounds = [make_round(n_answers) for _ in range(n_rounds)]
    return make_initial_state(rounds)


# ---------------------------------------------------------------------------
# Cykl 1: make_initial_state
# ---------------------------------------------------------------------------

def test_initial_state_round_index_is_zero():
    state = make_state()
    assert state.round_index == 0


def test_initial_state_all_hidden():
    state = make_state()
    assert all(r == 0 for r in state.revealed)


def test_initial_state_no_x_marks():
    state = make_state()
    assert state.x_left == (False, False, False)
    assert state.x_right == (False, False, False)


def test_initial_state_scores_zero():
    state = make_state()
    assert state.team1_score == 0
    assert state.team2_score == 0


def test_initial_state_phase_playing():
    state = make_state()
    assert state.phase == "playing"


def test_initial_state_rounds_stored():
    rounds = [make_round()]
    state = make_initial_state(rounds)
    assert len(state.rounds) == 1


# ---------------------------------------------------------------------------
# Cykl 2: compute_suma — brak odkrytych
# ---------------------------------------------------------------------------

def test_suma_zero_when_nothing_revealed():
    state = make_state()
    assert compute_suma(state) == 0


# ---------------------------------------------------------------------------
# Cykl 3: compute_suma — tylko stan 2 liczy się do sumy
# ---------------------------------------------------------------------------

def test_suma_counts_only_state_2():
    """State 1 (word visible, score hidden) should NOT be counted."""
    state = make_state()
    # Manually set revealed[0]=1 (word only) and revealed[1]=2 (full)
    from dataclasses import replace
    state = replace(state, revealed=(1, 2) + (0,) * 9)
    round_ = state.rounds[0]
    expected = round_.answers[1].points   # only index 1 (state 2)
    assert compute_suma(state) == expected


def test_suma_all_revealed():
    state = make_state(n_answers=6)
    from dataclasses import replace
    state = replace(state, revealed=(2,) * 6 + (0,) * 5)
    total = sum(a.points for a in state.rounds[0].answers)
    assert compute_suma(state) == total


# ---------------------------------------------------------------------------
# Cykl 4: action_reveal_full
# ---------------------------------------------------------------------------

def test_reveal_full_sets_state_2():
    state = make_state()
    new = action_reveal_full(state, 0)
    assert new.revealed[0] == 2


def test_reveal_full_noop_if_word_visible():
    """Row already in state 1 (word only) — should NOT change."""
    from dataclasses import replace
    state = make_state()
    state = replace(state, revealed=(1,) + (0,) * 10)
    same = action_reveal_full(state, 0)
    assert same is state


def test_reveal_full_noop_if_already_full():
    from dataclasses import replace
    state = make_state()
    state = replace(state, revealed=(2,) + (0,) * 10)
    same = action_reveal_full(state, 0)
    assert same is state


def test_reveal_full_only_changes_target_row():
    state = make_state()
    new = action_reveal_full(state, 2)
    assert new.revealed[2] == 2
    assert all(new.revealed[i] == 0 for i in range(11) if i != 2)


def test_reveal_full_returns_new_object():
    state = make_state()
    new = action_reveal_full(state, 0)
    assert new is not state


# ---------------------------------------------------------------------------
# Cykl 5: action_reveal_score
# ---------------------------------------------------------------------------

def test_reveal_score_1_to_2():
    from dataclasses import replace
    state = make_state()
    state = replace(state, revealed=(1,) + (0,) * 10)
    new = action_reveal_score(state, 0)
    assert new.revealed[0] == 2


def test_reveal_score_noop_if_hidden():
    state = make_state()   # all zeros
    same = action_reveal_score(state, 0)
    assert same is state


def test_reveal_score_noop_if_already_2():
    from dataclasses import replace
    state = make_state()
    state = replace(state, revealed=(2,) + (0,) * 10)
    same = action_reveal_score(state, 0)
    assert same is state


# ---------------------------------------------------------------------------
# Cykl 6: action_add_x_left
# ---------------------------------------------------------------------------

def test_x_left_sets_zone():
    state = make_state()
    new = action_add_x_left(state, 1)
    assert new.x_left == (False, True, False)


def test_x_left_noop_if_already_set():
    from dataclasses import replace
    state = make_state()
    state = replace(state, x_left=(False, True, False))
    same = action_add_x_left(state, 1)
    assert same is state


def test_x_left_does_not_touch_other_zones():
    state = make_state()
    new = action_add_x_left(state, 0)
    assert new.x_left[1] is False
    assert new.x_left[2] is False


# ---------------------------------------------------------------------------
# Cykl 7: action_add_x_right
# ---------------------------------------------------------------------------

def test_x_right_sets_zone():
    state = make_state()
    new = action_add_x_right(state, 2)
    assert new.x_right == (False, False, True)


def test_x_right_noop_if_already_set():
    from dataclasses import replace
    state = make_state()
    state = replace(state, x_right=(False, False, True))
    same = action_add_x_right(state, 2)
    assert same is state


# ---------------------------------------------------------------------------
# Cykl 8: action_transfer_to_team — punkty trafiają do drużyny
# ---------------------------------------------------------------------------

def _state_with_revealed(points_per_answer=10, n_answers=3, n_rounds=2):
    """Helper: 2-rund state with first n_answers fully revealed."""
    answers = tuple(
        Answer(rank=i + 1, text=f"ODP{i+1}", points=points_per_answer)
        for i in range(n_answers)
    )
    round_ = Round(question="Q", answers=answers)
    from dataclasses import replace as dc_replace
    state = make_initial_state([round_] * n_rounds)
    revealed = (2,) * n_answers + (0,) * (11 - n_answers)
    return dc_replace(state, revealed=revealed)


def test_transfer_adds_suma_to_team1():
    state = _state_with_revealed(points_per_answer=10, n_answers=3)
    new = action_transfer_to_team(state, 1)
    assert new.team1_score == 30
    assert new.team2_score == 0


def test_transfer_adds_suma_to_team2():
    state = _state_with_revealed(points_per_answer=10, n_answers=3)
    new = action_transfer_to_team(state, 2)
    assert new.team2_score == 30
    assert new.team1_score == 0


def test_transfer_accumulates_scores_across_rounds():
    state = _state_with_revealed(points_per_answer=10, n_answers=3, n_rounds=2)
    # Round 0 → team1 gets 30
    state = action_transfer_to_team(state, 1)
    # Round 1 — same answers but from dataclass replace, revealed already reset
    from dataclasses import replace as dc_replace
    state = dc_replace(state, revealed=(2,) * 3 + (0,) * 8)
    state = action_transfer_to_team(state, 1)
    assert state.team1_score == 60


# ---------------------------------------------------------------------------
# Cykl 9: action_transfer_to_team — board reset i awans rundy
# ---------------------------------------------------------------------------

def test_transfer_advances_round():
    state = _state_with_revealed()
    new = action_transfer_to_team(state, 1)
    assert new.round_index == 1


def test_transfer_resets_revealed():
    state = _state_with_revealed()
    new = action_transfer_to_team(state, 1)
    assert all(r == 0 for r in new.revealed)


def test_transfer_resets_x_marks():
    from dataclasses import replace as dc_replace
    state = _state_with_revealed()
    state = dc_replace(state, x_left=(True, True, False), x_right=(False, True, True))
    new = action_transfer_to_team(state, 1)
    assert new.x_left == (False, False, False)
    assert new.x_right == (False, False, False)


# ---------------------------------------------------------------------------
# Cykl 10: action_transfer_to_team — game over po ostatniej rundzie
# ---------------------------------------------------------------------------

def test_transfer_last_round_triggers_gameover():
    state = _state_with_revealed(n_rounds=1)
    new = action_transfer_to_team(state, 1)
    assert new.phase == "gameover"


def test_transfer_not_last_round_stays_playing():
    state = _state_with_revealed(n_rounds=2)
    new = action_transfer_to_team(state, 1)
    assert new.phase == "playing"


def test_transfer_gameover_keeps_final_scores():
    state = _state_with_revealed(points_per_answer=15, n_answers=2, n_rounds=1)
    new = action_transfer_to_team(state, 2)
    assert new.team2_score == 30
    assert new.phase == "gameover"
