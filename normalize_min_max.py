import os
import argparse
import sys

import utils

def _normalize(image,output):
	normalized = utils.min_max_normalize(image[0])
	utils.save_file(normalized, image[1], image[2], output)

def _normalize_file(args):
		image = utils.read_file(args.input)
		_normalize(image,args.output)

def _normalize_folder(args):
		imageFiles = []
		for file in os.listdir(args.input):
			imageFiles.append(file)
		for file in imageFiles:
			imagefilename = os.path.join(args.input,file)
			outputfilename = os.path.join(args.output,file)

			image = utils.read_file(imagefilename)
			_normalize(image,outputfilename)

def _main(args):
	if args.file:
		_normalize_file(args)
	elif args.folder:
		_normalize_folder(args)
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
