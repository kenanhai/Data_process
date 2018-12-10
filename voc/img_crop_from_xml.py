# -*- coding: utf-8 -*-
import os
import os.path
from xml.etree.ElementTree import parse, Element
import cv2

def test():
    path="/home/kenanhai/programs/work/darknet/mytrain/Annotations/"
    files=os.listdir(path) #得到文件夹下所有文件名称 
    s=[]
    for xmlFile in files: #遍历文件夹 
        if not os.path.isdir(xmlFile): #判断是否是文件夹,不是文件夹才打开 
            print (xmlFile)
            pass
        path="/home/kenanhai/programs/work/darknet/mytrain/Annotations/"
        newStr=os.path.join(path,xmlFile)
        dom=parse(newStr)  ###最核心的部分,路径拼接,输入的是具体路径 
        root=dom.getroot()
        #print root
        part=xmlFile[:-4]
        part1=part+'.jpg'
        newStr1='/home/kenanhai/programs/work/darknet/mytrain/JPEGImages/'+part1
        img = cv2.imread(newStr1)
        new_name = './crop/'+part1
        #root.remove(root.find('path'))
        #e=Element('path')
        print (root.find('path').text)
        for obj in root.iter('object'):
            xmlbox = obj.find('bndbox')
            x1 = int(xmlbox.find('xmin').text)
            y1 = int(xmlbox.find('ymin').text)
            x2 = int(xmlbox.find('xmax').text)
            y2 = int(xmlbox.find('ymax').text)
            crop = img[y1:y2,x1:x2,:]
            cv2.imwrite(new_name,crop)
        pass

if __name__=='__main__':
    test()
