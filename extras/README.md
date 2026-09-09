# Extras

Things Omarchy cannot install from a theme repo, so `install.sh` puts them in
place (and `install.sh --uninstall` takes them out again):

- `cliamp/ozark.toml` — music player theme
- `art/hawksbill-crag.txt` — Whitaker Point, printed when a terminal opens
- `art/ozark-ridge.txt` — the ridgeline, dropped into Omarchy's About logo slot
  (`~/.config/omarchy/branding/about.txt`) so Omarchy sizes the About window
  to fit it
- `art/*.svg` — the vector sources both pieces were converted from
- `greeting.sh` — prints the crag, only while this theme is active
- `../hooks/ozark-theme-set.sh` — switches cliamp and the About logo with the
  theme. Named after the theme on purpose: `omarchy hook install` copies by
  basename, so a hook called `theme-set.sh` would overwrite another theme's.

## Redrawing the art

Both pieces come from the SVGs in `art/`. To regenerate after an edit:

```bash
magick art/hawksbill-crag.svg -background white -alpha remove -alpha off /tmp/crag.png
braille.py /tmp/crag.png --width 56 --height 18 --threshold 150 > art/hawksbill-crag.txt
```

Keep the character width the same or the art will not line up with the About
window Omarchy measures for it.
