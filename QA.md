# Verification record

## Repository preparation on 2026-10-10

`make check ENGINE=pdflatex` passed: the 20-page demo, four configuration
fixtures, embedded demo fonts, extractable text, clean logs, copy/link
installation, external compilation, uninstall and the final repository rebuild.
Both installation modes also verified that the complete project license was
installed and removed on uninstall. ShellCheck passed for `scripts/install.sh`.

The root `LICENSE` matches the system's complete GNU GPL version 3 text.
The bundled Orbitron font checksum matches its provenance record; its original
SIL Open Font License remains unchanged, including two trailing whitespace lines.
Git whitespace checks passed for the remaining authored files.

LuaLaTeX was unavailable in this environment. The earlier LuaLaTeX and visual
inspection results below are historical; no new visual review was performed
for this repository preparation.

## Presentation verification on 2026-10-09

Verified on 2026-10-09 against the built artifacts, not just the theme source.

The theme default and Computer Networks demo now use the light appearance for
classroom projection: white backgrounds, near-black foregrounds and darker muted
text. All 20 light-demo slides were rendered and inspected after this change,
and the complete LuaLaTeX check suite passed again. The dark option remains
covered by the dark 16:9 fixture.

Body typography now uses TeX Gyre Adventor, with Orbitron retained for space
headings and IBM Plex Mono for code. All 20 slides were rendered again and reviewed;
the definition slide was also inspected at full resolution. The geometric
body face fits the existing margins, diagrams and comparison columns.
The full LuaLaTeX check suite passed with Adventor, and a separate pdfLaTeX
build of the 20-page demo also passed PDF and clean-log verification.

The diagnostic slide now centers its standalone flowchart vertically beside
the question column, using the documented optional `c` column alignment.
Its updated render was inspected at full resolution; the other demo columns
retain top alignment. The image/profile fixture also exercises centered columns.
The complete LuaLaTeX check suite passed after the alignment change, including
all four aspect/appearance fixtures and both installation modes.

Monospace typography now uses IBM Plex Mono for `\texttt`, listings and
technical labels. The demo was rendered again; terminal and Python slides
were inspected at full resolution, with no clipping or loss of indentation.
The pdfLaTeX demo also passed clean-log and 20-page PDF verification with
embedded Plex Mono fonts.
The complete LuaLaTeX `make check` suite passed with Plex Mono, including
the repository rebuild after temporary installations were removed.

Content slides now omit heading rules, side rails, column dividers, separator
rules, the automatic footer progress line and the cropped corner mesh. Content
separation uses whitespace; `\YTwoKProgress` remains available explicitly.
The demo was rendered again and reviewed, including full-size content and
definition slides. Spacer adjustments fixed overflow in dense block layouts.
The complete LuaLaTeX `make check` suite passed after removing these rules.

The content safe area now uses 7.5% side margins, a 6 mm reserved top inset
and footer text inset 5.5 mm from the bottom. The top and bottom space remains
reserved when footer text and numbering are disabled. Body text defaults to
10/12 pt, frame headings to 20/24 pt, and footer text to 6/7.2 pt. Cover metadata
shares the proportional side margins. Quiz and block spacers were adjusted
to fit the smaller content area.

All 20 demo slides were rendered and reviewed after the margin change, with
definition and quiz slides inspected at full resolution. The light 4:3 dense
block fixture was also inspected. The pdfLaTeX demo passed clean-log and
20-page PDF verification.
The complete LuaLaTeX `make check` suite passed with the new safe area,
including installation checks and the final repository rebuild.

Code windows now use a single Beamer color box background with padding; the
listings style paints no per-line backgrounds or borders. Inline listings and
external files share the same panel, with the SQL fixture exercising
`\YTwoKInputCode`. Terminal and Python renders were inspected at full size.
A pixel check on the terminal panel's unused right edge confirmed a continuous
charcoal fill with no horizontal seams. A focused pdfLaTeX fixture compiled
both inline Bash and external SQL blocks with a clean log.
The complete LuaLaTeX `make check` suite passed with solid code panels,
including all four fixtures, both installation modes and the final rebuild.

Code line numbering is now disabled by default in the shared listings style.
The 20-page demo was rebuilt and passed clean-log/PDF verification; the Python
slide was rendered and inspected to confirm the number gutter is empty.

Personal default setup: shared presentation instructions in `$HOME/AGENTS.md`,
with Codex and OpenCode global rules pointing to that file and a saved memory
preference. The actual TEXMFHOME symlink installation was discovered from an
unrelated temporary directory with `TEXINPUTS` empty. A two-page deck compiled
there under pdfLaTeX and LuaLaTeX. The LuaLaTeX PDF passed clean-log, page-count
and text verification, embedded Orbitron/Adventor/Plex fonts, and its content
page was rendered and inspected. These checks verify discovery and compilation;
they do not test a separate agent session's compliance with the default.

