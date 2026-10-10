#!/bin/sh
set -eu
usage() { printf '%s\n' "Usage: sh scripts/install.sh install [copy|link] | uninstall | --help"; }
die() { printf '%s\n' "$*" >&2; exit 1; }
case "${1:-}" in --help|-h) usage; exit 0;; install|uninstall) action=$1;; *) usage >&2; exit 2;; esac
mode=${2:-copy}
case "$mode" in copy|link) ;; *) die "Installation mode must be copy or link.";; esac
command -v kpsewhich >/dev/null 2>&1 || die "Missing kpsewhich. Install TeX Live first."
root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
texhome=$(kpsewhich -var-value TEXMFHOME)
[ -n "$texhome" ] || die "kpsewhich returned an empty TEXMFHOME."
dest=$texhome/tex/latex/y2k-beamer
marker=$dest/.y2k-beamer-install
if [ "$action" = uninstall ]; then
  [ -f "$marker" ] || die "No managed Y2K installation at $dest; refusing removal."
  while IFS= read -r file; do
    case "$file" in beamerthemeY2K.sty|beamercolorthemeY2K.sty|beamerfontthemeY2K.sty|beamerinnerthemeY2K.sty|beamerouterthemeY2K.sty|y2kgraphics.sty|Orbitron-Bold.otf|OFL.markdown|LICENSE) rm -f -- "$dest/$file";; *) die "Invalid installation manifest.";; esac
  done < "$marker"
  rm -f -- "$marker"
  rmdir -- "$dest" 2>/dev/null || :
  command -v mktexlsr >/dev/null 2>&1 && mktexlsr "$texhome"
  printf '%s\n' "Removed the managed Y2K theme from $dest"
  exit 0
fi
if [ -d "$dest" ] && [ ! -f "$marker" ]; then
  die "Unmanaged directory exists at $dest; refusing to overwrite it."
fi
mkdir -p -- "$dest"
: > "$marker"
for file in beamerthemeY2K.sty beamercolorthemeY2K.sty beamerfontthemeY2K.sty beamerinnerthemeY2K.sty beamerouterthemeY2K.sty y2kgraphics.sty Orbitron-Bold.otf OFL.markdown LICENSE; do
  source=$root/$file
  case "$file" in Orbitron-Bold.otf|OFL.markdown) source=$root/assets/fonts/$file;; esac
  [ -f "$source" ] || die "Missing source file: $source"
  if [ "$mode" = link ]; then
    ln -sf -- "$source" "$dest/$file"
  else
    rm -f -- "$dest/$file"
    cp -- "$source" "$dest/$file"
  fi
  printf '%s\n' "$file" >> "$marker"
done
command -v mktexlsr >/dev/null 2>&1 && mktexlsr "$texhome"
found=$(cd / && TEXINPUTS='' kpsewhich beamerthemeY2K.sty)
[ "$found" = "$dest/beamerthemeY2K.sty" ] || die "Installed files, but discovery found '$found' instead of '$dest/beamerthemeY2K.sty'. Check TEXMFHOME and TEXMF configuration."
printf '%s\n' "Installed ($mode): $found" "TEXMFHOME: $texhome"
