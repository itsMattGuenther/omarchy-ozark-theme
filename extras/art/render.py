#!/usr/bin/env python3
"""Regenerate the two terminal artworks. Requires ImageMagick on PATH."""

from pathlib import Path
from collections import Counter
import subprocess
import tomllib


ART = Path(__file__).resolve().parent
PALETTE = tomllib.loads((ART.parents[1] / "colors.toml").read_text())
BACKGROUND = bytes.fromhex(PALETTE["background"].lstrip("#"))
INKS = [bytes.fromhex(PALETTE[key].lstrip("#")) for key in
        ("green", "cyan", "blue", "muted", "orange", "yellow", "magenta")]
ANSI = {bytes.fromhex(PALETTE[key].lstrip("#")): code for key, code in
        (("green", 32), ("cyan", 36), ("blue", 34), ("muted", 90),
         ("yellow", 33), ("magenta", 35))}
# Each Braille cell contains two columns and four rows of dots.
DOTS = ((0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 3),
        (1, 1, 4), (1, 2, 5), (0, 3, 6), (1, 3, 7))


def render(name, columns, rows, compact=False):
    width, height = columns * 2, rows * 4
    pixels = subprocess.run(
        ["magick", "-background", PALETTE["background"], str(ART / f"{name}.svg"),
         "-alpha", "remove", "-alpha", "off", "-resize", f"{width}x{height}!",
         "-colorspace", "sRGB", "-depth", "8", "rgb:-"],
        check=True, capture_output=True,
    ).stdout
    if len(pixels) != width * height * 3:
        raise ValueError(f"Unexpected raster size for {name}")
    # Project onto each ink/background blend so antialiasing does not invent
    # a different hue at the edges. Each cell then chooses its majority ink.
    def nearest(pixel):
        delta = [a - b for a, b in zip(pixel, BACKGROUND)]
        candidates = []
        for ink in ANSI if compact else INKS:
            vector = [a - b for a, b in zip(ink, BACKGROUND)]
            coverage = min(1, max(0, sum(a * b for a, b in zip(delta, vector)) /
                                 sum(a * a for a in vector)))
            error = sum((a - coverage * b) ** 2 for a, b in zip(delta, vector))
            candidates.append((error, coverage, ink))
        _, coverage, ink = min(candidates)
        return ink if coverage >= .42 else BACKGROUND

    dots = [nearest(pixels[i:i + 3]) for i in range(0, len(pixels), 3)]
    lines, coloured_lines = [], []
    for y in range(0, height, 4):
        line, coloured, previous = [], [], None
        for x in range(0, width, 2):
            ink = [(dots[(y + dy) * width + x + dx], bit)
                   for dx, dy, bit in DOTS
                   if dots[(y + dy) * width + x + dx] != BACKGROUND]
            cell = chr(0x2800 + sum(1 << bit for _, bit in ink))
            if ink:
                colour = Counter(rgb for rgb, _ in ink).most_common(1)[0][0]
                if colour != previous:
                    coloured.append(f"\033[{ANSI[colour]}m" if compact else
                                    f"\033[38;2;{colour[0]};{colour[1]};{colour[2]}m")
                    previous = colour
            line.append(cell)
            coloured.append(cell)
        # Preserve blank Braille cells so About measures the full canvas.
        lines.append("".join(line))
        coloured_lines.append("".join(coloured) + "\033[0m")
    (ART / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ART / f"{name}.ansi.txt").write_text("\n".join(coloured_lines) + "\n", encoding="utf-8")
    print(f"{name}.txt: {columns} columns x {rows} rows")


if __name__ == "__main__":
    render("luna-moth", 56, 18)
    render("ozark-ridge", 64, 20, compact=True)
