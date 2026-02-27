import logging as l
import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def split_pdf(src: Path, dest: Path):
    if not dest.is_dir:
        raise ValueError(f"{dest.absolute} is not a directory")
    if not src.is_file():
        raise ValueError(f"{src.absolute} must be a file")

    name, ext = os.path.splitext(src.name)
    if ext != ".pdf":
        raise ValueError(f"{src.absolute} must be a pdf")

    reader = PdfReader(src)

    num_pages = reader.get_num_pages()
    l.info(f"number of pages {num_pages}")

    for idx, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        dest.mkdir(parents=True, exist_ok=True)
        with open(dest / f"{name}_{idx}.pdf", "wb+") as file:
            writer.write_stream(file)

    return num_pages
