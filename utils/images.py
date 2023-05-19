from io import BytesIO

import requests
from PIL import Image


def convert_and_compress_image(image):
    filename = "%s.jpg" % image.name.split(".")[0]
    image = Image.open(image)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=80)
    return filename, buffer


def get_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        bytes = BytesIO(response.content)
        return bytes
    return None
