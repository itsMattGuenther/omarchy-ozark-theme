#!/bin/bash
# Installs the Ozark extras that an Omarchy theme cannot ship on its own:
#   - cliamp music player theme    -> ~/.config/cliamp/themes/ozark.toml
#   - Ozark ridgeline About logo   -> ~/.config/ozark/about.txt (swapped in by the hook)
#   - terminal greeting            -> ~/.config/ozark/ + one block in ~/.bashrc
#   - theme-set hook               -> ~/.config/omarchy/hooks/theme-set.d/
# Safe to run more than once. Run with --uninstall to remove everything it added.
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
OZ_DIR="$HOME/.config/ozark"
BASHRC="$HOME/.bashrc"
MARK_START="# >>> ozark greeting >>>"
MARK_END="# <<< ozark greeting <<<"
HOOK="$HOME/.config/omarchy/hooks/theme-set.d/ozark-theme-set.sh"

remove_bashrc_block() {
  [[ -f $BASHRC ]] && grep -qF "$MARK_START" "$BASHRC" || return 0
  cp "$BASHRC" "$BASHRC.bak.ozark"
  sed -i "/^$MARK_START\$/,/^$MARK_END\$/d" "$BASHRC"
}

if [[ ${1:-} == --uninstall ]]; then
  remove_bashrc_block
  rm -f "$HOME/.config/cliamp/themes/ozark.toml" "$HOOK"
  # give Omarchy its own About logo back
  bash "$ROOT/hooks/ozark-theme-set.sh" "not-ours"
  rm -rf "$OZ_DIR"
  echo "Ozark extras removed. Open a new terminal to see the change."
  exit 0
fi

mkdir -p "$OZ_DIR" "$HOME/.config/cliamp/themes"
cp "$HERE/cliamp/ozark.toml" "$HOME/.config/cliamp/themes/ozark.toml"

# Recognize the installed art before replacing it, so the hook does not
# mistake our previous version for the user's original About logo.
ABOUT="$HOME/.config/omarchy/branding/about.txt"
ABOUT_WAS_OURS=0
if [[ -f $ABOUT && -f $OZ_DIR/about.txt ]] && cmp -s "$ABOUT" "$OZ_DIR/about.txt"; then
  ABOUT_WAS_OURS=1
fi
# Short ANSI palette codes keep Omarchy's About measurement compact.
cp "$HERE/art/ozark-ridge.ansi.txt" "$OZ_DIR/about.txt"
if (( ABOUT_WAS_OURS )); then cp "$OZ_DIR/about.txt" "$ABOUT"; fi
cp "$HERE/greeting.sh" "$OZ_DIR/greeting.sh"
cp "$HERE/art/luna-moth.txt" "$HERE/art/luna-moth.ansi.txt" "$OZ_DIR/"
rm -f "$OZ_DIR/hawksbill-crag.txt"

remove_bashrc_block
cat >> "$BASHRC" <<BLOCK
$MARK_START
[[ -r ~/.config/ozark/greeting.sh ]] && source ~/.config/ozark/greeting.sh
$MARK_END
BLOCK

omarchy hook install theme-set "$ROOT/hooks/ozark-theme-set.sh" >/dev/null
# Apply the hook to whatever theme is active right now.
"$HOOK" "$(cat "$HOME/.local/state/omarchy/current/theme.name" 2>/dev/null || true)"

cat <<MSG
Installed:
  - cliamp theme        ~/.config/cliamp/themes/ozark.toml
  - About-screen logo   $OZ_DIR/about.txt
  - greeting            one marked block at the end of ~/.bashrc
  - theme hook          $HOOK
Open a new terminal to see the greeting. Run with --uninstall to undo.
MSG
