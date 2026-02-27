import logging as l
import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def split_pdf(
    src: Path,
    dest: Path,
    *,
    # 0 based page indices to skip
    skip_indices: list[int] = [],
):
    if dest.is_file():
        raise ValueError(f"{dest.absolute} is a file")
    if not src.is_file():
        raise ValueError(f"{src.absolute} must be a file")

    if dest.exists == False:
        l.warning(f"creating folder {dest.absolute}")
        dest.mkdir(parents=True)

    name, ext = os.path.splitext(src.name)
    if ext != ".pdf":
        raise ValueError(f"{src.absolute} must be a pdf")

    reader = PdfReader(src)

    num_pages = reader.get_num_pages()
    l.info(f"number of pages {num_pages}")

    for idx, page in enumerate(reader.pages, start=1):
        if idx in skip_indices:
            continue

        writer = PdfWriter()
        writer.add_page(page)
        dest.mkdir(parents=True, exist_ok=True)
        with open(dest / f"{name}_page_{idx}.pdf", "wb+") as file:
            writer.write_stream(file)

    return num_pages
