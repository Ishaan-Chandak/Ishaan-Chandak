"""Render recent listening data as a game-native SVG profile card."""

from __future__ import annotations

import argparse
import html
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


FEED_URL = (
    "https://spotify-recently-played.jeffreyca.workers.dev/svg"
    "?user=scg9tufh3xukyw7w5uwu0xm8y"
)
SVG_NS = "{http://www.w3.org/2000/svg}"


def load_feed(source: str | None) -> bytes:
    if source:
        return Path(source).read_bytes()
    request = urllib.request.Request(FEED_URL, headers={"User-Agent": "Ishaan-Chandak-profile"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def recent_tracks(svg: bytes) -> list[tuple[str, str, str]]:
    root = ET.fromstring(svg)
    tracks: list[tuple[str, str, str]] = []
    for group in root.findall(f"{SVG_NS}g"):
        title = group.find(f"{SVG_NS}title")
        if title is None or not title.text or "\nby " not in title.text:
            continue
        lines = title.text.splitlines()
        name = lines[0].strip()
        artist = lines[1].removeprefix("by ").strip()
        link = group.find(f"{SVG_NS}a")
        href = link.get("href", "https://open.spotify.com/") if link is not None else "https://open.spotify.com/"
        tracks.append((name, artist, href))
    if not tracks:
        raise RuntimeError("No recent tracks found in listening feed")
    return tracks[:5]


def short(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def render(tracks: list[tuple[str, str, str]]) -> str:
    rows = []
    for index, (name, artist, href) in enumerate(tracks, start=1):
        y = 121 + (index - 1) * 55
        state = "NOW EQUIPPED" if index == 1 else f"SLOT {index:02d}"
        color = "#F7C948" if index == 1 else "#73849A"
        bars = "".join(
            f'<rect x="{1045 + n * 12}" y="{y - (8 + ((index + n) % 3) * 5)}" width="6" height="{12 + ((index + n) % 3) * 5}" rx="3" fill="#35D0BA" opacity="{1 - n * .12:.2f}"/>'
            for n in range(5)
        )
        rows.append(
            f'''<a href="{html.escape(href, quote=True)}" target="_blank">
  <rect x="49" y="{y - 34}" width="1102" height="46" rx="8" fill="#0D1C2D" stroke="#23445A"/>
  <text x="70" y="{y - 6}" fill="{color}" font-size="13">{state}</text>
  <text x="220" y="{y - 7}" fill="#FFFFFF" font-size="17" font-weight="700">{html.escape(short(name, 42))}</text>
  <text x="690" y="{y - 7}" fill="#C9D7E5" font-size="14">// {html.escape(short(artist, 37))}</text>
  {bars}
</a>'''
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="395" viewBox="0 0 1200 395" role="img" aria-labelledby="title desc">
<title id="title">Loot Radio - recent quest soundtrack</title>
<desc id="desc">Five recently played tracks rendered as game inventory slots.</desc>
<defs>
  <linearGradient id="bg" x1="0" x2="1"><stop stop-color="#08111F"/><stop offset="1" stop-color="#102A3C"/></linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#35D0BA" stroke-opacity=".035"/></pattern>
</defs>
<rect width="1200" height="395" rx="20" fill="url(#bg)"/>
<rect width="1200" height="395" rx="20" fill="url(#grid)" stroke="#23445A" stroke-width="2"/>
<g font-family="Consolas,monospace">
  <circle cx="31" cy="27" r="6" fill="#FF6B6B"/><circle cx="51" cy="27" r="6" fill="#F7C948"/><circle cx="71" cy="27" r="6" fill="#35D0BA"/>
  <text x="600" y="32" text-anchor="middle" fill="#73849A" font-size="13">LOOT_RADIO.EXE // AUDIO INVENTORY</text>
  <path d="M24 51h1152" stroke="#23445A"/>
  <text x="49" y="75" fill="#35D0BA" font-size="13" letter-spacing="3">RECENT AUDIO DROPS</text>
  <text x="1151" y="75" text-anchor="end" fill="#73849A" font-size="12">AUTO-SYNC: ONLINE</text>
  {''.join(rows)}
  <text x="49" y="374" fill="#73849A" font-size="12">♪ MUSIC BUFF ACTIVE</text>
  <text x="1151" y="374" text-anchor="end" fill="#35D0BA" font-size="12">5 TRACKS LOADED</text>
</g>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Local source SVG, used for tests")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(recent_tracks(load_feed(args.source))), encoding="utf-8")


if __name__ == "__main__":
    main()
