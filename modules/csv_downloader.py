import os
import sys
import time
import urllib.request
import pandas as pd
import numpy as np

OID_URL = 'https://storage.googleapis.com/openimages/2018_04/'

def TTV(csv_dir, name_file):
    '''
    Manage error_csv and read the correct .csv file.

    :param csv_dir: folder of the .csv files
    :param name_file: name of the correct .csv file
    :return: None
    '''
    types = {
        'Confidence':  np.int8,
        'XMin':        np.float32,
        'XMax':        np.float32,
        'YMin':        np.float32,
        'YMax':        np.float32,
        'IsOccluded':  np.int8,
        'IsTruncated': np.int8,
        'IsGroupOf':   np.int8,
        'IsDepiction': np.int8,
        'IsInside':    np.int8 }

    CSV = os.path.join(csv_dir, name_file)
    error_csv(name_file, csv_dir)
    df_val = pd.read_csv(CSV, dtype=types)
    return df_val

def error_csv(file, csv_dir):
    '''
    Check the presence of the required .csv files.

    :param file: .csv file missing
    :param csv_dir: folder of the .csv files
    :return: None
    '''
    if not os.path.isfile(os.path.join(csv_dir, file)):
        print("[ERROR] Missing the {} file.".format(os.path.basename(file)))
        ans = input("[DOWNLOAD] Do you want to download the missing file? [Y/n] ")

        if ans.lower() == 'y':
            folder = str(os.path.basename(file)).split('-')[0]
            if folder != 'class':
                FILE_URL = str(OID_URL + folder + '/' + file)
            else:
                FILE_URL = str(OID_URL + file)

            FILE_PATH = os.path.join(csv_dir, file)
            save(FILE_URL, FILE_PATH)
            print("\n[DOWNLOAD] File {} downloaded into {}.".format(file, FILE_PATH))

        else:
            exit(1)

def save(url, filename):
    '''
    Download the .csv file.

    :param url: Google url for download .csv files
    :param filename: .csv file name
    :return: None
    '''
    urllib.request.urlretrieve(url, filename, reporthook)

def reporthook(count, block_size, total_size):
    '''
    Print the progression bar for the .csv file download.

    :param count:
    :param block_size:
    :param total_size:
    :return:
    '''
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * duration) + 1e-5))
    percent = int(count * block_size * 100 / (total_size + 1e-5))
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()