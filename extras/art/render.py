#!/usr/bin/env python3
"""Regenerate the two terminal artworks. Requires ImageMagick on PATH."""

from pathlib import Path
import subprocess


ART = Path(__file__).resolve().parent
# Each Braille cell contains two columns and four rows of dots.
DOTS = ((0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 3),
        (1, 1, 4), (1, 2, 5), (0, 3, 6), (1, 3, 7))


def render(name, columns, rows):
    width, height = columns * 2, rows * 4
    pixels = subprocess.run(
        ["magick", "-background", "white", str(ART / f"{name}.svg"),
         "-alpha", "remove", "-alpha", "off", "-resize", f"{width}x{height}!",
         "-colorspace", "Gray", "-depth", "8", "gray:-"],
        check=True, capture_output=True,
    ).stdout
    if len(pixels) != width * height:
        raise ValueError(f"Unexpected raster size for {name}")
    lines = []
    for y in range(0, height, 4):
        line = []
        for x in range(0, width, 2):
            bits = sum(1 << bit for dx, dy, bit in DOTS
                       if pixels[(y + dy) * width + x + dx] < 170)
            line.append(chr(0x2800 + bits))
        # Preserve blank Braille cells so About measures the full canvas.
        lines.append("".join(line))
    (ART / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{name}.txt: {columns} columns x {rows} rows")


if __name__ == "__main__":
    render("hawksbill-crag", 56, 18)
    render("ozark-ridge", 64, 20)
