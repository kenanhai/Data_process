import os
import cv2
import numpy as np

def face_crop(txt_path,save_path):
    f = open(txt_path)
    line = f.readline()
    n = 0
    while line:
        try:
            img_path = line.split(" ")[0].strip()
            x1 = int(line.split(" ")[1].strip())
            y1 = int(line.split(" ")[2].strip())
            x2 = int(line.split(" ")[3].strip())
            y2 = int(line.split(" ")[4].strip())

            img = cv2.imread(img_path)
            #print(img.shape)
            filename = img_path.split("/")[-1]
            print(n,filename)
            width = img.shape[1]
            height = img.shape[0]
            center_y = int(0.5*(y1+y2))
            y11 = np.maximum(center_y - int(0.5*width), 0)
            y22 = np.minimum(center_y + int(0.5*width),height)
            crop= img[y11:y22,0:width,:]
            new_name = save_path + "/" + filename;
            src_name = "./src/"+ filename
            #print(x1)
            cv2.imwrite(new_name, crop)
            #cv2.imwrite(src_name,img)
            line = f.readline()
            n+=1
        except:
           line = f.readline()

if __name__=="__main__":
    txt_path = "./bounding_boxes_86754.txt"
    save_path = "./split"
    face_crop(txt_path,save_path)


