SHELL := /bin/sh
.DEFAULT_GOAL := demo
ENGINE ?= $(shell command -v lualatex >/dev/null 2>&1 && echo lualatex || echo pdflatex)
LATEXMK ?= latexmk
export TEXINPUTS := $(CURDIR):$(CURDIR)/build/assets:$(CURDIR)/examples:$(CURDIR)/assets/fonts:$(TEXINPUTS):
ASSETS := rack fiber portrait-a portrait-b portrait-c
ASSET_PDFS := $(addprefix build/assets/,$(addsuffix .pdf,$(ASSETS)))
THEME := $(wildcard *.sty)

.PHONY: all demo clean install uninstall check dependencies force
all: demo
demo: build/demo.pdf

dependencies:
	@command -v "$(ENGINE)" >/dev/null 2>&1 || { echo "Missing $(ENGINE). Install TeX Live (LuaLaTeX preferred), or use make ENGINE=pdflatex." >&2; exit 1; }
	@command -v "$(LATEXMK)" >/dev/null 2>&1 || { echo "Missing latexmk. Install the TeX Live latexmk package." >&2; exit 1; }
	@command -v kpsewhich >/dev/null 2>&1 || { echo "Missing kpsewhich. Install TeX Live." >&2; exit 1; }
	@for package in beamer.cls tikz.sty listings.sty standalone.cls booktabs.sty tgadventor.sty tgbonum.sty plex-mono.sty; do kpsewhich "$$package" >/dev/null || { echo "Missing TeX package: $$package" >&2; exit 1; }; done

build/assets/%.pdf: examples/assets/%.tex | dependencies
	@mkdir -p build/assets
	$(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build/assets "$<"

force:

build/demo.pdf: examples/demo.tex $(THEME) assets/fonts/Orbitron-Bold.otf $(ASSET_PDFS) force | dependencies
	@mkdir -p build
	$(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build "$<"

check: demo
	@command -v python3 >/dev/null 2>&1 || { echo "Missing python3 (used by make check)." >&2; exit 1; }
	python3 scripts/check.py --engine "$(ENGINE)" --latexmk "$(LATEXMK)"

install:
	sh scripts/install.sh install $(INSTALL_MODE)

uninstall:
	sh scripts/install.sh uninstall

clean:
	rm -rf build
