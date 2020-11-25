import os
import cv2
import numpy as np
from PIL import Image
import json
from tqdm import tqdm
from modules.utils import images_options
from modules.utils import bcolors as bc
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
from imgaug.augmentables.segmaps import SegmentationMapsOnImage
from imantics import Mask
import shutil

MASK_DIR = os.path.join("OID", "masks")

def download(args, df_val, folder, dataset_dir, class_name, class_code, class_list=None, threads = 20):
    '''
    Manage the download of the images and the label maker.
    :param args: argument parser.
    :param df_val: DataFrame Values
    :param folder: train, validation or test
    :param dataset_dir: self explanatory
    :param class_name: self explanatory
    :param class_code: self explanatory
    :param class_list: list of the class if multiclasses is activated
    :param threads: number of threads
    :return: None
    '''
    if os.name == 'posix':
        rows, columns = os.popen('stty size', 'r').read().split()
    elif os.name == 'nt':
        try:
            columns, rows = os.get_terminal_size(0)
        except OSError:
            columns, rows = os.get_terminal_size(1)
    else:
        columns = 50
    l = int((int(columns) - len(class_name))/2)

    print ('\n' + bc.HEADER + '-'*l + class_name + '-'*l + bc.ENDC)
    print(bc.INFO + 'Downloading {} images.'.format(args.type_csv) + bc.ENDC)
    df_val_images = images_options(df_val, args)

    images_list = df_val_images['ImageID'][df_val_images.LabelName == class_code].values
    images_list = set(images_list)
    print(bc.INFO + '[INFO] Found {} online images for {}.'.format(len(images_list), folder) + bc.ENDC)

    if args.limit is not None:
        import itertools
        print(bc.INFO + 'Limiting to {} images.'.format(args.limit) + bc.ENDC)
        images_list = set(itertools.islice(images_list, args.limit))

    if class_list is not None:
        class_name_list = '_'.join(class_list)
    else:
        class_name_list = class_name

    """
aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/validation/78fc07b95a216074.jpg "OID\Dataset\validation\Coin"
1f990b331e554127_m03qhv5_c2198baf.png
aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/validation/1f990b331e554127_m03qhv5_c2198baf.png "OID\Dataset\validation\Heater"
aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/1f990b331e554127_m03qhv5_c2198baf.png "OID\Dataset\validation\Heater"
    """

    # download the actual image
    download_img(folder, dataset_dir, class_name_list, images_list, threads, ".jpg")
    
    # again for the mask image
    images_list = df_val_images['MaskPath'][df_val_images.LabelName == class_code].values
    images_list = set(images_list)
    print(bc.INFO + '[INFO] Found {} online images for {}.'.format(len(images_list), folder) + bc.ENDC)

    if args.limit is not None:
        import itertools
        print(bc.INFO + 'Limiting to {} images.'.format(args.limit) + bc.ENDC)
        images_list = set(itertools.islice(images_list, args.limit))
    masks_list = images_list
    # download_img(folder, dataset_dir, class_name_list, masks_list, threads, "")
    # print("\n\n\n\n\n")
        # print(mask)
        # orig_mask = "D:\oid-seg_masks\0" + mask[0] + "\\" + mask
    # orig_mask = "D:\oid-seg_masks"
    new_dst = str(os.path.join(dataset_dir, folder, class_name))

    # path = image_dir + '/' + str(image) + file_format + ' "' + download_dir + '\\' + mask + '"'
    # for mask in masks_list:
    #     orig_mask = str(os.path.join("D:\oid-seg_masks", '0' + mask[0], mask))
    #     command = ('xcopy /q /n ' + orig_mask + ' ' + new_dst)
    #     # command = command + '\\0' + mask[0] + '\\' + mask + ' '
    #     # print(command)
    #     subprocess.call(command)

    if not args.skip_json_gen:
        # get_label(folder, dataset_dir, class_name, class_code, df_val, class_name_list, args)
        make_json(MASK_DIR, masks_list, folder, class_name, dataset_dir)
    
