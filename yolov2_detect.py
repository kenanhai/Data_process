#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))
import datetime
import time
import cv2
import darknet as dn
import pdb

CLASSES = ('hold', 'stop', 'shutter')

if __name__ == '__main__':
    # 配置路径
    net = dn.load_net("cfg/yolov2_tiny_3.cfg", 
                "backup/yolov2_tiny_3_30000.weights", 0)
    meta = dn.load_meta("cfg/yolov2_tiny_3.data")
    test_dir = "/home/bu5/bu5project/caffe_yolov2/examples/yolov2/gesture_recognition_test.txt"
    
    ft = open(test_dir,'r')
    ft_line = ft.readline()
    
    i = 1
    while ft_line:  

        if i > 5:
            exit()
        ft_line = ft_line.strip('\n')
        imgfile = "%s"%(ft_line)
        print(imgfile)
        image = cv2.imread(imgfile)
        img_h = image.shape[0]
        img_w = image.shape[1]
        print(image.shape)
        
        # 检测目标
        out = dn.detect(net, meta, imgfile)
        print(out)
        
        for i in range(len(out)):
            x = out[i][2][0]
            y = out[i][2][1]
            w = out[i][2][2]
            h = out[i][2][3]
            print(x/img_w, y/img_h, w/img_w, h/img_h)
            
            left   = max(int(x - w/2), 0)
            top    = max(int(y - h/2), 0)
            right  = min(int(x + w/2), img_w)
            bottom = min(int(y + h/2), img_h)
            
            print(left, top, right, bottom)
            cv2.rectangle(image, (left, top), (right, bottom), (255,0,0), 5)
        name = "result-" + imgfile.split("/")[-1]
        cv2.imwrite(name, image)
        ft_line = ft.readline()
        
        i += 1
    ft.close()
    print("done")
    


