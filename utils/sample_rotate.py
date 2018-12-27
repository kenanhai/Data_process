import os, sys
import cv2
import tqdm

rate = 3

date = "nir_real"
src = os.path.join("/mnt/disk0/kenanhai/NIR/nir", date)
dst = os.path.join("/mnt/disk0/kenanhai/NIR/nir/nir_real_split", date)
if not os.path.exists(dst):
    os.makedirs(dst)

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


videos = sorted(os.listdir(src))
for video in videos:
    print (video)
    cap = cv2.VideoCapture(os.path.join(src, video))
    if not cap.isOpened():
        print ("Error:", video)
        continue
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print (frames, width, height, fps)
    pbar = tqdm.tqdm(total=len(range(0, frames, rate)))
    for frame in range(0, frames, rate):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, mat = cap.read()
        #mat=cv2.resize(mat,(1280,720),interpolation=cv2.INTER_CUBIC)
        if not ret:
            print ("Error:", video, frame)
            continue
        img = os.path.splitext(os.path.basename(video))[0]
        img += "_{}.jpg".format(frame)
        #mat = rotate_image(mat, -90)
        cv2.imwrite(os.path.join(dst, img), mat)
        pbar.update(1)
    pbar.close()
    cap.release()
    print (video, "done")
