import numpy as np
import os
import nibabel as nib


def read_file(file_path):
	file = nib.load(file_path)
	return file.get_data(), file.affine, file.header


# flag: 'left', 'right' or 'entrie'
def mask(image, mask, flag):

	mask_img = np.zeros_like(mask)

	if flag == 'entire':
		mask_img[mask > 0] = 1.0
	elif flag == 'left':
		mask_img[mask > 1] = 1.0
		mask_img[mask > 40] = 0.0
	elif flag == 'right':
		mask_img[mask > 40] = 1.0
	else:
		print('Please enter \'entire\', \'left\' or \'right\'')


	masked_img = image * mask_img

	return masked_img


def min_max_normalize(image, percentiles=0, set_min=-1, set_max=1):
	minimum = np.percentile(image, 0+percentiles)
	maximum = np.percentile(image, 100-percentiles)

	normalized = (np.divide((image-minimum), maximum-minimum)*(set_max-set_min)+set_min)

	normalized[normalized < set_min] = set_min
	normalized[normalized > set_max] = set_max

	return normalized

def sum_normalize(image, affine, header):
	image_sum = np.sum(left_img, dtype=np.float32)
	normalized = np.divide(image, image_sum)

	return normalized

def save_file(image, affine, header, file_path):
	file = nib.Nifti1Image(image, affine, header)
	nib.save(file, file_path)