# Winter_melon
# Heater
# Armadillo
# Pizza_cutter
# Band-aid

def download_img(folder, dataset_dir, class_name, images_list, threads, file_format):
    '''
    Download the images.
    :param folder: train, validation or test
    :param dataset_dir: self explanatory
    :param class_name: self explanatory
    :param images_list: list of the images to download
    :param threads: number of threads
    :return: None
    '''
    image_dir = folder
    download_dir = os.path.join(dataset_dir, image_dir, class_name)
    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir)]
    images_list = list(set(images_list) - set(downloaded_images_list))

    pool = ThreadPool(threads)

    if len(images_list) > 0:
        print(bc.INFO + 'Download of {} images in {}.'.format(len(images_list), folder) + bc.ENDC)
        commands = []
        for image in images_list:
            path = image_dir + '/' + str(image) + file_format + ' "' + download_dir + '"'
            command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path
            commands.append(command)
            # print(command)

        list(tqdm(pool.imap(os.system, commands), total = len(commands) ))

        print(bc.INFO + 'Done!' + bc.ENDC)
        pool.close()
        pool.join()
    else:
        print(bc.INFO + 'All images already downloaded.' +bc.ENDC)


# json template: 
#   set flags to false
#   change shapes->label
#   add points
#   add image path/name
#   add image hight and width
"""
# -need list of pngs, and their src directory
# -need class
# -parse out image name from mask file name
-get height/width
# -append shape to existing json


# open template
# open mask
# if existing json, append to shapes and set "multiple targets" to true
#     -set "multiple targets" to true if applicable


"""

def make_json(masks_dir, masks_list, img_dir, class_name, dataset_dir):

    with open("template.json") as json_file:
        template = json.load(json_file)
    
    for mask in masks_list:
        mask_path = os.path.join(masks_dir, '0' + mask[0], mask)
        image_name = mask.split('_')[0]
        new_shape = {}
        new_shape['label'] = class_name
        new_shape['line_color'] = None
        new_shape['fill_color'] = None
        new_shape['shape_type'] = "polygon"
        new_shape['flags'] = {}
        real_image = Image.open(os.path.join(dataset_dir, img_dir, class_name, image_name + '.jpg'))
        real_width, real_height = real_image.size
        mask_image = Image.open(mask_path)
        width, height = mask_image.size

        mask_array = np.array(mask_image)
        mask_array = SegmentationMapsOnImage(mask_array, (height, width)).resize((real_height, real_width))
        segmap_aug_arr = np.array(mask_array.get_arr_int(background_threshold=0 + .1))
        segmap_single = np.ma.masked_where(True, segmap_aug_arr).mask * segmap_aug_arr
        polygons = Mask(segmap_single).polygons()
        # Image.fromarray(mask_array.draw_on_image(np.array(real_image))[0]).show()
        if len(polygons.points) > 1:
            selected_points = polygons.points[0]
            for points in polygons.points:
                if selected_points.size < points.size:
                    selected_points = points
            new_shape['points'] = np.array(selected_points).tolist()
        else:
            try:
                new_shape['points'] = np.array(polygons.points).tolist()[0]
            except:
                new_shape['points'] = np.array(polygons.points).tolist()
        
        json_file_path = os.path.join(dataset_dir, img_dir, class_name, image_name + '.json')
        if os.path.exists(json_file_path):
            existing_json = None
            with open(json_file_path) as preexisting_json:
                existing_json = json.load(preexisting_json)
            for old_shapes in existing_json['shapes']:
                template['shapes'].append(old_shapes)
                template['flags']["multiple targets"] = True
            template['imagePath'] = image_name + '.jpg'
            template['imageHeight'] = existing_json['imageHeight']
            template['imageWidth'] = existing_json['imageWidth']

        template['shapes'].append(new_shape)
        template['imagePath'] = image_name + '.jpg'
        template['imageHeight'] = real_height
        template['imageWidth'] = real_width
        template['imageData'] = None
        
        with open(json_file_path, 'w+') as outfile:
            json.dump(template, outfile, indent=2)

        new_mask_path = os.path.join(dataset_dir, img_dir, class_name, mask)
        shutil.copy(mask_path, new_mask_path)
        
        template['shapes'] = []
        

    
    
    # segments = []
    # dataList = []
    # imageFilenames = []
    # for mask in masks_list:
    #     with open(filename) as json_file:
    #         data = json.load(json_file)
    #         dataList.append(data)
    #         segmap = shapes_to_masks(data)
    #         segments.append(segmap)
    #         imageFilenames.append(os.path.join(os.path.dirname(filename), data['imagePath']))



