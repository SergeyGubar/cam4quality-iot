import cv2
import numpy as np


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