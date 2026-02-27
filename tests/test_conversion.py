import logging as l
import json
import os
from pathlib import Path
from pdf_conversion_pipeline.pdf_to_markdown import convert_to_markdown
from pdf_conversion_pipeline.images_to_base64 import convert_to_base64


def test_conversion():
    src = Path(__file__).parent / "samples" / 'fitjee'
    dest = Path(__file__).parent / "outputs" / "fitjee"
    dest.mkdir(exist_ok=True, parents=True)
    for filep in src.iterdir():
        l.info(f"converting {filep}")
        content, _, images = convert_to_markdown(filep)
        encoded_images = convert_to_base64(images)

        fname,_ = os.path.splitext(filep.name)

        with open(dest / f"{fname}.md", "x+") as file:
            file.write(content)
        with open(dest / f"images_{fname}.json", "x+") as file:
            json.dump(encoded_images, file)
