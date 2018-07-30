import numpy as np
import nibabel as nib
import os
import argparse
import sys

import utils


def crop(image, output, args):
	if args.type == 'coor':
		print(args.mincoor)
		print(args.maxcoor)
		cropped = utils.crop_coors(image[0], args.mincoor, args.maxcoor)
		utils.save_file(cropped, image[1], image[2], output)
	elif args.type == 'size':
		cropped = utils.crop_size(image[0], args.size, args.offset)
		utils.save_file(cropped, image[1], image[2], output)
	else:
		print('type error')


def crop_file(args):
	image = utils.read_file(args.input)
	crop(image, args.output, args)

def crop_folder(args):
	imageFiles = []
	for file in os.listdir(args.input):
		imageFiles.append(file)
	for file in imageFiles:
		imagefilename = os.path.join(args.input, file)
		outputfilename = os.path.join(args.output, file)

		image = utils.read_file(imagefilename)
		crop(image, outputfilename, args)


def main(args):
	if args.file:
		crop_file(args)
	elif args.folder:
		crop_folder(args)
	else:
		print('choose file or folder')

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--file', action='store_true', dest='file', help='process a file')
	parser.add_argument('--folder', action='store_true', dest='folder', help='process all eligible files in a folder')
	parser.add_argument('--input', required='True', type=str, dest='input', help='input file or folder')
	parser.add_argument('--output', required='True', type=str, dest='output', help='output file or folder')
	parser.add_argument('--cropType', required='True', type=str, dest='type', help='crop type, coor or size')
	parser.add_argument('--size', nargs='*', type=int, dest='size', help='target size')
	parser.add_argument('--offset', nargs='*', type=int, dest='offset', help='offset')
	parser.add_argument('--mincoor', nargs='*', type=int, dest='mincoor', help='minimum coordinates')
	parser.add_argument('--maxcoor', nargs='*', type=int, dest='maxcoor', help='maximum coordinates')
	

	args = parser.parse_args()
	main(args)




