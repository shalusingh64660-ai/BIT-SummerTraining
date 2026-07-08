from __future__ import annotations
from pathlib import Path

from manga_scanner.models import MangaScan


def _escape(text: str) -> str:
    """Escape markdown special characters."""
    return (
        text.replace("\\", "\\\\")
        .replace("*", "\\*")
        .replace("_", "\\_")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("#", "\\#")
        .replace("-", "\\-")
        .replace(".", "\\.")
        .replace("`", "\\`")
    )
def _normalize_path(path: str) -> str:
    return "/" + Path(path).as_posix().lstrip("/")

def render_markdown(scan: MangaScan) -> str:
    lines = []

    # -----------------------
    # Title
    # -----------------------
    lines.append(f"# {_escape(scan.title)}\n")

    # -----------------------
    # Metadata
    # -----------------------
    lines.append(f"- Source: `{_normalize_path(scan.source_path)}`")
    lines.append(f"- Type: {scan.source_type}")
    lines.append(f"- Pages: {len(scan.pages)}\n")

    # -----------------------
    # Pages
    # -----------------------
    for i, page in enumerate(scan.pages, start=1):
        lines.append(f"## Page {i}\n")

        lines.append(f"- Source page: `{page.source_name}`")
        lines.append(f"- Dimensions: {page.width} x {page.height}\n")

        lines.append("### OCR Text\n")

        if page.text_blocks:
            for j, block in enumerate(page.text_blocks, start=1):
                lines.append(f"{j}. {_escape(block)}")
        else:
            lines.append("_No text detected._")

        # warnings section only if exists
        if page.warnings:
            lines.append("\n### Warnings\n")
            for w in page.warnings:
                lines.append(f"- {_escape(w)}")

        lines.append("")  # spacing

    return "\n".join(lines).rstrip() + "\n"