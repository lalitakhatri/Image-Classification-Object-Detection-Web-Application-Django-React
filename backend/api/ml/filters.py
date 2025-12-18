import cv2
import numpy as np


def apply_filter(img, filter_name):
    """Apply various image filters to the input image."""
    
    if filter_name == "grayscale":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif filter_name == "blur":
        return cv2.GaussianBlur(img, (7, 7), 0)

    elif filter_name == "canny":
        return cv2.Canny(img, 100, 200)

    elif filter_name == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        return cv2.transform(img, kernel)

    elif filter_name == "negative":
        return cv2.bitwise_not(img)

    elif filter_name == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)

    elif filter_name == "emboss":
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        return cv2.filter2D(img, -1, kernel)

    elif filter_name == "median":
        return cv2.medianBlur(img, 5)

    elif filter_name == "bilateral":
        return cv2.bilateralFilter(img, 9, 75, 75)

    elif filter_name == "threshold":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return th

    elif filter_name == "sobel":
        return cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)

    elif filter_name == "laplacian":
        return cv2.Laplacian(img, cv2.CV_64F)

    elif filter_name == "hsv":
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    elif filter_name == "erosion":
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(img, kernel)

    elif filter_name == "dilation":
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(img, kernel)

    elif filter_name == "edge_enhance":
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        return cv2.filter2D(img, -1, kernel)

    return img
