import cv2

from os import path
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]



def cut_image(img, new_width, new_height, oldCoordinates):
    result = img[oldCoordinates[1]:oldCoordinates[1] + new_height,
             oldCoordinates[0]:oldCoordinates[0] + new_width
             ]

    return result


def new_points(oldPoints, newImg_xmax, newImg_ymax, newImg_width):
    if (newImg_xmax != 0):
        x_min = oldPoints[0][0] - (newImg_xmax - newImg_width)
        y_min = oldPoints[0][1] - (newImg_ymax - newImg_width)
        x_max = oldPoints[1][0] - (newImg_xmax - newImg_width)
        y_max = oldPoints[2][1] - (newImg_ymax - newImg_width)
    else:
        x_min = oldPoints[0][0]
        y_min = oldPoints[0][1]
        x_max = oldPoints[0][0]
        y_max = oldPoints[0][1]
        for i, item in enumerate(oldPoints):
            if (oldPoints[i][0] < x_min): x_min = oldPoints[i][0]
            if (oldPoints[i][1] < y_min): y_min = oldPoints[i][1]
            if (oldPoints[i][0] > x_max): x_max = oldPoints[i][0]
            if (oldPoints[i][1] > y_max): y_max = oldPoints[i][1]
    if (newImg_width == 0):
        new_width = x_max - x_min
        x_min = 1
        x_max = x_min + new_width - 2
        new_height = y_max - y_min
        y_min = 1
        y_max = y_min + new_height - 2
    else:
        new_width = newImg_width
        new_height = newImg_width
    return ({'bboxes': [x_min, y_min, x_max, y_max],
             'width': new_width,
             'height': new_height
             })


def newCoordinates(oldCoordinates, origImg, newImg_xmax=0, newImg_ymax=0,
                   newImg_width=0):
    oldPoints = [
        [oldCoordinates[0], oldCoordinates[1]],
        [oldCoordinates[2], oldCoordinates[1]],
        [oldCoordinates[0], oldCoordinates[3]],
        [oldCoordinates[2], oldCoordinates[3]]
    ]

    newData = new_points(oldPoints, newImg_xmax, newImg_ymax, newImg_width)
    newBboxes = newData['bboxes']
    new_width = newData['width']
    new_height = newData['height']
    if (newImg_xmax == 0):
        newImg = cut_image(origImg, new_width, new_height, oldCoordinates)
    else:
        oldCoordinates[0] = newImg_xmax - newImg_width
        oldCoordinates[1] = newImg_ymax - newImg_width
        newImg = cut_image(origImg, new_width, new_height, oldCoordinates)

    return ({
        'bboxes': newBboxes,
        'width': new_width,
        'height': new_height,
        'newImg': newImg
    })


def cutBbox(origImg, bnd_box):


    newData = newCoordinates(
        bnd_box,
        origImg
    )
    return newData['newImg']

