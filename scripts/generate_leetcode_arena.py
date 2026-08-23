"""Generate self-updating LeetCode game panels for the profile README."""

from __future__ import annotations

import argparse
import html
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


USERNAME = "Ishaan_Chandak"
ENDPOINT = "https://leetcode.com/graphql/"
QUERY = """
query profileArena($username: String!, $limit: Int!) {
  matchedUser(username: $username) {
    profile { ranking }
    submitStatsGlobal { acSubmissionNum { difficulty count } }
    tagProblemCounts {
      advanced { tagName problemsSolved }
      intermediate { tagName problemsSolved }
      fundamental { tagName problemsSolved }
    }
  }
  recentAcSubmissionList(username: $username, limit: $limit) {
    title titleSlug timestamp
  }
}
"""


def fetch() -> dict:
    payload = json.dumps(
        {"query": QUERY, "variables": {"username": USERNAME, "limit": 12}}
    ).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Ishaan-profile"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]


def fill(template: Path, replacements: dict[str, object]) -> str:
    value = template.read_text(encoding="utf-8")
    for key, replacement in replacements.items():
        value = value.replace("{{" + key + "}}", html.escape(str(replacement)))
    if "{{" in value:
        raise RuntimeError(f"Unfilled template value in {template}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    data = fetch()
    user = data["matchedUser"]
    solved = {item["difficulty"]: item["count"] for item in user["submitStatsGlobal"]["acSubmissionNum"]}
    largest = max(solved.get("Easy", 0), solved.get("Medium", 0), solved.get("Hard", 0), 1)
    sync = datetime.now(timezone.utc).strftime("%d %b %Y").upper()

    overview = {
        "RANK": f'{user["profile"]["ranking"]:,}',
        "TOTAL": solved.get("All", 0),
        "EASY": solved.get("Easy", 0),
        "MEDIUM": solved.get("Medium", 0),
        "HARD": solved.get("Hard", 0),
        "EASY_W": round(240 * solved.get("Easy", 0) / largest),
        "MEDIUM_W": round(240 * solved.get("Medium", 0) / largest),
        "HARD_W": round(240 * solved.get("Hard", 0) / largest),
        "SYNC": sync,
    }
    (output / "arena-leetcode.svg").write_text(
        fill(root / "assets/arena-leetcode.svg", overview), encoding="utf-8"
    )

    tags = {}
    for level in user["tagProblemCounts"].values():
        tags.update({item["tagName"]: item["problemsSolved"] for item in level})
    topic_values = {
        "ARRAY": tags.get("Array", 0),
        "HASH": tags.get("Hash Table", 0),
        "STRING": tags.get("String", 0),
        "SORTING": tags.get("Sorting", 0),
        "DFS": tags.get("Depth-First Search", 0),
        "DP": tags.get("Dynamic Programming", 0),
        "MATH": tags.get("Math", 0),
        "BFS": tags.get("Breadth-First Search", 0),
        "SYNC": sync,
    }
    (output / "arena-topics.svg").write_text(
        fill(root / "assets/arena-topics.svg", topic_values), encoding="utf-8"
    )

    unique = []
    seen = set()
    for item in data["recentAcSubmissionList"]:
        if item["titleSlug"] in seen:
            continue
        seen.add(item["titleSlug"])
        unique.append(item)
        if len(unique) == 5:
            break
    recent_values: dict[str, object] = {"SYNC": sync}
    for index in range(5):
        item = unique[index] if index < len(unique) else None
        title = item["title"] if item else "NO ENCOUNTER DATA"
        if len(title) > 76:
            title = title[:75].rstrip() + "…"
        date = (
            datetime.fromtimestamp(int(item["timestamp"]), timezone.utc).strftime("%d %b")
            if item
            else "--"
        )
        recent_values[f"RECENT_{index + 1}"] = title
        recent_values[f"DATE_{index + 1}"] = date.upper()
    (output / "arena-recent.svg").write_text(
        fill(root / "assets/arena-recent.svg", recent_values), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
