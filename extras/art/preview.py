#!/usr/bin/env python3
"""Render the actual ANSI text to docs/preview-art.png using ImageMagick."""

from pathlib import Path
import re
import subprocess
import tempfile
from xml.sax.saxutils import escape
from render import ANSI


ART = Path(__file__).resolve().parent
ROOT = ART.parents[1]
SGR = re.compile(r"\033\[([0-9;]*)m")


def panel(name, title, subtitle, offset):
    elements = [
        f'<text x="{offset}" y="40" fill="#e2dee8" font-size="20">{title}</text>',
        f'<text x="{offset}" y="66" fill="#9990b0" font-size="14">{subtitle}</text>',
    ]
    for row, line in enumerate((ART / f"{name}.ansi.txt").read_text().splitlines()):
        column, start, colour = 0, 0, "#ef9268"
        for match in [*SGR.finditer(line), None]:
            end = match.start() if match else len(line)
            run = line[start:end]
            if run:
                elements.append(
                    f'<text x="{offset + column * 12}" y="{110 + row * 26}" '
                    f'fill="{colour}" font-size="20">{escape(run)}</text>')
                column += len(run)
            if match:
                codes = match.group(1).split(";")
                if codes[:2] == ["38", "2"]:
                    colour = "#" + "".join(f"{int(c):02x}" for c in codes[2:])
                elif len(codes) == 1 and codes[0] != "0":
                    colour = "#" + next(rgb.hex() for rgb, code in ANSI.items()
                                         if code == int(codes[0]))
                start = match.end()
    return elements


if __name__ == "__main__":
    elements = panel("luna-moth", "NIGHT FLIGHT", "Luna moth / terminal greeting", 40)
    elements += panel("ozark-ridge", "BLUE HOUR", "Ozark hollows / About screen", 768)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1576" height="644">'
           '<rect width="1576" height="644" fill="#171525"/>'
           '<g font-family="JetBrainsMono Nerd Font">' + "".join(elements) + '</g></svg>')
    output = ROOT / "docs/preview-art.png"
    with tempfile.TemporaryDirectory(prefix="ozark-preview-") as directory:
        source = Path(directory) / "preview.svg"
        source.write_text(svg)
        subprocess.run(["magick", str(source), "-strip", str(output)], check=True)
    print(output)
