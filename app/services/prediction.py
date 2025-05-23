from matplotlib import cm
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt

classifier = load_model('app/ml_models/classifier.keras')
segmenter = load_model('app/ml_models/best_segmenter_3.keras')

def get_prediction(image):
  size = image.shape
  mel = round(float(classifier.predict(np.expand_dims(cv2.resize(image, (224, 224)).astype('float32') / 255.0, axis=0))[0][1]), 3)
  segmentation = segmenter.predict(np.expand_dims(cv2.resize(image, (128, 128)).astype('float32') / 255.0, axis=0))[0]
  segmentation = (segmentation > 0.5).astype(np.uint8)
  segmentation = cv2.resize(segmentation, (size[1], size[0]))
  return mel, segmentation

def generate_segmentation(segmentation):
    mask = segmentation.astype(np.float32)
    if mask.max() > 1:
        mask = mask / 255.0
    colormap = cm.get_cmap('viridis')
    colored_mask = colormap(mask) 
    colored_mask = (colored_mask[:, :, :3] * 255).astype(np.uint8) 
    colored_mask_bgr = cv2.cvtColor(colored_mask, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', colored_mask_bgr)
    return buffer.tobytes()