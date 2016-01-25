import cv2
#cap = cv2.VideoCapture(0)
img = cv2.imread("1927.jpg", cv2.CV_LOAD_IMAGE_COLOR)
print img
cv2.startWindowThread()
cv2.namedWindow("preview")
cv2.imshow("preview", img)
cv2.waitKey(5000)