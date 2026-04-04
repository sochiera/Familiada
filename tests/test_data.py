"""Unit tests for data.py — TDD cycles."""
import json
import pytest
from data import load_rounds
from state import Answer, Round


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_round(tmp_path, filename, pytanie, odpowiedzi):
    f = tmp_path / filename
    f.write_text(
        json.dumps({"pytanie": pytanie, "odpowiedzi": odpowiedzi}, ensure_ascii=False),
        encoding="utf-8",
    )
    return f


# ---------------------------------------------------------------------------
# Cykl 11: podstawowe ładowanie
# ---------------------------------------------------------------------------

def test_load_single_round(tmp_path):
    write_round(tmp_path, "round01.json", "Pytanie testowe", [
        {"odpowiedz": "Chleb", "punkty": 35},
        {"odpowiedz": "Ryba",  "punkty": 20},
    ])
    rounds = load_rounds(str(tmp_path))
    assert len(rounds) == 1


def test_loaded_round_has_correct_question(tmp_path):
    write_round(tmp_path, "round01.json", "Pytanie testowe", [
        {"odpowiedz": "Chleb", "punkty": 35},
    ])
    rounds = load_rounds(str(tmp_path))
    assert rounds[0].question == "Pytanie testowe"


def test_loaded_round_has_correct_answer_count(tmp_path):
    write_round(tmp_path, "round01.json", "Q", [
        {"odpowiedz": "Chleb", "punkty": 35},
        {"odpowiedz": "Ryba",  "punkty": 20},
        {"odpowiedz": "Wino",  "punkty": 10},
    ])
    rounds = load_rounds(str(tmp_path))
    assert len(rounds[0].answers) == 3


def test_loaded_answers_have_correct_points(tmp_path):
    write_round(tmp_path, "round01.json", "Q", [
        {"odpowiedz": "Chleb", "punkty": 35},
        {"odpowiedz": "Ryba",  "punkty": 20},
    ])
    rounds = load_rounds(str(tmp_path))
    assert rounds[0].answers[0].points == 35
    assert rounds[0].answers[1].points == 20


# ---------------------------------------------------------------------------
# Cykl 12: tekst auto-uppercase
# ---------------------------------------------------------------------------

def test_answer_text_is_uppercased(tmp_path):
    write_round(tmp_path, "round01.json", "Q", [
        {"odpowiedz": "chleb", "punkty": 10},
    ])
    rounds = load_rounds(str(tmp_path))
    assert rounds[0].answers[0].text == "CHLEB"


def test_answer_text_already_upper_stays_upper(tmp_path):
    write_round(tmp_path, "round01.json", "Q", [
        {"odpowiedz": "MIÓD", "punkty": 5},
    ])
    rounds = load_rounds(str(tmp_path))
    assert rounds[0].answers[0].text == "MIÓD"


# ---------------------------------------------------------------------------
# Cykl 13: rank przypisany poprawnie
# ---------------------------------------------------------------------------

def test_answer_rank_starts_at_1(tmp_path):
    write_round(tmp_path, "round01.json", "Q", [
        {"odpowiedz": "A", "punkty": 10},
        {"odpowiedz": "B", "punkty": 5},
    ])
    rounds = load_rounds(str(tmp_path))
    assert rounds[0].answers[0].rank == 1
    assert rounds[0].answers[1].rank == 2


# ---------------------------------------------------------------------------
# Cykl 14: wiele rund w kolejności alfabetycznej
# ---------------------------------------------------------------------------

def test_multiple_rounds_loaded_in_order(tmp_path):
    write_round(tmp_path, "round02.json", "Druga", [{"odpowiedz": "X", "punkty": 1}])
    write_round(tmp_path, "round01.json", "Pierwsza", [{"odpowiedz": "Y", "punkty": 2}])
    rounds = load_rounds(str(tmp_path))
    assert len(rounds) == 2
    assert rounds[0].question == "Pierwsza"
    assert rounds[1].question == "Druga"


# ---------------------------------------------------------------------------
# Cykl 15: błąd gdy brak plików
# ---------------------------------------------------------------------------

def test_empty_directory_raises(tmp_path):
    with pytest.raises(ValueError, match="No round JSON files"):
        load_rounds(str(tmp_path))


# ---------------------------------------------------------------------------
# Cykl 15b: maksymalnie 11 odpowiedzi
# ---------------------------------------------------------------------------

def test_answers_capped_at_11(tmp_path):
    odpowiedzi = [{"odpowiedz": f"ODP{i}", "punkty": i} for i in range(15)]
    write_round(tmp_path, "round01.json", "Q", odpowiedzi)
    rounds = load_rounds(str(tmp_path))
    assert len(rounds[0].answers) == 11
