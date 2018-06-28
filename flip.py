import os
import argparse
import sys

import utils

def _flip(image, output):
	flipped = utils.flip(image[0])
	utils.save_file(flipped, image[1], image[2], output)

def _flip_file(args):
	image = utils.read_file(args.input)
	_flip(image, args.output)

def _flip_folder(args):
	imageFiles = []
	for file in os.listdir(args.input):
		imageFiles.append(file)

	for file in imageFiles:
		imagefilename = os.path.join(args.input, file)
		outpufilename = os.path.join(args.output, file)

		image = utils.read_file(imagefilename)
		_flip(image, outpufilename)


def _main(args):
	if args.file:
		_flip_file(args)
	elif args.folder:
		_flip_folder(args)
	else:
		print('choose file or folder')


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--file', action='store_true', dest='file', help='process a file')
	parser.add_argument('--folder', action='store_true', dest='folder', help='process all eligible files in a folder')
	parser.add_argument('--input', required = True, type=str, dest='input', help='input file or folder')
	parser.add_argument('--output', required = True, type=str, dest='output', help='output file or folder')

	args = parser.parse_args()

	_main(args)
