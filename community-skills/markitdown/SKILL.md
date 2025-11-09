---
name: markitdown
description: Universal conversion of common document types (PDF, DOCX, PPTX, XLSX, HTML, EML, etc.) into Markdown using the MarkItDown library. Provides single-file and batch conversion with folder recursion and structure preservation.
license: Proprietary. LICENSE.txt has complete terms
---

# MarkItDown Skill — Convert Files to Markdown

## Overview

This skill converts many document formats to Markdown using the MarkItDown library. It supports both one-off conversions and batch processing of folders, preserving directory structure in the output.

Typical inputs: PDF, DOCX, PPTX, XLSX, HTML/HTM, EML, TXT, CSV, JSON.

For large batches, use the provided Python script to recurse through folders and write `.md` files to an output directory under `.local/out/`.

## Quick Start

1) Create (optional) local venv
```
python -m venv .local/.venv
.local\.venv\Scripts\activate
```

2) Install MarkItDown (all extras)
```
pip install "markitdown[all]"
```

3) One file → Markdown (CLI do MarkItDown)
```
python -m markitdown "path/to/file.pdf" > "path/to/file.md"
```

4) Pasta inteira (recursivo, preservando estrutura)
```
python document-skills/markitdown/scripts/convert_to_markdown.py \
  --input "C:\\dados\\origem" \
  --out-dir ".local/out/markitdown" \
  --recursive
```

Resultado: arquivos `.md` em `.local/out/markitdown`, mantendo a árvore de diretórios de entrada.

## Script (batch)

Arquivo: `document-skills/markitdown/scripts/convert_to_markdown.py`

Funções principais:
- Converte arquivo único ou diretório.
- Filtro por extensões conhecidas (padrão cobre PDF/DOCX/PPTX/XLSX/HTML/EML/TXT/CSV/JSON). Use `--ext` para ajustar.
- `--recursive` para percorrer subpastas.
- Preserva estrutura de pastas na saída.
- Gera log simples no console (sucesso/falha por arquivo).

Uso detalhado:
```
python document-skills/markitdown/scripts/convert_to_markdown.py \
  --input "C:\\docs" \
  --out-dir ".local/out/markitdown" \
  --recursive \
  --ext .pdf .docx .pptx .xlsx .html .htm .eml .txt .csv .json
```

## Tips & Notes

- Para PDFs longos ou complexos, a saída pode reorganizar quebras de linha; isso é normal em conversores para Markdown.
- Se você precisa extrair campos específicos por rótulos (regex), prefira o skill `pdf` com `pdfplumber`.
- Para inspeção rápida, o CLI nativo também funciona: `python -m markitdown ...`.

## Troubleshooting

- Erro de parsing em um arquivo específico: reexecute o script com a flag `--debug` para ver a exceção.
- Saída vazia: verifique se a extensão está incluída em `--ext`. Tente também o CLI puro: `python -m markitdown <arquivo>`.

## References

- MarkItDown (CLI & Python API). Consultar a documentação oficial do projeto para formatos suportados e exemplos atualizados.

