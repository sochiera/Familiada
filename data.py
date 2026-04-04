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
    Answers are taken in order, up to 10. No blank padding.
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
        rounds.append(Round(
            question=raw.get("pytanie", ""),
            answers=tuple(answers[:10]),
        ))
    return rounds
