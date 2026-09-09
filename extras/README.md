# Extras

Things Omarchy cannot install from a theme repo, so `install.sh` puts them in
place (and `install.sh --uninstall` takes them out again):

- `cliamp/ozark.toml` — music player theme
- `art/luna-moth.ansi.txt` — Night Flight, printed when a terminal opens
- `art/ozark-ridge.ansi.txt` — Blue Hour, dropped into Omarchy's About logo slot
  (`~/.config/omarchy/branding/about.txt`) so Omarchy sizes the About window
  to fit it
- `art/luna-moth.txt`, `art/ozark-ridge.txt` — monochrome versions
- `art/*.svg` — the editable vector sources
- `art/render.py` — regenerates plain and ANSI text from the SVG sources
- `art/preview.py` — renders the color text to `docs/preview-art.png`
- `greeting.sh` — prints the moth, only while this theme is active
- `../hooks/ozark-theme-set.sh` — switches cliamp and the About logo with the
  theme. Named after the theme on purpose: `omarchy hook install` copies by
  basename, so a hook called `theme-set.sh` would overwrite another theme's.

## Redrawing the art

Both pieces come from the SVGs in `art/`. The drawings use theme colors for
dots and the theme background for open space. To regenerate, with Python 3.11+ and
ImageMagick installed, run from the repository root:

```bash
python3 extras/art/render.py
python3 extras/art/preview.py
```

Night Flight stays at 56 columns by 18 rows and Blue Hour at 64 columns by 20
rows. Each Braille cell uses the dominant ink among its eight dots. Antialiased
edges retain their ink hue, and blank cells preserve the full canvas width.

The moth uses true color; About uses short ANSI codes that pick up the active
Ozark terminal palette. Omarchy counts the printable parts of these escape
codes when sizing its window, so short codes avoid excessive extra width.
Every color line ends with a reset. The greeting uses the plain text version
when `NO_COLOR` is nonempty. Preview rendering also needs JetBrainsMono Nerd Font.

Run `extras/install.sh` again after editing the art. Updating an active Ozark
About image preserves the original logo backup used when switching away.
