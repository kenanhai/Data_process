# -*- coding: utf-8 -*-

import os
import shutil
path = '/data/kenanhai/NIR/NIR_negative/20181015/imgs_1015/rotated/labeled/789'
new_jpg_path = '/data/kenanhai/NIR/NIR_negative/20181015/imgs_1015/rotated/labeled/paper/jpg'
new_xml_path = '/data/kenanhai/NIR/NIR_negative/20181015/imgs_1015/rotated/labeled/paper/xml'
items = os.listdir(path)
newlist = []
count = 1462
for name in items:
    if name.endswith('.xml'):
        filename=os.path.splitext(name)[0] + '.jpg'
        old_jpg_path = os.path.join(path,filename)
        old_xml_path = os.path.join(path,name)
        jpg_name = str(count).zfill(6)+'.jpg'
        xml_name = str(count).zfill(6)+'.xml'
        new_jpg_name = os.path.join(new_jpg_path,jpg_name)
        new_xml_name = os.path.join(new_xml_path,xml_name)
        shutil.copy(old_jpg_path,new_jpg_name)
        shutil.copy(old_xml_path,new_xml_name)
        count+=1
        #print(filename)
        #newlist.append(name)
#print(newlist)
