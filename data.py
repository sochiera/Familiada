import json
import pathlib

from state import Answer, Round


def load_rounds(rounds_dir: str = "rounds") -> list:
    """
    Load all round JSON files from rounds_dir, sorted by filename.
    Each file must follow the format:
        {"answers": [{"rank": 1, "text": "...", "points": 45}, ...]}
    Returns a list of Round objects with exactly 6 answers each.
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
            Answer(rank=a["rank"], text=a["text"].upper(), points=a["points"])
            for a in sorted(raw["answers"], key=lambda x: x["rank"])
        ]
        # Pad to exactly 6 answers if the JSON has fewer
        while len(answers) < 6:
            answers.append(Answer(rank=len(answers) + 1, text="", points=0))
        rounds.append(Round(answers=tuple(answers[:6])))
    return rounds
