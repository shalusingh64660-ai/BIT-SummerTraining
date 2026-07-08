"""High-level scan orchestration."""

from __future__ import annotations

from pathlib import Path

from manga_scanner.loaders import load_pages
from manga_scanner.ocr import NullOcrEngine
from manga_scanner.models import MangaScan,PageScan


def scan_source(path: str | Path, ocr_engine=None) -> MangaScan:
    path = Path(path)

    pages = load_pages(path)

    engine = ocr_engine or NullOcrEngine()

    page_scans = []

    for page in pages:
        # OCR
        text_blocks = engine.recognize(page)

        cleaned = tuple(t.strip() for t in text_blocks if t.strip())

        warnings = []

        if not cleaned:
            warnings.append("No OCR text detected.")

        # manhwa check
        try:
            width, height = page.width, page.height
            if width > 0 and height / width >= 2.5:
                warnings.append("Long vertical manhwa-style page.")
        except Exception:
            pass

        page_scans.append(
            PageScan(
                page.page_number,
                page.source_name,
                page.width,
                page.height,
                cleaned,
                tuple(warnings),
            )
        )

    source_type = "folder"
    if path.suffix.lower() == ".cbz":
        source_type = "archive"
    elif path.suffix.lower() == ".zip":
        source_type = "archive"
    elif path.suffix.lower() == ".pdf":
        source_type = "pdf"
    elif path.is_file():
        source_type = "image"

    title = path.stem

    return MangaScan(
        title=title,
        source_path=str(path),
        source_type=source_type,
        pages=tuple(page_scans),
    )