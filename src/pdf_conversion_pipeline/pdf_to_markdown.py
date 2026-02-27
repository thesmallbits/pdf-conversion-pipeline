import logging as l
from pathlib import Path

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

from pdf_conversion_pipeline.utils import assert_dir, assert_file


converter = PdfConverter(
    artifact_dict=create_model_dict(device="cuda"),
    renderer="marker.renderers.markdown.MarkdownRenderer",
    config={"use_llm": False},
)
# converts a pdf file to markdown
#
def convert_to_markdown(src: Path):
    assert_file(src)

    rendered = converter(str(src))
    return text_from_rendered(rendered)
