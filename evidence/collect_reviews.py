"""Collect a bounded public review sample, omitting authors and raw responses."""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import time
import unicodedata
import urllib.request

BANGKOK = timezone(timedelta(hours=7))


def normalize(text):
    return " ".join(unicodedata.normalize("NFC", text).lower().split())


def redact(text):
    text = re.sub(r"https?://\S+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[đã ẩn liên hệ]", text)
    text = re.sub(r"(?<!\w)(?:\+?84|0)[\d .-]{8,14}(?!\w)", "[đã ẩn số]", text)
    return text


def excerpt(text):
    # One sentence, no more than 25 whitespace-delimited words per review.
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    interesting = [s for s in sentences if re.search(r"thiếu|khiếu nại|hỗ trợ|hoàn tiền|cskh|giao sai|sai món|chậm|trễ", s, re.I)]
    selected = (interesting or sentences)[0]
    words = redact(selected).split()
    if len(words) <= 25:
        return " ".join(words)
    match = re.search(r"thiếu|khiếu nại|hỗ trợ|hoàn tiền|cskh|giao sai|sai món|chậm|trễ", selected, re.I)
    offset = max(0, len(selected[:match.start()].split()) - 5) if match else 0
    return ("[…] " if offset else "") + " ".join(words[offset:offset + 25]) + " […]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--app-id", default="1137866760")
    parser.add_argument("--pages", type=int, default=4)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    destination = args.output / "reviews.csv"
    if destination.exists():
        raise SystemExit("Refusing to replace an existing sample")
    rows, pages, seen = [], [], set()
    collected = datetime.now(BANGKOK).isoformat()
    duplicates = blank = 0
    for page in range(1, args.pages + 1):
        url = f"https://itunes.apple.com/vn/rss/customerreviews/page={page}/id={args.app_id}/sortby=mostrecent/json"
        request = urllib.request.Request(url, headers={"User-Agent": "ResearchEvidence/1.0 (public RSS; educational sample)"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
        data = json.loads(body)
        entries = [x for x in data["feed"].get("entry", []) if "im:rating" in x]
        pages.append({"page": page, "url": url, "returned_reviews": len(entries),
                      "response_sha256": hashlib.sha256(body).hexdigest(), "fetched_at": datetime.now(BANGKOK).isoformat()})
        for entry in entries:
            source_id = entry["id"]["label"]
            if source_id in seen:
                duplicates += 1
                continue
            seen.add(source_id)
            content = entry.get("content", {}).get("label", "").strip()
            if not content:
                blank += 1
                continue
            lower = normalize(content)
            rows.append({"evidence_id": f"RV{len(rows) + 1:03d}", "source_id": source_id,
                "review_date": entry["updated"]["label"], "collected_at": collected,
                "stars": entry["im:rating"]["label"], "source_url": url,
                "content_sha256": hashlib.sha256(content.encode("utf8")).hexdigest(),
                "excerpt": excerpt(content),
                "missing_food_candidate": int(bool(re.search(r"thiếu (?:món|đồ|nước|đồ ăn|thức ăn)|giao thiếu|đồ.*thiếu món", lower))),
                "support_candidate": int(bool(re.search(r"khiếu nại|hỗ trợ|cskh|chăm sóc khách|hoàn tiền|bồi thường|phản ánh", lower))),
                "wrong_food_candidate": int(bool(re.search(r"sai món|giao sai|không đúng món", lower))),
                "late_candidate": int(bool(re.search(r"giao (?:trễ|chậm)|giao hàng lâu|chờ.*(?:phút|tiếng)|đợi.*(?:phút|tiếng)", lower))),
                "missing_food": "", "complaint_difficulty": "", "coding_note": ""})
        time.sleep(0.5)
    with destination.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = {"collected_at": collected, "app_id": args.app_id, "storefront": "vn",
        "sort": "mostrecent", "planned_pages": args.pages, "pages": pages,
        "eligible_unique_reviews": len(rows), "duplicates_excluded": duplicates,
        "blank_excluded": blank, "privacy": "author/title/raw payload deliberately not stored; excerpts <=25 source words and one sentence"}
    (args.output / "collection.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps({"reviews": len(rows), "duplicates": duplicates, "pilot": [
        {k: row[k] for k in ("evidence_id", "stars", "excerpt", "missing_food_candidate", "support_candidate")}
        for row in rows[:30]]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
