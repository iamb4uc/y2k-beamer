#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
BAD_LOG = re.compile(r"Overfull|Underfull|Missing character:|LaTeX Warning:|Package .* Warning:")


def run(args, env=None, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(map(str, args))}\n{result.stdout[-6000:]}")
    return result.stdout


def verify_pdf(path, pages=None):
    info = run(["pdfinfo", str(path)])
    count = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    if pages is not None and count != pages:
        raise RuntimeError(f"{path}: expected {pages} pages; found {count}")
    text = run(["pdftotext", str(path), "-"])
    if not text.strip():
        raise RuntimeError(f"{path}: no extractable text")
    log = path.with_suffix(".log").read_text()
    warnings = [line for line in log.splitlines() if BAD_LOG.search(line)]
    if warnings:
        raise RuntimeError(f"{path}: log warnings:\n" + "\n".join(warnings))
    return count


def main():
    parser = argparse.ArgumentParser(description="Compile theme fixtures and verify installation")
    parser.add_argument("--engine", default="lualatex")
    parser.add_argument("--latexmk", default="latexmk")
    args = parser.parse_args()
    for tool in [args.engine, args.latexmk, "kpsewhich", "pdfinfo", "pdftotext", "pdffonts"]:
        if not shutil.which(tool):
            raise RuntimeError(f"Missing {tool}; install TeX Live / Poppler before make check.")
    env = os.environ.copy()
    env["TEXINPUTS"] = ":".join(map(str, [ROOT, ROOT / "examples", ROOT / "tests",
        ROOT / "build/assets", ROOT / "assets/fonts"])) + ":"
    count = verify_pdf(ROOT / "build/demo.pdf", pages=20)
    fonts = run(["pdffonts", str(ROOT / "build/demo.pdf")])
    rows = fonts.splitlines()[2:]
    if not rows or any(not re.search(r"\s+yes\s+(yes|no)\s+", row) for row in rows):
        raise RuntimeError("Demo contains unembedded fonts")
    print(f"Demo: {count} pages, embedded fonts, clean log, extractable text")
    out = ROOT / "build/check"
    out.mkdir(parents=True, exist_ok=True)
    variants = {
        "dark-169": ("169", "appearance=dark,decoration=full"),
        "light-43": ("43", "appearance=light,typography=editorial,decoration=subtle,grain=false"),
        "quiet-1610": ("1610", "decoration=none,footer=false,numbering=false,accent=35546B"),
        "numbers-only": ("169", "footer=false,numbering=true"),
    }
    for name, (aspect, options) in variants.items():
        source = out / f"{name}.tex"
        source.write_text(f"\\def\\TestAspect{{{aspect}}}\n\\def\\TestOptions{{{options}}}\n\\input{{smoke.tex}}\n")
        run([args.latexmk, f"-{args.engine}", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", f"-outdir={out}", str(source)], env=env)
        verify_pdf(source.with_suffix(".pdf"), pages=11)
        print(f"Variant {name}: clean log; layouts, overlays, images, code and links")
    run(["sh", "-n", "scripts/install.sh"])
    run(["sh", "scripts/install.sh", "--help"])
    invalid = subprocess.run(["sh", "scripts/install.sh", "invalid"], cwd=ROOT,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if invalid.returncode != 2:
        raise RuntimeError("Installer must reject invalid actions")
    for mode in ("copy", "link"):
        with tempfile.TemporaryDirectory(prefix="y2k-texmf-") as temp:
            install_env = env.copy()
            install_env["TEXMFHOME"] = temp
            install_env["TEXINPUTS"] = ""
            run(["sh", ROOT / "scripts/install.sh", "install", mode], env=install_env, cwd=Path("/"))
            found = run(["kpsewhich", "beamerthemeY2K.sty"], env=install_env, cwd=Path("/")).strip()
            expected = Path(temp) / "tex/latex/y2k-beamer/beamerthemeY2K.sty"
            if Path(found) != expected or expected.is_symlink() != (mode == "link"):
                raise RuntimeError(f"{mode} installation failed discovery")
            installed_license = expected.parent / "LICENSE"
            if installed_license.read_bytes() != (ROOT / "LICENSE").read_bytes():
                raise RuntimeError(f"{mode} installation omitted the project license")
            foreign_file = expected.parent / "user-file.txt"
            foreign_file.write_text("Keep this unrelated file.\n")
            source = Path(temp) / "installed.tex"
            source.write_text("\\documentclass{beamer}\n\\usetheme{Y2K}\n\\title{Installed theme}\n"
                              "\\begin{document}\n\\begin{frame}[plain]\\titlepage\\end{frame}\n\\end{document}\n")
            run([args.latexmk, f"-{args.engine}", "-interaction=nonstopmode", "-halt-on-error",
                 str(source)], env=install_env, cwd=Path(temp))
            verify_pdf(source.with_suffix(".pdf"), pages=1)
            run(["sh", ROOT / "scripts/install.sh", "uninstall"], env=install_env, cwd=Path("/"))
            if expected.exists() or expected.is_symlink():
                raise RuntimeError("Uninstall left a theme file")
            if installed_license.exists() or installed_license.is_symlink():
                raise RuntimeError("Uninstall left the project license")
            if not foreign_file.exists():
                raise RuntimeError("Uninstall removed an unrelated file")
        print(f"Installation {mode}: kpsewhich discovery, external compilation, uninstall")
    run([args.engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
         f"-output-directory={ROOT / 'build'}", str(ROOT / "examples/demo.tex")], env=env)
    verify_pdf(ROOT / "build/demo.pdf", pages=20)
    print("Repository rebuild after font relocation: clean log and valid PDF")
    print("All Y2K checks passed.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        raise SystemExit(str(error)) from error
