import cv2
import os
import pandas as pd

def show(class_name, download_dir, label_dir, index):
    '''
    Show the images with the labeled boxes.

    :param class_name: self explanatory
    :param download_dir: folder that contains the images
    :param label_dir: folder that contains the labels
    :param index: self explanatory
    :return: None
    '''
    cv2.namedWindow(class_name, cv2.WINDOW_NORMAL)
    if len(os.listdir(label_dir)) == 1:
        df = pd.read_csv(label_dir+'/'+class_name+'.csv')
    else:
    	names = os.listdir(label_dir)
    	df = pd.read_csv(label_dir+'/'+names[0])
    	for name in names:
    		df = pd.concat((df, pd.read_csv(label_dir+'/'+names[0])))

    imgid = df['ImageID'].unique()[index]
    img_file = imgid+'.jpg'
    current_image_path = str(os.path.join(download_dir, img_file))
    img = cv2.imread(current_image_path)

    for line in df[df['ImageID']==imgid][['XMin', 'XMax', 'YMin', 'YMax']].values:
        xmin, xmax, ymin, ymax = line
        xmin, xmax, ymin, ymax = int(xmin*img.shape[1]), int(xmax*img.shape[1]), int(ymin*img.shape[0]), int(ymax*img.shape[0])
        cv2.rectangle(img, (xmax, ymax),(xmin, ymin), (0, 255, 0), 6)

    cv2.imshow(class_name, img)
