from transform import transform_four_points
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
import os


file_path = 'images/'

saves = 'modified/'
if not os.path.isdir(saves):
	os.mkdir(saves)

for file in os.listdir(file_path):
	print(f'[INFO] Processing image {file}')
	# loading the image and resizing it 
	image = cv2.imread(f'{file_path}/{file}')
	ratio = image.shape[0] / 500.0
	origin = image.copy()

	image = imutils.resize(image, height = 500)

	# convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edge = cv2.Canny(gray, 75, 200)

	# show the original and the edged image
	print('[INFO] Detecting...')
	cv2.imshow("Origin", origin)
	cv2.imshow("Edge", edge)
	cv2.waitKey(0)
	cv2.imwrite(f"{saves}edge.png", edge)
	cv2.destroyAllWindows()


	# finding all the contours and filter out the smaller ones
	# keeping the largest one for the corners coordinates

	contours = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

	for contour in contours:
		# approximate the contours
		peri = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.05 * peri, True)

		if len(approx) == 4:
			screenContour = approx
			break

	# showing the contours on the image
	print('[INFO] Detecting contours....')
	cv2.drawContours(image, [screenContour], -1, (0, 0, 255), 2)
	cv2.imshow("Contour", image)
	cv2.waitKey(0)
	cv2.imwrite(f"{saves}contour.png", image)
	cv2.destroyAllWindows()


	# apply the bird's eye view to the image
	warped = transform_four_points(origin, screenContour.reshape(4, 2) * ratio)

	# convert the image to grayscale, then threshold it 
	# to give the 'black and white' paper effect

	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	threshold = threshold_local(warped, 11, offset=10, method='gaussian')
	warped = (warped > threshold).astype('uint8') * 255

	#show the orignal and the scanned image
	print("[INFO] Applying the transformation...")
	cv2.imshow("Original", imutils.resize(origin, height=600))
	cv2.imshow("Scanned", imutils.resize(warped, height=600))
	cv2.waitKey(0)
	cv2.imwrite(f"{saves}scanned.png", imutils.resize(warped, height=600))
	cv2.destroyAllWindows()


