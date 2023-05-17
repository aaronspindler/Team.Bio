from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from utils.images import convert_and_compress_image


class CleanedImageField(forms.ImageField):
    def clean(self, data, initial=None):
        data = super(CleanedImageField, self).clean(data, initial)
        if data:
            if not data.name.lower().endswith(".png"):
                name, buffer = convert_and_compress_image(data)
                data = InMemoryUploadedFile(
                    name=name,
                    file=buffer,
                    field_name="picture",
                    content_type="image/jpg",
                    size=buffer.getbuffer().nbytes,
                    charset=None,
                )
        return data
