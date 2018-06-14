# nifti2binary A Python script for converting nifti images to binary file(s).
# 
# Author   : Haomeng Zhang and Liang Mi (Arizona State University)
# Contact  : icemiliang@gmail.com
# Date     : June 7th 2018

import argparse
import os
import sys
import h5py
import nibabel as nib
import pandas as pd
import numpy as np
import logging
import gc

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

dtypeDict = {'rid':np.uint32, 'sid':'S10', 'age':np.float32, \
			'sex':'S10', 'visit':np.uint32, 'dxCurrent':'S10', \
			'dxChange':np.uint32, 'mmse':np.uint32, 'filename':'S10', \
			'iid':np.uint32}

def _read_nifti(filename):
	nifti = nib.load(filename)
	# We assume the images are aligned and/or registered, no need to return header.
	return nifti.get_data(), nifti.header

def _write_buffer_to_hdft(data, images, counterFrom, counterTo):
	logging.info('Writting data from %d to %d ...' %(counterFrom,counterTo-1))
	imageArr = np.asarray(images, dtype=np.float32)
	data[counterFrom:counterTo, ...] = imageArr

def _release_buffer(buffer):
	del	buffer[:]
	gc.collect()

def _nifti2hdf5(args):
	logging.info('Converting nifti to hdf5...')
	csv = pd.read_csv(args.csvFile)
	rids = csv.rid.unique()
	imageNames = []
	for rid in rids:
		imageNames.append(csv.loc[csv['rid'] == rid]['filename'].values[0])

	numImages = len(imageNames)
	hdf5 = h5py.File(args.outPrefix + ".hdf5", "w")

	imageSize = list(map(int,args.imageSize.split(',')))
	data = hdf5.create_dataset("images", [numImages] + imageSize, dtype = np.float32)

	labels = []
	cols = []
	for label, col in csv.iteritems():
		cols.append(col)
		labels.append(label)

	for i in range(len(cols)):
		hdf5.create_dataset(labels[i], data=np.asarray(cols[i], dtype=dtypeDict[labels[i]]))

	imageBuffer = []
	logging.info('Start reading images...')
	bufferLength = 0
	counterFrom = 0

	# Main process
	# 1. Load several images.
	# 2. Store them in buffer.
	# 3. Write the buffer to file.
	# 4. Clean buffer.

	for imageName in imageNames:
		imageFullName = os.path.join(args.inFolder,imageName)
		logging.info('Reading image: %s' % imageName)
		nifti = _read_nifti(imageFullName)
		image = nifti[0].copy()
		imageBuffer.append(image)
		bufferLength += 1

		if bufferLength == args.maxBuffLength:
			counterTo = counterFrom + bufferLength

			_write_buffer_to_hdft(data, imageBuffer, counterFrom, counterTo)
			_release_buffer(imageBuffer)

			counterFrom = counterTo
			bufferLength = 0;

	if not bufferLength == 0:
		counterTo  = counterFrom + bufferLength
		_write_buffer_to_hdft(data, imageBuffer, counterFrom, counterTo)
		_release_buffer(imageBuffer)
	
	hdf5.close()
	logging.info('Converting nifti to hdf5... Done.')

def _nifti2npz(args):
	print('Converting nifti to npz...')

	csv = pd.read_csv(args.csvFile)
	rids = csv.rid.unique()


	labels = []
	cols = []
	for label, col in csv.iteritems():
		cols.append(col)
		labels.append(label)

	rids = []
	names = []
	for i, row in csv.iterrows():
		#rid = row['rid']
		#diag = row['diagnosis']
		#image = row['name']
		rid = row['rid']
		rids.append(rid)
		name = row['filename']
		names.append(name)

	ridBuffer = []
	diagBuffer = []
	imageBuffer = []
	bufferLength = 0
	counterFrom = 0
	logging.info('Start reading images')

	# Main process
	# 1. Load several images.
	# 2. Store them in buffer.
	# 3. Write the buffer to file.
	# 4. Clean buffer.

	keys = {}
	for i in range(len(labels)):
		keys[labels[i]] = cols[i]

	for name in names:
		imageFullName = os.path.join(args.inFolder, name)
		logging.info('reading image: %s' % name)
		nifti = _read_nifti(imageFullName)
		image = nifti[0].copy()
		
		imageBuffer.append(image)

		bufferLength += 1

		if bufferLength == args.maxBuffLength:
			counterTo = counterFrom + bufferLength - 1
			outFile = '%s_from_%s_to_%s.npz' %(args.outPrefix, counterFrom, counterTo)
			imageArr = np.asarray(imageBuffer, dtype=np.float32)
			for i in range(len(labels)):
				keys[labels[i]] = cols[i][counterFrom:counterTo+1]
			keys['images'] = imageArr

			logging.info('Writting data from %d to %d ...' %(counterFrom,counterTo))
			np.savez(outFile, **keys)
			_release_buffer(imageBuffer)
			_release_buffer(ridBuffer)
			_release_buffer(diagBuffer)

			counterFrom = counterTo + 1
			bufferLength = 0;

	if not bufferLength == 0:
		counterTo  = counterFrom + bufferLength
		outFile = '%s_from_%s_to_%s' %(args.outPrefix, counterFrom, counterTo)
		logging.info('Writting data from %d to %d ...' %(counterFrom,counterTo))
		imageArr = np.asarray(imageBuffer, dtype=np.float32)
		for i in range(len(labels)):
			keys[labels[i]] = cols[i][counterFrom:counterTo+1]
		keys['images'] = imageArr
		np.savez(args.outFile, imageArr)
		_release_buffer(imageBuffer)
		_release_buffer(ridBuffer)
		_release_buffer(diagBuffer)

	logging.info('Converting nifti to npz... Done.')

def _parse_argument():
	parser = argparse.ArgumentParser(description = 'Convert nifti images to binary file(s).')

	parser.add_argument('--inFolder',required = True, type=str, dest='inFolder', help='input image folder.')
	parser.add_argument('--csv',     required = True, type=str, dest='csvFile',  help='csv table')
	parser.add_argument('--outPrefix', required = True, type=str, dest='outPrefix',  help = 'output binary filename prefix.')
	parser.add_argument('--size',    required = True, type=str, dest='imageSize', help='image size [x,y,z].')
	parser.add_argument('--maxBufferLength', required = False, type=int, default = 20, dest='maxBuffLength', 
			    							 help = 'maximum write buffer length.')
	parser.add_argument('--format', required = True, dest='format', 
			    							 help='output file format [nyz or hdf5].')

	args = parser.parse_args()
	return args

def main(args):
	if args.format == 'hdf5':
		_nifti2hdf5(args)
	elif args.format == 'npz':
		_nifti2npz(args)
	else:
		print('[ Error ]: Output format %s is not supported.',(args.format))

if __name__ == '__main__':

	args = _parse_argument()

	main(args)
