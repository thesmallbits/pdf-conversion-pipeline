import os

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


def main():
    converter = PdfConverter(
        artifact_dict=create_model_dict(device="cuda"),
        # renderer="marker.renderers.json.JSONRenderer"
    )

    rendered = converter(
        os.path.join(os.path.dirname(__file__), "../samples/singlepage.pdf")
    )

    _,something,images = text_from_rendered(rendered)
    print(something)
    print(images)
    # with open("./outputs/singlepage.md", "w+") as file:
    #     file.write(text) # text is already json


if __name__ == "__main__":
    main()
