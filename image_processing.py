import cv2
import numpy as np


def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def detect_edges(image):
    gray = convert_to_grayscale(image)
    blurred = apply_blur(gray)
    return cv2.Canny(blurred, 100, 200)


def apply_threshold(image):
    gray = convert_to_grayscale(image)
    _, threshold = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY
    )
    return threshold