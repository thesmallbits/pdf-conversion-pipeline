import logging as l
import json
import os
from pathlib import Path
import shutil
from pdf_conversion_pipeline.pdf_to_markdown import (
    ConvertToMarkdown,
)
from pdf_conversion_pipeline.images_to_base64 import convert_to_base64


src = Path(__file__).parent / "outputs" / "splits" / "fitjee"


# def test_conversion():
#     return
#     dest = Path(__file__).parent / "outputs" / "converted" / "fitjee" / "function"
#     dest.mkdir(exist_ok=True, parents=True)
#     for filep in src.iterdir():
#         l.info(f"converting {filep}")
#         content, _, images = convert_to_markdown(filep)
#         encoded_images = convert_to_base64(images)

#         fname, _ = os.path.splitext(filep.name)

#         with open(dest / f"{fname}.md", "x+") as file:
#             file.write(content)
#         with open(dest / f"images_{fname}.json", "x+") as file:
#             json.dump(encoded_images, file)
#         l.info(f"converted {filep}")


# def test_conversion_class():
#     return
#     dest = Path(__file__).parent / "outputs" / "converted" / "fitjee" / "class"
#     if dest.exists():
#         shutil.rmtree(dest, ignore_errors=True)
#     dest.mkdir(exist_ok=True, parents=True)

#     for idx, filep in enumerate(src.iterdir()):
#         if idx == 3:
#             break

#         l.info(f"converting {filep}")

#         with ConvertToMarkdown() as converter:
#             content, _, images = converter(filep)
#             encoded_images = convert_to_base64(images)

#             fname, _ = os.path.splitext(filep.name)

#             with open(dest / f"{fname}.md", "x+") as file:
#                 file.write(content)
#             with open(dest / f"images_{fname}.json", "x+") as file:
#                 json.dump(encoded_images, file)
#             l.info(f"converted {filep}")


def test_single():
    file = src / "fitjee_page_6.pdf"
    dest = Path(__file__).parent / "outputs" / "converted" / "fitjee" / "class"
    with ConvertToMarkdown() as converter:
        content, _, images = converter(file)
        encoded_images = convert_to_base64(images)

        fname, _ = os.path.splitext(file.name)

        with open(dest / f"{fname}.md", "x+") as file:
            file.write(content)
        with open(dest / f"images_{fname}.json", "x+") as file:
            json.dump(encoded_images, file)
        l.info(f"converted {file}")
