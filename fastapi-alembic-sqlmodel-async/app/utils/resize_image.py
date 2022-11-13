from typing import Any
from PIL import Image
from io import BytesIO
from pydantic import BaseModel


class IModifiedImageResponse(BaseModel):
    width: int
    height: int
    file_format: str
    file_data: Any


def modify_image(image: BytesIO):
    pil_image = Image.open(image)
    file_format = pil_image.format

    # Prints out (1280, 960)
    # print(pil_image.size)
    # Image can be resized here

    in_mem_file = BytesIO()

    # format here would be something like "JPEG". See below link for more info.
    pil_image.save(in_mem_file, format=file_format)

    return IModifiedImageResponse(
        width=pil_image.width,
        height=pil_image.height,
        file_format=file_format,
        file_data=in_mem_file.getvalue(),
    )
