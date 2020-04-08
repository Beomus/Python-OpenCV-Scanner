import numpy as np
import cv2


def order_points(points):
	"""
	This function takes in only one parameter which is a list of 
	(x, y) coordinates to re-order them into
	top-left => top-right => bottom-right => bottom-left
	"""
	rect = np.zeros((4,2), dtype = 'float32')

	"""
	For the math here to make sense, we will assume that the image
	will be a vertical image instead of a horizontal image
	"""

	# sum by each row
	s = points.sum(axis=1)

	# top left will always have the smallest sum
	rect[0] = points[np.argmin(s)]
	# bottom right will always have the largest sum
	rect[2] = points[np.argmax(s)]

	# difference between the coordinate
	d = np.diff(points, axis=1)

	# top right coordinate will have the smallest difference
	rect[1] = points[np.argmin(d)]
	rect[3] = points[np.argmax(d)]

	# return the coordinate in order
	return rect


def transform_four_points(image, points):
	# obtain the order of points
	rect = order_points(points)
	(tl, tr , br, bl) = rect

	# calculating the width of the new image
	# which is max distance between the x coordiantes of 
	# (tl and tr) or between the (br and bl)
	width_top = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	# or an easier way but less accurate:
	# width_top = (abs(br[0] - bl[0]) + abs(br[1] - bl[1]))
	width_bot = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	max_width = max(int(width_top), int(width_bot))

	# the same goes for the height 
	# but it will be depending on the y coordinates
	height_right = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	height_left = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	max_height = max(int(height_left), int(height_right))


	"""
	Once we obtained the new dimension for the new image
	we can construct a new set of points to get the bird's eye view
	of the image in the respective order of the points
	"""
	pts = np.array([
		[0, 0],
		[max_width - 1, 0],
		[max_width - 1, max_height -1],
		[0, max_height - 1]], dtype='float32')

	# apply cv2 perspective transform matrix
	matrix = cv2.getPerspectiveTransform(rect, pts)
	warped_img = cv2.warpPerspective(image, matrix, (max_width, max_height))

	# return the warped image
	return warped_img
	