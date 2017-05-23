import os
import glob
import random
import numpy as np

import cv2

import caffe
from caffe.proto import caffe_pb2
import lmdb

#Size of images
IMAGE_WIDTH = 350
IMAGE_HEIGHT = 350

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

	#Histogram Equalization
	img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
	img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
	img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

	#Image Resizing
	img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

	return img


def make_datum(img, label):
	#image is numpy.ndarray format. BGR instead of RGB
	return caffe_pb2.Datum(
		channels=3,
		width=IMAGE_WIDTH,
		height=IMAGE_HEIGHT,
		label=label,
		data=np.rollaxis(img, 2).tostring())

train_lmdb = '/workspace/input/train_lmdb'
validation_lmdb = '/workspace/input/validation_lmdb'

os.system('rm -rf  ' + train_lmdb)
os.system('rm -rf  ' + validation_lmdb)


train_data = [img for img in glob.glob("../input/train/*jpg")]
test_data = [img for img in glob.glob("../input/test/*jpg")]

#Shuffle train_data
random.shuffle(train_data)

print 'Creating train_lmdb'

in_db = lmdb.open(train_lmdb, map_size=int(1e12), writemap=True)
with in_db.begin(write=True) as in_txn:
	for in_idx, img_path in enumerate(train_data):
		if in_idx %  6 == 0:
			continue
		img = cv2.imread(img_path, cv2.IMREAD_COLOR)
		img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
		if 'A' in img_path:
			label = 0
		elif 'B' in img_path:
			label = 1
		elif 'C' in img_path:
			label = 2
		elif 'D' in img_path:
			label = 3
		elif 'E' in img_path:
			label = 4
		elif 'F' in img_path:
			label = 5
		elif 'G' in img_path:
			label = 6
		elif 'H' in img_path:
			label = 7
		elif 'I' in img_path:
			label = 8
		elif 'J' in img_path:
			label = 9
		elif 'K' in img_path:
			label = 10
		elif 'L' in img_path:
			label = 11
		elif 'M' in img_path:
			label = 12
		elif 'N' in img_path:
			label = 13
		elif 'O' in img_path:
			label = 14
		elif 'P' in img_path:
			label = 15
		elif 'Q' in img_path:
			label = 16
		datum = make_datum(img, label)
		in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
		print '{:0>5d}'.format(in_idx) + ':' + img_path
in_db.close()


print '\nCreating validation_lmdb'

in_db = lmdb.open(validation_lmdb, map_size=int(1e12), writemap=True)
with in_db.begin(write=True) as in_txn:
	for in_idx, img_path in enumerate(train_data):
		if in_idx % 6 != 0:
			continue
		img = cv2.imread(img_path, cv2.IMREAD_COLOR)
		img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
		if 'A' in img_path:
			label = 0
		elif 'B' in img_path:
			label = 1
		elif 'C' in img_path:
			label = 2
		elif 'D' in img_path:
			label = 3
		elif 'E' in img_path:
			label = 4
		elif 'F' in img_path:
			label = 5
		elif 'G' in img_path:
			label = 6
		elif 'H' in img_path:
			label = 7
		elif 'I' in img_path:
			label = 8
		elif 'J' in img_path:
			label = 9
		elif 'K' in img_path:
			label = 10
		elif 'L' in img_path:
			label = 11
		elif 'M' in img_path:
			label = 12
		elif 'N' in img_path:
			label = 13
		elif 'O' in img_path:
			label = 14
		elif 'P' in img_path:
			label = 15
		elif 'Q' in img_path:
			label = 16
		datum = make_datum(img, label)
		in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
		print '{:0>5d}'.format(in_idx) + ':' + img_path
in_db.close()

print '\nFinished processing all images'
