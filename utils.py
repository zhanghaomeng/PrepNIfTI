import numpy as np
import os
import nibabel as nib


def read_file(file_path):
	file = nib.load(file_path)
	return file.get_data(), file.affine, file.header


def flip(image):
	flipped = np.flip(image, 0)
	return flipped

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


def crop_coors(image, min_coors, max_coors):
	xmin, ymin, zmin = min_coors
	xmax, ymax, zmax = max_coors

	x = slice(min_coors[0], max_coors[0])
	y = slice(min_coors[1], max_coors[1])
	z = slice(min_coors[2], max_coors[2])

	print(min_coors[0])

	cropped = image[x, y, z]

	return cropped

def crop_size(image, target_size, offset=None):
	if offset is None:
		offset = (0, 0, 0)

	origin_x, origin_y, origin_z = image.shape
	target_x, target_y, target_z = target_size


	output = np.amin(image)*np.ones((target_x, target_y, target_z))

	dx = abs(target_x-origin_x) // 2 + offset[0]
	dy = abs(target_y-origin_y) // 2 + offset[1]
	dz = abs(target_z-origin_z) // 2 + offset[2]

	origin_ranges = []
	target_ranges = []

	for o, t, d in zip([origin_x, origin_y, origin_z], [target_x, target_y, target_z], [dx, dy, dz]):
		if t < o:
			origin_range = slice(d, d+t)
			target_range = slice(t)
		else:
			origin_range = slice(o)
			target_range = slice(d, d+o)

		origin_ranges.append(origin_range)
		target_ranges.append(target_range)

	output[target_ranges[0], target_ranges[1], target_ranges[2]] = image[origin_ranges[0], origin_ranges[1], origin_ranges[2]]

	return output



def save_file(image, affine, header, file_path):
	file = nib.Nifti1Image(image, affine, header)
	nib.save(file, file_path)

