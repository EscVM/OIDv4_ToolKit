import os
import cv2
from tqdm import tqdm
from modules.utils import images_options
from modules.utils import bcolors as bc
from multiprocessing.dummy import Pool as ThreadPool

def download(args, df_val, folder, dataset_dir, class_name, class_code, class_list=None, class_list_for_yolo=None, threads = 20):
    print("classes_list_from_download_function ", class_list_for_yolo)
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

    download_img(folder, dataset_dir, class_name_list, images_list, threads)
    if not args.sub:
        get_label(folder, dataset_dir, class_name, class_code, df_val, class_name_list, args, class_list_for_yolo= class_list_for_yolo )


def download_img(folder, dataset_dir, class_name, images_list, threads):
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
    

    
    download_dir = os.path.join(dataset_dir, image_dir, class_name )

    if not os.path.exists(download_dir+"/images"):
        os.makedirs(download_dir+"/images")
        download_dir += "/images"
   
    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir)]
    images_list = list(set(images_list) - set(downloaded_images_list))

    print("downloaded_images_list  " ,downloaded_images_list)

    pool = ThreadPool(threads)


    if len(images_list) > 0:
        print(bc.INFO + 'Download of {} images in {}.'.format(len(images_list), folder) + bc.ENDC)
        commands = []
        for image in images_list:
            path = image_dir + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
            command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path                    
            commands.append(command)

        list(tqdm(pool.imap(os.system, commands), total = len(commands) ))

        print(bc.INFO + 'Done!' + bc.ENDC)
        pool.close()
        pool.join()
    else:
        print(bc.INFO + 'All images already downloaded.' +bc.ENDC)


def get_label(folder, dataset_dir, class_name, class_code, df_val, class_list, args, class_list_for_yolo= None):
    '''
    Make the label.txt files
    :param folder: train, validation or test
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
        
        download_dir += "/images"

        downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir) if f.endswith('.jpg')]
        images_label_list = list(set(downloaded_images_list))

        groups = df_val[(df_val.LabelName == class_code)].groupby(df_val.ImageID)

        for image in images_label_list:
            try:
                
                boxes = groups.get_group(image.split('.')[0])[['XMin', 'XMax', 'YMin', 'YMax']].values.tolist()
                file_name = str(image.split('.')[0]) + '.txt'
                file_path = os.path.join(label_dir, file_name)

                if os.path.isfile(file_path):
                    f = open(file_path, 'a')
                else:
                    f = open(file_path, 'w')


                if(args.yoloLabelStyle):
                    #print("write labels in yolo style")
                    # box = {x0, x1, y0, y1}
                    # x-mid = x0 + (x1-x0)/2.0
                    # same goes for y-mid = y0+(y1-y0)/2.0 
                    # width = x1-x0
                    # height = y1-y0
                    # <object-class-index> <x-mid> <y-mid> <width> <height>
                    for box in boxes:
                        x0, x1, y0, y1 = box

                        midx = x0 + ((x1-x0)/2.0)
                        midy = y0 + ((y1-y0)/2.0)

                        width = x1-x0
                        height = y1 - y0

                        # each row in a file is name of the class_name_index, Xmid, Y-mid, width, height (Yolo style)
                        print(class_list_for_yolo.index(class_name), midx, midy, width, height, file=f)
                else:
                    #store in the OID normal way.
                    current_image_path = os.path.join(download_dir, image + '.jpg')
                    dataset_image = cv2.imread(current_image_path)
                    for box in boxes:
                        box[0] *= int(dataset_image.shape[1])
                        box[1] *= int(dataset_image.shape[1])
                        box[2] *= int(dataset_image.shape[0])
                        box[3] *= int(dataset_image.shape[0])

                        # each row in a file is name of the class_name, XMin, YMix, XMax, YMax (left top right bottom)
                        print(class_name, box[0], box[2], box[1], box[3], file=f)



                


            except Exception as e:
                print(e)

        print(bc.INFO + 'Labels creation completed.' + bc.ENDC)
