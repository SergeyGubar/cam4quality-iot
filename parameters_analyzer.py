from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


image_width = 19
image_height = 15
camera_paper_height = 13.3
reference_width = 1.5
reference_height = 1


def get_params(img):
    image = cv2.imread(img)

    height_px, width_px = image.shape[:2]
    reference_width_px = int(width_px * (reference_width / image_width))
    pixel_per_metric = None

    print("Original width (px) = " + str(width_px))
    print("Original height  (px) = " + str(height_px))
    print("Reference witdh (px) = " + str(reference_width_px))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)
    cnts = (list(filter(lambda cnt: cv2.contourArea(cnt) > 100, cnts)))
    print("Number of filtered counters: " + str(len(cnts)))
    for index, c in enumerate(cnts):
        # compute the rotated bounding box of the contour
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        distance_height = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        distance_width = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        if pixel_per_metric is None:
            pixel_per_metric = distance_width / reference_width

        width = distance_width / pixel_per_metric
        print("Got object dimenison (width): " + str(width))
        height = distance_height / pixel_per_metric
        print("Got object dimenison (height): " + str(height))

        if index == 1:
            result = [width, height]
            return result
