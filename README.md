# 🏔️ Ozark

An [Omarchy](https://omarchy.org) theme named for the Ozark mountains in
Northwest Arkansas. Indigo dusk, a coral sunset band, hazy blue ridges, and
teal-and-olive forest. Dark first, readable always.

![Desktop preview](preview.png)

## ✨ What you get

- **Palette** pulled from a dusk photograph of the Boston Mountains: a deep
  indigo-charcoal background, coral sunset accent, and secondaries taken from
  the ridge haze and the forest canopy. Every colour clears its contrast
  target on every background — body text sits near 13:1, and `muted`, the grey
  used for code comments, holds at 5.9:1 instead of the usual 3-ish.
- **Everything themed at once**: terminals (foot, Alacritty, Kitty, Ghostty),
  Neovim, btop, Helix, the Omarchy bar, launcher, notifications, lock screen,
  Chromium, VS Code, Obsidian, Claude Code, and the keyboard backlight.
- **Window borders** fade from sunset coral into ridge violet.
- **Six 4K wallpapers** in three illustration styles, with and without the
  Omarchy wordmark.
- **Optional extras**: Braille art of Hawksbill Crag greeting you in every new
  terminal, an Ozark ridgeline on the About screen, and a matching theme for
  the cliamp music player.

## 📦 Install

```bash
omarchy theme install https://github.com/itsMattGuenther/omarchy-ozark-theme.git
```

The theme is applied right away. Later, switch with:

```bash
omarchy theme set ozark
omarchy theme bg next        # cycle wallpapers
```

## 🎨 Wallpapers

![Wallpapers](docs/wallpapers.jpg)

Six variants live in `backgrounds/`, all 3840x2160: the original illustration,
a brush-painted version, and a flat cell-shaded version, each with and without
the Omarchy wordmark. They sort by filename, so the numbered prefixes decide
the order `omarchy theme bg next` walks. Add your own next to them, or drop
extra images into `~/.config/omarchy/backgrounds/ozark/` to keep them out of
the theme folder.

## 🖼️ The art

![Hawksbill Crag and the Ozark ridgeline](docs/preview-art.png)

Two original pieces of Braille art, drawn as vectors and converted dot by dot
rather than traced from a photo.

**Hawksbill Crag** — the overhanging ledge at Whitaker Point in the Ozark
National Forest, the most photographed spot in Arkansas — greets you in every
new terminal:

![Terminal greeting](docs/preview-greeting.png)

**The Ozark ridgeline** takes over the About screen, sized so Omarchy's own
window measurement fits around it:

![About screen](docs/preview-about.png)

Both live in `extras/art/` as plain text, with the SVG sources next to them so
you can redraw or resize them.

## 🎵 cliamp

![cliamp in the Ozark theme](docs/preview-cliamp.png)

A matching theme for the [cliamp](https://github.com/omacom-io/cliamp) music
player. The theme hook switches cliamp to it while Ozark is active and puts
your previous cliamp theme back when you switch away.

## 🔐 The lock screen

The lock screen (Super+Escape) shows a blurred copy of whichever wallpaper you
are on, with the theme's colours on the password box. That is how Omarchy
builds it, and no theme can put its own artwork there.

## 👾 Extras (optional)

Omarchy cannot install the art, the greeting or the cliamp theme from a theme
repo, so there is a one-shot script:

```bash
~/.config/omarchy/themes/ozark/extras/install.sh
```

What it changes:

- copies files into `~/.config/ozark/` and `~/.config/cliamp/themes/`
- adds one marked block at the end of `~/.bashrc` (a backup is kept as
  `.bashrc.bak.ozark`)
- installs a theme hook, `ozark-theme-set.sh`, that switches cliamp and the
  About logo whenever this theme is active, and puts both back when you pick
  another theme

The hook is named after the theme rather than `theme-set.sh`, so it sits
alongside other themes' hooks instead of overwriting them.

The greeting and the About art only show while this theme is the active one,
so other themes are left alone.

To remove all of it:

```bash
~/.config/omarchy/themes/ozark/extras/install.sh --uninstall
```

## 🛠️ Hacking on it

- `colors.toml` is the whole palette. Everything else is generated from it.
- The wallpapers were upscaled to 4K with a Mitchell resample and a light
  unsharp pass; if you re-render the sources at native 4K they will be sharper
  than any upscale.
- The Braille art is generated from `extras/art/*.svg`. Edit the vectors, then
  re-run the converter at the same character width to keep the proportions.

## 🙏 Credits

- Wallpapers and Braille art are original work for this theme.
- Built on Omarchy's theme system by DHH and the Omarchy community.

## 🤝 Contributing

I'd gladly take help from anyone who wants to iterate on this: native 4K
wallpaper renders, better art, palette tweaks, new extras, anything. Open an
issue or a pull request. I'm here for the community <3

## ⚖️ License

MIT, see `LICENSE`.
