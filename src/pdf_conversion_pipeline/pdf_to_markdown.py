import gc
import logging as l
import os
from pathlib import Path

import torch
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from torch.cuda import OutOfMemoryError, set_per_process_memory_fraction
from torch.cuda.memory import empty_cache

from pdf_conversion_pipeline.utils import assert_dir, assert_file

os.environ["RECOGNITION_BATCH_SIZE"] = "1"
os.environ["DETECTOR_BATCH_SIZE"] = "1"
os.environ["ORDER_BATCH_SIZE"] = "1"
os.environ["TABLE_REC_BATCH_SIZE"] = "1"


def log_allocated_mem(text):
    l.info(f"{text} CUDA memory allocated {torch.cuda.memory_allocated() / 1024**3}")


class ConvertToMarkdown:
    converter: PdfConverter

    def __init__(self) -> None:
        pass

    def convert_to_markdown(self, src: Path):
        assert_file(src)
        rendered = self.converter(str(src))
        result = text_from_rendered(rendered)
        del rendered
        return result

    def __enter__(self):
        log_allocated_mem("pre initialization")
        self.converter = PdfConverter(
            artifact_dict=create_model_dict(device="cuda"),
            renderer="marker.renderers.markdown.MarkdownRenderer",
            config={"use_llm": False},
        )
        log_allocated_mem("post initialization")
        return self.convert_to_markdown

    def __exit__(self, exc_type, exc_value, tb):
        l.info(torch.cuda.memory_summary())
        log_allocated_mem("pre collection")
        del self.converter
        torch.cuda.synchronize()
        gc.collect()
        empty_cache()
        log_allocated_mem("post collection")

        if exc_type == OutOfMemoryError:
            l.warn(
                "Went out of memory while converting the current file. The program will continue as usual but the file wont be saved"
            )
            empty_cache()

        return True
