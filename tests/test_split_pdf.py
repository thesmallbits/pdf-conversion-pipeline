import logging as l
from pathlib import Path

from pdf_conversion_pipeline.split_pdf import split_pdf


def test_split_pdf():
    src = Path(__file__).parent / "samples" / "fitjee.pdf"
    dest = Path(__file__).parent / "outputs" / "splits" / "fitjee"

    l.info(f"src path {src}")
    l.info(f"dest path {dest}")

    _ = split_pdf(src, dest)