## Environment

- Linux with TeX Live 2026; Beamer 3.77 (2026-01-22).
- Native pdfTeX 1.40.29 / pdfLaTeX and latexmk 4.87.
- LuaHBTeX 1.24.0 from the TeX Live 2026 distribution, used in a temporary
  directory with the installed TeX package tree and a generated LuaLaTeX format.
- Poppler for PDF metadata, text, font, URL and rendering checks.

The system PATH did not contain LuaLaTeX. The temporary LuaHBTeX installation
was used for preferred-engine verification; it is not a theme dependency or
a permanent system installation. `make` automatically uses pdfLaTeX when
LuaLaTeX is unavailable.

## Results

- Complete Computer Networks demo: **20 pages**, 16:9, valid PDF 1.7,
  `453.543 x 255.118 pt`, all fonts embedded and text extractable.
- Final LuaLaTeX `make ENGINE=lualatex check`: **passed**. The final demo and
  all four fixture logs contain no overfull/underfull boxes, package warnings
  or missing glyphs.
- pdfLaTeX fallback: complete demo, four fixtures, copy/link installation and
  uninstall passed `make check` during implementation. Final delivery uses
  LuaLaTeX with Orbitron; pdfLaTeX substitutes Adventor.
- Fixtures exercised dark 16:9, light/editorial 4:3, undecorated 16:10 with
  footer/numbers disabled, and numbers without a footer. Each produces 11 PDF
  pages from 10 frames, verifying the two-overlay frame.
- Interfaces exercised: semantic and native blocks, equations, tables,
  hyperlinks, image cover crops, full bleed, circular profiles, primitive
  graphics, question options and C/SQL/config listings. The demo also exercises
  Bash/Python listings, topology, layer and architecture diagrams, a flowchart,
  comparisons and bibliography.
- Copy and symlink installs verified `kpsewhich -var-value TEXMFHOME` and theme
  discovery outside the repository, then compiled an installed theme there.
  Uninstall removed managed files while preserving an unrelated file.
- The Makefile's install/uninstall targets were separately exercised with a
  temporary TEXMFHOME. The theme is now also symlink-installed in the user's
  actual TEXMFHOME for use by future teaching and work presentations.
- `make clean` removed `build/`; the theme and all illustration assets rebuilt.
- Direct compilation from `examples/` succeeded with its `.latexmkrc`, without
  a manual TEXINPUTS assignment.
- ShellCheck, POSIX shell parsing, Perl configuration parsing and Python syntax
  checks passed. Installer help and invalid-action handling were exercised.
  A missing engine produced the intended dependency error.
- `pdfinfo -url` confirmed the three bibliography URL annotations on page 19.

## Visual inspection and refinements

All 20 final slides were rendered with `pdftoppm` at a 1600-pixel long side and
reviewed as a contact sheet. Cover, divider, code, quiz and profile slides were
also inspected at full size during refinement. The 11-page light 4:3 fixture
was rendered and reviewed separately.

The review corrected heading hyphenation, enlarged and repositioned cover
orbits, protected cover metadata from decoration, and gave dividers and the
conclusion distinct geometric compositions. Final inspection found readable
text and code, consistent margins, correct image proportions and circular
clipping, and no clipped or overlapping teaching content. The demo portraits
are original illustrations of fictional members, not photographs of real people.

Installation testing exposed an OTF cache retaining a deleted temporary font
path. The bundled Orbitron font now uses LuaHBTeX's HarfBuzz renderer. The check
suite rebuilds the repository demo after both temporary installation directories
have been removed; this regression check passed.

## Evidence

- `build/demo.pdf`: final LuaLaTeX demo.
- `build/preview/contact.png`: final overview of all slides.
- `build/preview/slide-*.png`: individual slide renders.
- `build/preview/light/contact.png`: light 4:3 fixture overview.
- `build/check/*.pdf`: the compiled configuration fixtures.
- `build/qa/check-lualatex.txt`: final full check output.
- `build/qa/check-pdflatex.txt`: fallback check output.
- `build/qa/direct-example.txt`: direct example-directory build output.

These generated artifacts are intentionally removed by `make clean`.
The checkout has no `.git` directory, so Git diff checks were unavailable;
the authored source was checked separately for trailing whitespace.

Physical projector performance and other operating systems/TeX distributions
were not tested. Arbitrary user content still needs its own overflow and visual
review. Minted is optional and was not exercised; the supported default uses
listings without shell escape.
