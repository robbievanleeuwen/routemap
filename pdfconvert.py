import os
from PIL import Image
from pdf2image import convert_from_path


def convert_pdf(path):
    Image.MAX_IMAGE_PIXELS = None

    files = os.listdir(path)

    for file in files:
        if file[-3:] == 'pdf':
            print("Converting {0}...".format(file))
            convert_from_path(
                path + file, dpi=300, fmt='jpeg', output_file=file[:-4], output_folder=path,
                single_file=True
            )


if __name__ == "__main__":
    convert_pdf(path='maps/')
