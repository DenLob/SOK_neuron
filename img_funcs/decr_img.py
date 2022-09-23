import cv2

def resize_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    # resize image
    result = cv2.resize(image, dsize)


    return ([{'width': width, 'height': height}, result])

def scale_point(oldPoint, scale_percent):
    x = int(oldPoint[0] * scale_percent / 100)
    y = int(oldPoint[1] * scale_percent / 100)
    return [x, y]


def new_coordinates(oldArr, scale_percent):
    oldPoints = [
        [oldArr[0], oldArr[1]],
        [oldArr[2], oldArr[1]],
        [oldArr[0], oldArr[3]],
        [oldArr[2], oldArr[3]]
    ]

    newArr = []
    for point in oldPoints:
        newArr.append(scale_point(point, scale_percent))
    x_min = newArr[0][0]
    y_min = newArr[0][1]
    x_max = newArr[0][0]
    y_max = newArr[0][1]
    for i, item in enumerate(newArr):
        if (newArr[i][0] < x_min): x_min = newArr[i][0]
        if (newArr[i][1] < y_min): y_min = newArr[i][1]
        if (newArr[i][0] > x_max): x_max = newArr[i][0]
        if (newArr[i][1] > y_max): y_max = newArr[i][1]
    return [x_min, y_min, x_max, y_max]
