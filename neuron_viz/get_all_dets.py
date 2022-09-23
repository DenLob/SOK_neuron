"""
            list_all_dets =
            [
                {
                    disease: disease,
                    accuracy: accuracy,
                    coordinates: 'x_min,y_min;x_max,y_max'
                },
                {}
            ...]
    """
import cv2

from img_funcs.cut_bboxes import cutBbox
from img_funcs.decr_img import resize_img, new_coordinates
from neuron_viz.bbox_ph_viz import get_category_bbox
from neuron_viz.decr_ph_viz import get_bboxes


def list_all_dets(decrPredictorMeta, bboxPredictorMeta, orig_img_path):

    origImg = cv2.imread(orig_img_path)
    decrSize, decrImg = resize_img(origImg, 10)                         # Уменьшаем в 10 раз исходное фото
    decrBboxes = get_bboxes(decrPredictorMeta, decrImg)                 # Находим все салаты на уменьшенной фотке

    full_all_dets = []
    for i in range(0, len(decrBboxes)):
        incrBox = (new_coordinates(decrBboxes[i], 1000))                # Вычисляем координаты салата на исходном фото
        bboxImg = cutBbox(origImg, incrBox)                             # Вырезаем салат
        diseaseName, accuracy = get_category_bbox(bboxPredictorMeta, bboxImg)
        newDiseaseCase = dict([
            (
                'disease',
                diseaseName
            ),
            (
                'accuracy',
                round(100 * accuracy, 2)
            ),
            (
                'coordinates',
                str(incrBox[0]) + ',' + str(incrBox[1]) +
                ';' +
                str(incrBox[2]) + ',' + str(incrBox[3])
            )
        ])
        if len(newDiseaseCase) != 0:
            full_all_dets.append(newDiseaseCase)
    return full_all_dets