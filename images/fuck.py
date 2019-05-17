import cv2
 
image = cv2.imread("Test.png")

cv2.imshow("Test image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()