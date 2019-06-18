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
refer to README.md file
"""
from sys import exit
from textwrap import dedent
from modules.parser import *
from modules.utils import *
from modules.downloader import *
from modules.show import *
from modules.csv_downloader import *
from modules.bounding_boxes import *
from modules.image_level import *


ROOT_DIR = ''
DEFAULT_OID_DIR = os.path.join(ROOT_DIR, 'OID')

if __name__ == '__main__':

    args = parser_arguments()

    if args.command == 'downloader_ill':
        image_level(args, DEFAULT_OID_DIR)
    else:
        bounding_boxes_images(args, DEFAULT_OID_DIR)
