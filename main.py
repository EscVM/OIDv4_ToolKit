# ---------------
# Date: 7/19/2018
# Place: Biella/Torino
# Author: EscVM & TArt
# Project: OID v4
# ---------------

"""
OID v4 Downloader
Download specific classes of the huge online dataset Open Image Dataset.
Licensed under the MIT License (see LICENSE for details)
------------------------------------------------------------
Usage:
"""
import os

import modules.bounding_boxes as bbox
import modules.image_level as imglevel
import modules.parser as parser

ROOT_DIR = ''
DEFAULT_OID_DIR = os.path.join(ROOT_DIR, 'OID')

if __name__ == '__main__':

    args = parser.parser_arguments()

    if args.command == 'downloader_ill':
        imglevel.image_level(args, DEFAULT_OID_DIR)
    else:
        bbox.bounding_boxes_images(args, DEFAULT_OID_DIR)
