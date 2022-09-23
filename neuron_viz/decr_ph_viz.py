import cv2
from detectron2.utils.visualizer import Visualizer


def get_bboxes(predictMeta, im):

    predictor, metadata = predictMeta
    outputs = predictor(im)
    detectronBoxesTensors = outputs['instances'].get('pred_boxes')
    boxesIterTensors = detectronBoxesTensors.__iter__()
    boxesLen = detectronBoxesTensors.__len__()
    bboxes = []

    for i in range(0, boxesLen):
        bboxes.append(next(boxesIterTensors))


    # v = Visualizer(im[:, :, ::-1],
    #                metadata=metadata,
    #                scale=1)
    #
    # v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    #
    # cv2.imshow('salad', v.get_image()[:, :, ::-1])
    # cv2.waitKey(0)

    return bboxes
