import os
import cv2
from tqdm import tqdm
from modules.utils import images_options

def download(args, df_val, folder, dataset_dir, class_name, class_code, class_list=None):
    '''
    Manage the download of the images and the label maker.

    :param args: argument parser.
    :param df_val: DataFrame Values
    :param folder: train, validation or test
    :param dataset_dir: self explanatory
    :param class_name: self explanatory
    :param class_code: self explanatory
    :param class_list: list of the class if multiclasses is activated
    :return: None
    '''
    print('-' * 10 + class_name + '-' * 10)
    print('[INFO] Downloading {} images.'.format(args.type_csv))
    df_val_images = images_options(df_val, args)

    images_list = df_val_images['ImageID'][df_val_images.LabelName == class_code].values
    images_list = set(images_list)
    if class_list is not None:
        class_name_list = '_'.join(class_list)
    else:
        class_name_list = class_name
    download_img(folder, dataset_dir, class_name_list, images_list)
    get_label(folder, dataset_dir, class_name, class_code, df_val, class_name_list)


def download_img(folder, dataset_dir, class_name, images_list):
    '''
    Download the images.

    :param folder: train, validation or test
    :param dataset_dir: self explanatory
    :param class_name: self explanatory
    :param images_list: list of the images to download
    :return: None
    '''
    print("[INFO] Found {} online images for {}.".format(len(images_list), folder))

    image_dir = folder
    download_dir = os.path.join(dataset_dir, image_dir, class_name)
    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir)]
    images_list = list(set(images_list) - set(downloaded_images_list))

    if len(images_list) > 0:
        print("[INFO] Download of {} images in {}.".format(len(images_list), folder))
        for image in tqdm(images_list):
            path = image_dir + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
            command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path
            os.system(command)

        print('[INFO] Done!')
    else:
        print('[INFO] All images already downloaded.')


def get_label(folder, dataset_dir, class_name, class_code, df_val, class_list):
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
    print("[INFO] Creating labels for {} of {}.".format(class_name, folder))

    image_dir = folder
    if class_list is not None:
        download_dir = os.path.join(dataset_dir, image_dir, class_list)
        label_dir = os.path.join(dataset_dir, folder, class_list, 'Label')
    else:
        download_dir = os.path.join(dataset_dir, image_dir, class_name)
        label_dir = os.path.join(dataset_dir, folder, class_name, 'Label')

    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir) if f.endswith('.jpg')]
    images_label_list = list(set(downloaded_images_list))

    for image in images_label_list:
        try:
            current_image_path = os.path.join(download_dir, image + '.jpg')
            dataset_image = cv2.imread(current_image_path)
            boxes = df_val[['XMin', 'XMax', 'YMin', 'YMax']][
                (df_val.ImageID == image.split('.')[0]) & (df_val.LabelName == class_code)].values.tolist()
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

                # each row in a file is XMax, YMax, XMini, YMin
                print(class_name, box[1], box[3], box[0], box[2], file=f)

        except Exception as e:
            print(str(e))

    print('[INFO] Labels creation completed.')
