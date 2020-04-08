# Simple Scanner using OpenCV with Python

It scans the images provided then detects the four corners of the image. Then apply [**Bird's eye view**](https://en.wikipedia.org/wiki/Bird%27s-eye_view) matrix on it to transform the perspective.

### Original Image
![origin](https://imgur.com/Cgb9UwN.jpg)
### Edge
![edge](https://imgur.com/Ezmo3nM.png)
### Contour
![contour](https://imgur.com/tB3SwBv.png)
### Scanned
![scanned](https://imgur.com/UKJ0qRH.png)


## Installation

`$ pip install opencv-python imutils scikit-image`

## Known Bugs

Sometimes, `screenContour` is not defined since it could not be captured. Play around with `cv2.approxPolyDP()` with the value between 0.01 ~ 0.05 (1% ~ 5%). 

`screenContour` might not capture the image perfectly due to lighting and angles, make sure the images to be scanned are well lit and the doc is the only object in the image. 
