import os
from textwrap import dedent

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

def show_classes(classes):
    '''
    Show the downloaded classes in the selected folder during visualization mode
    '''
    for n in classes:
        print("- {}".format(n))
    print("\n")

def logo(command):
    '''
    Print the logo for the downloader and the visualizer when selected
    '''
    print("""

		   ___   _____  ______            _    _    
		 .'   `.|_   _||_   _ `.         | |  | |   
		/  .-.  \ | |    | | `. \ _   __ | |__| |_  
		| |   | | | |    | |  | |[ \ [  ]|____   _| 
		\  `-'  /_| |_  _| |_.' / \ \/ /     _| |_  
		 `.___.'|_____||______.'   \__/     |_____|

	""")

    if command == 'download':
        print(dedent(""" 

 ______                                 __                       __                
|_   _ `.                              [  |                     |  ]               
  | | `. \  .--.   _   _   __  _ .--.   | |  .--.   ,--.    .--.| | .---.  _ .--.  
  | |  | |/ .'`\ \[ \ [ \ [  ][ `.-. |  | |/ .'`\ \`'_\ : / /'`\' |/ /__\\[ `/'`\] 
 _| |_.' /| \__. | \ \/\ \/ /  | | | |  | || \__. |// | |,| \__/  || \__., | |     
|______.'  '.__.'   \__/\__/  [___||__][___]'.__.' \'-;__/ '.__.;__]'.__.'[___]    
                                                                                  
"""))

    if command == 'visualize':
        print(""" 

     ____   ____  _                         __    _                        
    |_  _| |_  _|(_)                       [  |  (_)                       
      \ \   / /  __   .--.  __   _   ,--.   | |  __   ____  .---.  _ .--.  
       \ \ / /  [  | ( (`\][  | | | `'_\ :  | | [  | [_   ]/ /__\\[ `/'`\] 
        \ ' /    | |  `'.'. | \_/ |,// | |, | |  | |  .' /_| \__., | |     
         \_/    [___][\__) )'.__.'_/\'-;__/[___][___][_____]'.__.'[___]    
                                                                                                                                                       
""")


