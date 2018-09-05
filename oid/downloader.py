import os
from tqdm import tqdm
from oid.utils import images_options
from multiprocessing.dummy import Pool as ThreadPool


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
    print('-' * 10 + class_name + '-' * 10)
    print('[INFO] Downloading {} images.'.format(args.type_csv))
    df_val_images = images_options(df_val, args)

    images_list = df_val_images['ImageID'][df_val_images['LabelName'] == class_code].values
    images_list = set(images_list)
    if class_list is not None:
        class_name_list = '_'.join(class_list)
    else:
        class_name_list = class_name
    download_img(folder, dataset_dir, class_name_list, images_list, threads)
    get_label(folder, dataset_dir, class_name, class_code, df_val, class_name_list)


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
    print("[INFO] Found {} online images for {}.".format(len(images_list), folder))

    image_dir = folder
    download_dir = os.path.join(dataset_dir, image_dir, class_name)
    downloaded_images_list = [f.split('.')[0] for f in os.listdir(download_dir)]
    images_list = list(set(images_list) - set(downloaded_images_list))

    if len(images_list) > 0:
        pool = ThreadPool(threads)
        print("[INFO] Download of {} images in {}.".format(len(images_list), folder))
        commands = []
        for image in images_list:
            path = image_dir + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
            command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path
            commands.append(command)
        
        list(tqdm(pool.imap(os.system, commands), total = len(commands) ))
        print('[INFO] Done!')
        
        pool.close()
        pool.join() 
    else:
        print('[INFO] All images already downloaded.')

    

def get_label(folder, dataset_dir, class_name, class_code, df_val, class_list):
    '''
    Make the class_name.csv files

    :param folder: trai, validation or test
    :param dataset_dir: self explanatory
    :param class_name: self explanatory
    :param class_code: self explanatory
    :param df_val: DataFrame values
    :param class_list: list of the class if multiclasses is activated
    :return: None
    '''
    tqdm.pandas()
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

    df_val['IN_FOLDER'] = df_val[df_val['LabelName'] == class_code]['ImageID'].progress_apply(lambda x: True if x in images_label_list else False)
    df_val[(df_val['IN_FOLDER'] == True)][['ImageID', 'XMin', 'XMax', 'YMin', 'YMax']].to_csv(label_dir+ '/' + class_name +'.csv', index = False)

    print('[INFO] Labels creation completed. Image count: {}, Labels count: {}'.format(len(images_label_list), len(df_val[df_val['IN_FOLDER'] == True])))
