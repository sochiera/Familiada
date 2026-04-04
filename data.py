import json
import pathlib

from state import Answer, Round


def load_rounds(rounds_dir: str = "rounds") -> list:
    """
    Load all round JSON files from rounds_dir, sorted by filename.
    Each file must follow the format:
        {
          "pytanie": "...",
          "odpowiedzi": [{"odpowiedz": "...", "punkty": 45}, ...]
        }
    Answers are taken in order; padded with blanks if fewer than 6.
    Only the first 6 answers are shown on the board.
    """
    p = pathlib.Path(rounds_dir)
    files = sorted(p.glob("round*.json"))
    if not files:
        raise ValueError(f"No round JSON files found in '{rounds_dir}/'. "
                         "Create at least one file named round01.json.")
    rounds = []
    for f in files:
        raw = json.loads(f.read_text(encoding="utf-8"))
        answers = [
            Answer(rank=i + 1, text=a["odpowiedz"].upper(), points=a["punkty"])
            for i, a in enumerate(raw["odpowiedzi"])
        ]
        # Pad to exactly 6 answers if the JSON has fewer
        while len(answers) < 6:
            answers.append(Answer(rank=len(answers) + 1, text="", points=0))
        rounds.append(Round(
            question=raw.get("pytanie", ""),
            answers=tuple(answers[:6]),
        ))
    return rounds
