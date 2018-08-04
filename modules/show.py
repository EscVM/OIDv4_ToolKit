import cv2
import os

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
    if not os.listdir(download_dir)[index].endswith('.jpg'):
        index += 2
    img_file = os.listdir(download_dir)[index]
    current_image_path = str(os.path.join(download_dir, img_file))
    img = cv2.imread(current_image_path)
    file_name = str(img_file.split('.')[0]) + '.txt'
    file_path = os.path.join(label_dir, file_name)
    f = open(file_path, 'r')

    for line in f:
        ax = line.split(' ')
        cv2.rectangle(img, (int(float(ax[-4])), int(float(ax[-3]))),
                      (int(float(ax[-2])),
                       int(float(ax[-1]))), (0, 255, 0), 3)

    cv2.imshow(class_name, img)
