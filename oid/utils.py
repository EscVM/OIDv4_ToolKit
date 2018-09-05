import os

def images_options(df_val, args):
    '''
    Manage the options for the images downloader.

    :param df_val: DataFrame Value.
    :param args: argument parser.
    :return: modified df_val
    '''
    if args.image_IsOccluded is not None:
        rejectedID = df_val.ImageID[df_val.IsOccluded != int(args.image_IsOccluded)].values
        df_val = df_val[~df_val.ImageID.isin(rejectedID)]

    if args.image_IsTruncated is not None:
        rejectedID = df_val.ImageID[df_val.IsTruncated != int(args.image_IsTruncated)].values
        df_val = df_val[~df_val.ImageID.isin(rejectedID)]

    if args.image_IsGroupOf is not None:
        rejectedID = df_val.ImageID[df_val.IsGroupOf != int(args.image_IsGroupOf)].values
        df_val = df_val[~df_val.ImageID.isin(rejectedID)]

    if args.image_IsDepiction is not None:
        rejectedID = df_val.ImageID[df_val.IsDepiction != int(args.image_IsDepiction)].values
        df_val = df_val[~df_val.ImageID.isin(rejectedID)]

    if args.image_IsInside is not None:
        rejectedID = df_val.ImageID[df_val.IsInside != int(args.image_IsInside)].values
        df_val = df_val[~df_val.ImageID.isin(rejectedID)]

    return df_val

def mkdirs(Dataset_folder, csv_folder, classes):
    '''
    Make the folder structure for the system.

    :param Dataset_folder: Self explanatory
    :return: None
    '''

    directory_list = ['train', 'validation', 'test']

    for directory in directory_list:
        for class_name in classes:
            folder = os.path.join(Dataset_folder, directory, class_name, 'Label')
            if not os.path.exists(folder):
                os.makedirs(folder)
            filelist = [f for f in os.listdir(folder) if f.endswith(".txt")]
            for f in filelist:
                os.remove(os.path.join(folder, f))
    folder = os.path.join(csv_folder)
    if not os.path.exists(folder):
        os.makedirs(folder)


def progression_bar(toolbar_width, index):
    '''
    Print the progression bar for the download of the images.

    :param toolbar_width: self explanatory
    :param index: self explanatory
    :return: None
    '''
    print(' ' * (toolbar_width + 10), end='\r')
    print("[{}{}] {}/{}".format('-' * index, ' ' * (toolbar_width - index), index, toolbar_width), end='\r')