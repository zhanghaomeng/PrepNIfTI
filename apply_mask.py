import os
import argparse
import sys

import utils

def _apply_mask(image,mask,output):
	masked = utils.mask(image[0], mask[0], args.side)
	utils.save_file(masked, image[1], image[2], output)

def _apply_mask_file(args):
		image = utils.read_file(args.input)
		mask = utils.read_file(args.mask)
		_apply_mask(image,mask,args.output)

def _apply_mask_folder(args):
		imageFiles = []
		for file in os.listdir(args.input):
			imageFiles.append(file)
		for file in imageFiles:
			imagefilename = os.path.join(args.input,file)
			maskfilename = os.path.join(args.mask,file)
			outputfilename = os.path.join(args.output,file)
			# Skip if mask not available
			if not os.path.isfile(maskfilename):
				continue;

			image = utils.read_file(imagefilename)
			mask = utils.read_file(maskfilename)
			_apply_mask(image,mask,outputfilename)

def _main(args):
	if args.file:
		_apply_mask_file(args)
	elif args.folder:
		_apply_mask_folder(args)
	else:
		print('choose file or folder')

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--file', action='store_true', dest='file', help='process a file')
	parser.add_argument('--folder', action='store_true', dest='folder', help='process all eligible files in a folder')
	parser.add_argument('--input', required = True, type=str, dest='input', help='input file or folder')
	parser.add_argument('--output', required = True, type=str, dest='output', help='output file or folder')

	parser.add_argument('--mask', required = True, type=str, dest='mask', help=('mask file or folder'
					'it should be in a different folder and has the same name with the image.'))
	
	parser.add_argument('--side', type=str, dest='side', help='entire, left, or right', default='entire')
	args = parser.parse_args()

	_main(args)
