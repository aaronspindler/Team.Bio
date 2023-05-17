from io import BytesIO

from PIL import Image


def convert_and_compress_image(image):
    filename = "%s.jpg" % image.name.split(".")[0]
    image = Image.open(image)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=80)
    return filename, buffer
