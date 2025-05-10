from PIL import Image
import torch
from transformers import YolosFeatureExtractor, YolosForObjectDetection

# Load model and feature extractor
feature_extractor = YolosFeatureExtractor.from_pretrained(r"D:\CollegeWork\ShopLens-AR-Shopping-Assistant\yolo_small")
model = YolosForObjectDetection.from_pretrained(r"D:\CollegeWork\ShopLens-AR-Shopping-Assistant\model")

def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def get_detections(image: Image.Image, threshold=0.3):

    # image = image.convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Compute class probabilities and filter by threshold
    probas = outputs.logits.softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > threshold

    # Rescale bounding boxes to image dimensions
    boxes = rescale_bboxes(outputs.pred_boxes[0, keep].cpu(), image.size)
    labels = probas[keep].argmax(-1).tolist()

    return image, boxes, labels
