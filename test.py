# import cv2
# im_gray = cv2.imread("detail.jpg", cv2.IMREAD_GRAYSCALE)
#
# cv2.imshow("test", im_gray)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np
from matplotlib import pyplot as plt


def to_inches(sm):
    return sm / 2.54


image_width = to_inches(19)
image_height = to_inches(15)
camera_paper_height = to_inches(13.3)
reference_width = to_inches(1.5)
reference_height = to_inches(1)

img = cv2.imread('detail.jpg', 0)
height_px, width_px = img.shape[:2]
reference_width_px = int(width_px * (reference_width / image_width))
pixel_per_metric = int(reference_width_px / reference_width)

print("Original width (px) = " + str(width_px))
print("Original height  (px) = " + str(height_px))
print("Reference witdh (px) = " + str(reference_width_px))
print("Pixel metric (px) = " + str(pixel_per_metric))
# edges = cv2.Canny(img, 200, 500)
#
# plt.subplot(121), plt.imshow(img, cmap='gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(edges, cmap='gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()
