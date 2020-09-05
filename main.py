from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import imutils
import cv2

from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import os
import shutil

import numpy as np
from skimage.transform import resize

original_image = imread("/content/drive/My Drive/MY_Work/car6.jpg", as_gray=True)
print(original_image.shape)

gray_image = original_image * 255
fig, (AxesSubplot1, AxesSubplot2) = plt.subplots(1, 2)
AxesSubplot1.imshow(gray_image, cmap="gray")
threshold_value = threshold_otsu(gray_image)
binary_image = gray_image > threshold_value
AxesSubplot2.imshow(binary_image, cmap="gray")
plt.show()
label_img = measure.label(binary_image)
num_plate_dim = (0.03*label_img.shape[0], 0.08*label_img.shape[0], 0.15*label_img.shape[1], 0.3*label_img.shape[1])
num_plate_dim2 = (0.08*label_img.shape[0], 0.2*label_img.shape[0], 0.15*label_img.shape[1], 0.4*label_img.shape[1])
min_height, max_height, min_width, max_width = num_plate_dim
plate_coordinates = []
plate_as_object = []
fig, (AxesSubplot1) = plt.subplots(1)
AxesSubplot1.imshow(gray_image, cmap="gray")
flag =0
for region in regionprops(label_img):
    if region.area < 50:
         # print("there is no licence plate found...: 1 ")
        continue
    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        flag = 1
        plate_as_object.append(binary_image[min_row:max_row,
                                  min_col:max_col])
        plate_coordinates.append((min_row, min_col,
                                        max_row, max_col))
        rectegular_Border = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                      linewidth=2, fill=False)
        AxesSubplot1.add_patch(rectegular_Border)
if (flag == 1):
    plt.show()

if (flag==0):
    min_height, max_height, min_width, max_width = num_plate_dim2
    plate_coordinates = []
    plate_as_object = []

    fig, (AxesSubplot1) = plt.subplots(1)
    AxesSubplot1.imshow(gray_image, cmap="gray")

    for region in regionprops(label_img):
        if region.area < 50:
             # print("there is no licence plate found...: 2")
            continue
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col
        
        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            plate_as_object.append(binary_image[min_row:max_row,
                                      min_col:max_col])
            plate_coordinates.append((min_row, min_col,
                                            max_row, max_col))
            rectegular_Border = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                          linewidth=2, fill=False)
            AxesSubplot1.add_patch(rectegular_Border)
    plt.show()
    print(plate_as_object)

'''-----------------------------'''
if len(plate_as_object) == 0:
    print('No vehicle is Found, Check your image agin')
else:
  license_plate = np.invert(plate_as_object[0])

  labelled_plate = measure.label(license_plate)

  fig, AxesSubplot1 = plt.subplots(1)
  AxesSubplot1.imshow(license_plate, cmap="gray")
  character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
  min_height, max_height, min_width, max_width = character_dimensions

  characters = []
  counter=0
  column_list = []
  for regions in regionprops(labelled_plate):
      y0, x0, y1, x1 = regions.bbox
      region_height = y1 - y0
      region_width = x1 - x0

      if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
          roi = license_plate[y0:y1, x0:x1]

          # draw a red bordered rectangle over the character.
          rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                        linewidth=2, fill=False)
          AxesSubplot1.add_patch(rect_border)

          # resize the characters to 20X20 and then append each character into the characters list
          resized_char = resize(roi, (20, 20))
          characters.append(resized_char)

          # this is just to keep track of the arrangement of the characters
          column_list.append(x0)
  print(character_dimensions)
  plt.show()
  plt.imshow(license_plate)
  plt.show()
img = license_plate.copy()                              
result = pytesseract.image_to_string(img)
print(result)
