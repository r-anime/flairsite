

import argparse
import pathlib

from PIL import Image


def validate_image(image_path) -> Image:
    image = Image.open(image_path)
    width, height = image.size

    if not 32 <= height <= 128:
        raise ValueError("Width must be between 32 and 128 pixels")

    if width % height != 0:
        raise ValueError(f"Width must be a multiple of height: {[height * i for i in range(1, 6)]}")

    return image


def slice_image(image_file, start_code) -> list[str]:
    width, height = image_file.size
    slices = width // height

    path_list = []
    next_code = None
    for i in range(1, slices + 1):
        # Tb -> Tc -> Td etc.
        next_code = start_code if next_code is None else next_code[0] + chr(ord(next_code[1]) + 1)
        output_path = f"{next_code}.png"
        path_list.append(output_path)
        box = (height * (i - 1), 0, height * i, height)
        image_slice = image_file.crop(box)
        image_slice.save(output_path)

    return path_list


def _get_parser() -> argparse.ArgumentParser:
    new_parser = argparse.ArgumentParser(description="Slice an image into equal size emoji.")
    new_parser.add_argument("-c", "--code", required=True, type=str, help="Starting emoji code to use.")
    new_parser.add_argument("-f", "--file", required=True, type=str, help="Image file to split into emoji.")
    return new_parser


def main():
    parser = _get_parser()
    args = parser.parse_args()

    image_path = pathlib.Path(args.file)
    image = validate_image(image_path)
    if len(args.code) != 2:
        raise ValueError("Code must be two characters")
    slice_image(image, args.code)


if __name__ == "__main__":
    main()
