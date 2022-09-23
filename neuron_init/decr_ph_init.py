from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import Metadata


def decr_ph_init():
    detectron2_repo = 'D:/detectron2/detectron_repo'
    sample_metadata = Metadata()
    sample_metadata.set(thing_classes=['salad'])

    cfg = get_cfg()
    cfg.merge_from_file(detectron2_repo + "configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model

    # cfg.MODEL.DEVICE = 'cpu'
    cfg.MODEL.WEIGHTS = "./weights/decreased_photo_weights.pth"

    predictor = DefaultPredictor(cfg)
    return [predictor, sample_metadata]
