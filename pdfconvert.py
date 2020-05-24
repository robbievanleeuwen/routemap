import os
from PIL import Image
from pdf2image import convert_from_path


def convert_pdf(path):
    Image.MAX_IMAGE_PIXELS = None

    files = os.listdir(path)

    for file in files:
        if file[-3:] == 'pdf':
            convert_from_path(path + file, dpi=300, fmt='jpeg')


if __name__ == "__main__":
    convert_pdf(path='maps/')