# def shapes_to_masks(data):
#     img_shape = (data['imageHeight'], data['imageWidth'])
#     count = 0
#     polyArray = np.zeros(img_shape, dtype=np.int32)
#     numObjects = len(data['shapes'])
#     for shape in data['shapes']:
#         count += 1
#         masks = labelme.utils.shape_to_mask(img_shape, shape['points'], line_width=1, point_size=1)
#         polyArray += (np.logical_xor(polyArray, masks) * np.array(masks).astype(dtype=np.int32) * count)
#     segmap = ia.SegmentationMapsOnImage(np.array(polyArray), img_shape, nb_classes=numObjects + 1)

#     return segmap

def get_label(folder, dataset_dir, class_name, class_code, df_val, class_list, args):
    '''
    Make the label.txt files
    :param folder: trai, validation or test
    :param dataset_dir: self explanatory
    :param class_name: self explanatory
    :param class_code: self explanatory
    :param df_val: DataFrame values
    :param class_list: list of the class if multiclasses is activated
    :return: None
    '''
    if not args.noLabels:
        print(bc.INFO + 'Creating labels for {} of {}.'.format(class_name, folder) + bc.ENDC)

        image_dir = folder
        if class_list is not None:
            download_dir = os.path.join(dataset_dir, image_dir, class_list)
            label_dir = os.path.join(dataset_dir, folder, class_list, 'Label')
        else:
            download_dir = os.path.join(dataset_dir, image_dir, class_name)
            label_dir = os.path.join(dataset_dir, folder, class_name, 'Label')

        downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir) if f.endswith('.jpg')]
        images_label_list = list(set(downloaded_images_list))

        groups = df_val[(df_val.LabelName == class_code)].groupby(df_val.ImageID)
        for image in images_label_list:
            try:
                current_image_path = os.path.join(download_dir, image + '.jpg')
                dataset_image = cv2.imread(current_image_path)
                # boxes = groups.get_group(image.split('.')[0])[['XMin', 'XMax', 'YMin', 'YMax']].values.tolist()
                boxes = groups.get_group(image.split('.')[0])[['BoxXMin', 'BoxXMax', 'BoxYMin', 'BoxYMax']].values.tolist()
                # BoxID,BoxXMin,BoxXMax,BoxYMin,BoxYMax
                file_name = str(image.split('.')[0]) + '.txt'
                file_path = os.path.join(label_dir, file_name)
                if os.path.isfile(file_path):
                    f = open(file_path, 'a')
                else:
                    f = open(file_path, 'w')

                for box in boxes:
                    box[0] *= int(dataset_image.shape[1])
                    box[1] *= int(dataset_image.shape[1])
                    box[2] *= int(dataset_image.shape[0])
                    box[3] *= int(dataset_image.shape[0])

                    # each row in a file is name of the class_name, XMin, YMix, XMax, YMax (left top right bottom)
                    print(class_name, box[0], box[2], box[1], box[3], file=f)

            except Exception as e:
                pass

        print(bc.INFO + 'Labels creation completed.' + bc.ENDC)
