import cv2
import numpy as np


def yolo_txt_to_box(image_path, label_path):
    '''将标注数据转化为矩形框

    :return:
    '''
