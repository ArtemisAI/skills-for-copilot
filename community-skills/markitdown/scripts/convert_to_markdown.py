import argparse
import sys
import traceback
from pathlib import Path
from typing import Iterable, List, Set

try:
    from markitdown import MarkItDown
except Exception as e:
    print("Erro: markitdown não está instalado. Execute: pip install \"markitdown[all]\"", file=sys.stderr)
    raise


DEFAULT_EXTS = [
    ".pdf", ".docx", ".pptx", ".xlsx",
    ".html", ".htm", ".eml",
    ".txt", ".csv", ".json",
]


def iter_files(inputs: List[Path], recursive: bool, allow_exts: Set[str]) -> Iterable[Path]:
    for inp in inputs:
        if inp.is_file():
            if inp.suffix.lower() in allow_exts or not allow_exts:
                yield inp
        elif inp.is_dir():
            if recursive:
                for p in inp.rglob("*"):
                    if p.is_file() and (p.suffix.lower() in allow_exts or not allow_exts):
                        yield p
            else:
                for p in inp.glob("*"):
                    if p.is_file() and (p.suffix.lower() in allow_exts or not allow_exts):
                        yield p


def output_path_for(file_path: Path, out_dir: Path, base_root: Path, keep_ext: bool) -> Path:
    # Preserve relative structure
    rel = file_path
    try:
        rel = file_path.relative_to(base_root)
    except Exception:
        pass

    # Build output filename
    if keep_ext:
        out_name = f"{rel.name}.md"
    else:
        out_name = f"{rel.stem}.md"

    return out_dir.joinpath(rel.parent).joinpath(out_name)


def convert_file(md: MarkItDown, src: Path) -> str:
    result = md.convert(str(src))
    # MarkItDown returns an object with a Markdown string in `text_content`
    return getattr(result, "text_content", str(result))


def main():
    ap = argparse.ArgumentParser(description="Convert documents to Markdown using MarkItDown.")
    ap.add_argument("--input", "-i", nargs="+", required=True, help="Arquivo(s) ou diretório(s) de entrada")
    ap.add_argument("--out-dir", "-o", default=".local/out/markitdown", help="Diretório de saída")
    ap.add_argument("--recursive", "-r", action="store_true", help="Percorrer subpastas ao ler diretórios")
    ap.add_argument("--ext", nargs="*", default=DEFAULT_EXTS, help="Lista de extensões a incluir (ex.: .pdf .docx)")
    ap.add_argument("--keep-ext", action="store_true", help="Manter a extensão original no nome do .md (ex.: file.pdf.md)")
    ap.add_argument("--overwrite", action="store_true", help="Sobrescrever arquivos já convertidos")
    ap.add_argument("--debug", action="store_true", help="Mostrar stacktrace em caso de erro")

    args = ap.parse_args()

    inputs = [Path(p).resolve() for p in args.input]
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    allow_exts = {e.lower() for e in (args.ext or [])}

    # Determine a common root for structure preservation (first directory if provided, else parent of first file)
    base_root = None
    for p in inputs:
        if p.is_dir():
            base_root = p
            break
    if base_root is None and inputs:
        base_root = inputs[0].parent

    md = MarkItDown()

    total = 0
    ok = 0
    fail = 0
    for src in iter_files(inputs, recursive=args.recursive, allow_exts=allow_exts):
        total += 1
        out_path = output_path_for(src, out_dir, base_root, args.keep_ext)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if out_path.exists() and not args.overwrite:
            print(f"[SKIP] {src} -> {out_path} (já existe)")
            ok += 1
            continue

        try:
            md_text = convert_file(md, src)
            out_path.write_text(md_text, encoding="utf-8")
            print(f"[OK]   {src} -> {out_path}")
            ok += 1
        except Exception as e:
            print(f"[ERR]  {src}: {e}", file=sys.stderr)
            if args.debug:
                traceback.print_exc()
            fail += 1

    print(f"Concluído. Total: {total} | OK: {ok} | Erros: {fail}")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()

