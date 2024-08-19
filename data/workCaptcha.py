import cv2
import numpy as np
from data.paths import*

def resultImage():
    image = cv2.imread(screenSot)
    templates = [cv2.imread(ip) for ip in template_files]
    image = getLargeImage(getLargeImage(image))
    images = imageCutNat(image)
    return findImageCurrect(images, templates)

   
def findImageCurrect(images, templates):
    angles = []
    for i, img in enumerate(images):
        skew = calculate_skew(img, templates)
        angles.append((skew, i + 1, img))
    angles.sort(key=lambda x: abs(x[0]))
    return angles[0][1]

def calculate_skew(image, templates):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    best_match = 0
    best_score = 0
    for template in templates:
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        _, binary_template = cv2.threshold(gray_template, 200, 255, cv2.THRESH_BINARY_INV)
        result = cv2.matchTemplate(binary, binary_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > best_score:
            best_score = max_val
            best_match = gray_template
    angle = (1 - best_score) * 180  
    return angle


def getLargeImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_image = image[y:y+h, x:x+w]
    height, width = cropped_image.shape[:2]
    b = 1
    cropped_image = cropped_image[b:height-b, b:width-b]
    return cropped_image

def imageCutNat(image):
    height, width = image.shape[:2]
    part_height = height // 2
    part_width = width // 3
    parts = []
    for i in range(2):
        for j in range(3):
            x = j * part_width
            y = i * part_height
            part = image[y:y + part_height, x:x + part_width]
            parts.append(part)
    return parts


