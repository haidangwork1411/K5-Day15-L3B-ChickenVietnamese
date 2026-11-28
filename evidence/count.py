"""Recompute descriptive counts from the anonymized, coded snapshot (stdlib)."""
import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


def calculate(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows, "No coded observations"
    assert len({row["source_id"] for row in rows}) == len(rows), "Duplicate review IDs"
    assert len({row["evidence_id"] for row in rows}) == len(rows)
    for row in rows:
        for label in ("missing_food", "complaint_difficulty"):
            assert row[label] in ("0", "1"), (row["evidence_id"], label)
        assert row["coding_note"], row["evidence_id"]
        assert 1 <= int(row["stars"]) <= 5
        datetime.fromisoformat(row["review_date"])
        datetime.fromisoformat(row["collected_at"])
        assert row["source_url"].startswith("https://itunes.apple.com/vn/rss/customerreviews/")
        words = [w for w in row["excerpt"].split() if w != "[…]" and not w.startswith("[không")]
        assert len(words) <= 25, row["evidence_id"]
        assert not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", row["excerpt"])
        assert not re.search(r"(?<!\d)(?:0|\+84)\d{8,10}(?!\d)", row["excerpt"])
        assert len(row["content_sha256"]) == 64
    total = len(rows)
    values = {
        "missing_food": sum(int(row["missing_food"]) for row in rows),
        "complaint_difficulty": sum(int(row["complaint_difficulty"]) for row in rows),
        "both": sum(row["missing_food"] == "1" and row["complaint_difficulty"] == "1" for row in rows),
    }
    return {"N": total, "unit": "public review excerpts, not users or orders",
        "counts": {label: {"x": count, "N": total, "percent": round(count * 100 / total, 2)} for label, count in values.items()},
        "star_distribution": dict(sorted(Counter(row["stars"] for row in rows).items())),
        "review_date_min": min(row["review_date"] for row in rows),
        "review_date_max": max(row["review_date"] for row in rows),
        "coded_by": "AI-assisted excerpt coding; human review pending",
        "snapshot_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "public-reviews/reviews.csv")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = calculate(args.input)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf8")
    print(text)


if __name__ == "__main__":
    main()
