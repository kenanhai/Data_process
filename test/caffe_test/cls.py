import sys
import numpy as np
import os
import cv2
import time
import argparse
import caffe
from caffe.proto import caffe_pb2
from google.protobuf import text_format

import mtcnn

class FaceDetection:
    def __init__(self, gpu_id, model_def, model_weights, image_resize):
        caffe.set_device(gpu_id)
        caffe.set_mode_gpu()
        PNet = caffe.Net(caffe_model_path+"/det1.prototxt", caffe_model_path+"/det1.caffemodel", caffe.TEST)
        RNet = caffe.Net(caffe_model_path+"/det2.prototxt", caffe_model_path+"/det2.caffemodel", caffe.TEST)
        ONet = caffe.Net(caffe_model_path+"/det3.prototxt", caffe_model_path+"/det3.caffemodel", caffe.TEST)

    def detect(self, image):
        img = image.copy()
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        boundingboxes, points = detect_face(img_rgb, minsize, PNet, RNet, ONet, threshold, False, factor)

        return boundingboxes, points



class Classification:
    def __init__(self, gpu_id, model_def, model_weights, image_resize):
        caffe.set_device(gpu_id)
        caffe.set_mode_gpu()

        self.image_resize = image_resize
        # Load the net in the test phase for inference, and configure input preprocessing.
        self.net = caffe.Net(model_def,      # defines the structure of the model
                             model_weights,  # contains the trained weights
                             caffe.TEST)     # use test mode (e.g., don't perform dropout)
         # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))  # h w c to c h w
        self.transformer.set_mean('data', np.array([127.5, 127.5, 127.5])) # mean pixel
        # the reference model operates on images in [0,255] range instead of [0,1]
        #self.transformer.set_raw_scale('data', 255)
        # the reference model has channels in BGR order instead of RGB
        #self.transformer.set_channel_swap('data', (2, 1, 0))
        self.transformer.set_input_scale('data', 0.0078125)

    def detect(self, image):
        '''
        classification
        '''
        # set net to batch size of 1
        # image_resize = 300
        #image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        #image=image/255

        self.net.blobs['data'].reshape(1, 3, self.image_resize, self.image_resize)
        #image = caffe.io.load_image(image_file)

        #Run the net and examine the top_k results
        transformed_image = self.transformer.preprocess('data', image)
        self.net.blobs['data'].data[...] = transformed_image

        # Forward pass.
        start = time.time()
        result = self.net.forward()['prob']  #result = self.net.forward()['fc7']
        print('Time consuming: ' + str(time.time()-start))

        return result
