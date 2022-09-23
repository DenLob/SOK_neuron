import cv2
from detectron2.utils.visualizer import Visualizer


def get_category_bbox(predictMeta, im):

    predictor, metadata = predictMeta
    outputs = predictor(im)
    classesTensors = outputs['instances'].get('pred_classes')
    scoresTensors = outputs['instances'].get('scores')
    scoresIterTensors = scoresTensors.__iter__()
    scoresLen = scoresTensors.__len__()
    if(scoresLen > 1):                                  # Если найдено более одного бокса,
        max_score = -1                                  # то выбираем тот, у кого процент больше
        index = -1
        for i in range(0, scoresLen):
            current_score = next(scoresIterTensors)
            if(current_score > max_score):
                max_score = current_score
                index = i
        bbox_class = classesTensors[index]
    elif(scoresLen == 1):
        max_score = scoresTensors[0]
        bbox_class = classesTensors[0]
    if(scoresLen == 0):
        max_score = 0
        bbox_class = 'undefined'
        return [bbox_class, max_score]

    # v = Visualizer(im[:, :, ::-1],
    #                metadata=metadata,
    #                scale=1)
    #
    # v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    #
    # cv2.imshow('salad', v.get_image()[:, :, ::-1])
    # cv2.waitKey(0)

    return [metadata.__getattr__('class_names')[bbox_class.item()], max_score.item()]
