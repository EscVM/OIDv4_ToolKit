import argparse

def parser_arguments():
    '''
    Manage the input from the terminal.

    :return: parser
    '''
    parser = argparse.ArgumentParser(description='Open Image Dataset Downloader', 
                                     epilog='Example: \n \
                                     python3 main.py download --classes Apple --type_csv validation --threads 50')

    parser.add_argument("command",
                        metavar="<command> 'download' or 'visualize'",
                        help="'download' or 'visualize'")
    parser.add_argument('--Dataset', required=False,
                        metavar="/path/to/OID/csv/",
                        help='Directory of the OID dataset folder')
    parser.add_argument('--classes', required=False, nargs='+',
                        metavar="list of classes",
                        help="Sequence of 'strings' of the wanted classes")
    parser.add_argument('--type_csv', required=False, choices=['train', 'test', 'validation', 'all'],
                        metavar="'train' or 'validation' or 'test' or 'all'",
                        help='From what csv search the images')

    parser.add_argument('--image_IsOccluded', required=False, choices=['0', '1'],
                        metavar="1 or 0",
                        help='Optional characteristic of the images. Indicates that the object is occluded by another object in the image.')
    parser.add_argument('--image_IsTruncated', required=False, choices=['0', '1'],
                        metavar="1 or 0",
                        help='Optional characteristic of the images. Indicates that the object extends beyond the boundary of the image.')
    parser.add_argument('--image_IsGroupOf', required=False, choices=['0', '1'],
                        metavar="1 or 0",
                        help='Optional characteristic of the images. Indicates that the box spans a group of objects (min 5).')
    parser.add_argument('--image_IsDepiction', required=False, choices=['0', '1'],
                        metavar="1 or 0",
                        help='Optional characteristic of the images. Indicates that the object is a depiction.')
    parser.add_argument('--image_IsInside', required=False, choices=['0', '1'],
                        metavar="1 or 0",
                        help='Optional characteristic of the images.  Indicates a picture taken from the inside of the object.')

    parser.add_argument('--multiclasses', required=False, default='0', choices=['0', '1'],
                       metavar="0 (default) or 1",
                       help='Download different classes separately (0) or together (1).')

    parser.add_argument('--threads', required=False, metavar="default 20",
                       help='Number of the threads to use, when downloading images. You can set up to 200.')


    return parser.parse_args()
