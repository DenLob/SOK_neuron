from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import Metadata


def bbox_ph_init():
    detectron2_repo = 'D:/detectron2/detectron_repo'
    sample_metadata = Metadata()
    thing_classes = ['bad', 'fall', 'good', 'smallbad']
    thing_dataset_id_to_contiguous_id = {0: 0, 1: 1, 2: 2, 3: 3}
    sample_metadata.set(thing_classes=thing_classes,
                        thing_dataset_id_to_contiguous_id=thing_dataset_id_to_contiguous_id)

    cfg = get_cfg()
    cfg.merge_from_file(detectron2_repo + "configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model

    # cfg.MODEL.DEVICE = 'cpu'
    cfg.MODEL.WEIGHTS = "./weights/bboxes_photo_weights.pth"

    predictor = DefaultPredictor(cfg)
    return [predictor, sample_metadata]
