#!/bin/bash
# Ozark terminal greeting. Sourced from ~/.bashrc by extras/install.sh.
# Prints Night Flight and one line when a new interactive terminal opens,
# but only while the Ozark theme is the active Omarchy theme.
# Reads two small files, starts no programs.
[[ $- == *i* ]] || return 0 2>/dev/null || exit 0
[[ -r "$HOME/.local/state/omarchy/current/theme.name" ]] || return 0
read -r _oz_theme < "$HOME/.local/state/omarchy/current/theme.name"
if [[ $_oz_theme != ozark ]]; then unset _oz_theme; return 0; fi
unset _oz_theme
_oz_art="${BASH_SOURCE[0]%/*}/luna-moth.ansi.txt"
[[ -n ${NO_COLOR:-} ]] && _oz_art="${BASH_SOURCE[0]%/*}/luna-moth.txt"
if [[ -r $_oz_art ]]; then
  mapfile -t _oz_lines < "$_oz_art"
  printf '%s\n' "${_oz_lines[@]}"
  if [[ -n ${NO_COLOR:-} ]]; then
    printf '%s\n\n' "                  Stay a little wild."
  else
    printf '\e[1;38;2;197;143;184m%s\e[0m\n\n' "                  Stay a little wild."
  fi
fi
unset _oz_art _oz_lines
