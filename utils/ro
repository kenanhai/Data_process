import cv2
import os
import numpy as np
import glob

def rotate_image(mat, angle):
  # angle in degrees

  height, width = mat.shape[:2]
  image_center = (width/2, height/2)

  rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

  abs_cos = abs(rotation_mat[0,0])
  abs_sin = abs(rotation_mat[0,1])

  bound_w = int(height * abs_sin + width * abs_cos)
  bound_h = int(height * abs_cos + width * abs_sin)

  rotation_mat[0, 2] += bound_w/2 - image_center[0]
  rotation_mat[1, 2] += bound_h/2 - image_center[1]

  rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
  return rotated_mat

def mkdir_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    root_path = './imgs-1029'
    img_path=root_path+'/oppo-a57'
    save_path=root_path+'/imgs-crop-sun-1029'
    mkdir_path(save_path)

    img_list = glob.glob(img_path+'/*.png')
    print((img_list[0]))

    i=0
    for item in img_list:
        i+=1
        print("%d/%d path:%s"%(i,len(img_list), item))
        name  =  os.path.splitext(os.path.basename(item))[0]
        img = cv2.imread(item)
        img_rotation = rotate_image(img, 90)
        cv2.imwrite(save_path+'/'+name+'.jpg', img_rotation)
if __name__ == '__main__':
    main()
