# Extras

Things Omarchy cannot install from a theme repo, so `install.sh` puts them in
place (and `install.sh --uninstall` takes them out again):

- `cliamp/ozark.toml` — music player theme
- `art/hawksbill-crag.txt` — Whitaker Point, printed when a terminal opens
- `art/ozark-ridge.txt` — the ridgeline, dropped into Omarchy's About logo slot
  (`~/.config/omarchy/branding/about.txt`) so Omarchy sizes the About window
  to fit it
- `art/*.svg` — the vector sources both pieces were converted from
- `art/render.py` — regenerates both text files from their SVG sources
- `greeting.sh` — prints the crag, only while this theme is active
- `../hooks/ozark-theme-set.sh` — switches cliamp and the About logo with the
  theme. Named after the theme on purpose: `omarchy hook install` copies by
  basename, so a hook called `theme-set.sh` would overwrite another theme's.

## Redrawing the art

Both pieces come from the SVGs in `art/`. The drawings use black for dots
and white for open space. To regenerate after an edit, with Python 3 and
ImageMagick installed, run from the repository root:

```bash
python3 extras/art/render.py
```

The converter fixes Hawksbill Crag at 56 columns by 18 rows and the ridgeline
at 64 columns by 20 rows. It preserves blank Braille cells, including those
at the ends of lines, so Omarchy measures the full About canvas.
