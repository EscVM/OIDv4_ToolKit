import os

from modules.parser import parser_arguments
from modules.bounding_boxes import bounding_boxes_images
from modules.image_level import image_level

ROOT_DIR = ''
DEFAULT_OID_DIR = os.path.join(ROOT_DIR, 'OID')


def main():

    args = parser_arguments()

    if args.command == 'downloader_ill':
        image_level(args, DEFAULT_OID_DIR)
    else:
        bounding_boxes_images(args, DEFAULT_OID_DIR)


if __name__ == "__main__":

    main()
