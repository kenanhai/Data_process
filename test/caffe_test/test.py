import sys
import numpy as np
import os
import cv2
import time
import argparse
import numpy
import cls

def main(arg_dict):
    cls_detection = cls.Classification(arg_dict['gpu_id'],arg_dict['cls_model_def'],arg_dict['cls_model_weights'],arg_dict['image_resize'])
    img = cv2.imread(arg_dict['image_path'])

    result = cls_detection.detect(img)
    print(result)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_id', type=int, default=0, help='gpu id')

    parser.add_argument('--cls_model_def',
                        default='./model/lenet_train_val_eye_split_deploy.prototxt')
    parser.add_argument('--cls_model_weights',
                        default='./model/eye_1103_iter_155000.caffemodel')
    parser.add_argument('--image_resize',
                         default=34, type=int)

    parser.add_argument('--video_path', type=str, default='a.MOV')
    parser.add_argument('--image_path', type=str, default='1.jpg')
    arg_dict = vars(parser.parse_args())

    main(arg_dict)
