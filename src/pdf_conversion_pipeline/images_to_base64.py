import base64
from io import BytesIO
from PIL.Image import Image
from pathlib import Path



def convert_to_base64(images: dict[str, Image]) -> dict[str, str]:
    converted = {}

    for name, image in images.items():
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        converted[name] = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return converted
