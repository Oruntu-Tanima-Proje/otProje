"""
Grad-CAM (Gradient-weighted Class Activation Mapping)
Modelin görüntünün hangi bölgesine baktığını ısı haritası olarak gösterir.
"""

import numpy as np
import tensorflow as tf
import matplotlib.cm as cm
from PIL import Image


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """
    Grad-CAM ısı haritası oluşturur.
    
    Args:
        img_array: Önişlenmiş görüntü tensoru (1, H, W, 3)
        model: Eğitilmiş Keras modeli
        last_conv_layer_name: Son convolutional katmanın adı
        pred_index: Tahmin edilen sınıf indeksi (None ise otomatik)
    
    Returns:
        heatmap: Numpy array, 0-1 arası normalize
    """
    grad_model = tf.keras.models.Model(
        model.inputs,
        [model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
    
    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # 0-1 arası normalize
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
    return heatmap.numpy()


def overlay_gradcam(original_image, heatmap, alpha=0.4):
    """
    Heatmap'i orijinal görüntüye bindiri.
    
    Args:
        original_image: PIL Image veya numpy array (H, W, 3)
        heatmap: Grad-CAM heatmap (h, w) — 0-1 arası
        alpha: Şeffaflık (0-1)
    
    Returns:
        Bindirilmiş görüntü (numpy array)
    """
    # PIL ise numpy'a çevir
    if isinstance(original_image, Image.Image):
        original_image = np.array(original_image)
    
    # Heatmap'i orijinal boyuta resize et
    h, w = original_image.shape[:2]
    heatmap_uint8 = np.uint8(255 * heatmap)
    
    # Jet colormap uygula
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap_uint8]
    
    # PIL ile resize
    jet_heatmap = Image.fromarray(np.uint8(jet_heatmap * 255)).resize((w, h))
    jet_heatmap = np.array(jet_heatmap)
    
    # Bindiri
    superimposed = jet_heatmap * alpha + original_image * (1 - alpha)
    return np.uint8(superimposed)


def find_last_conv_layer(model):
    """
    Modeldeki son convolutional katmanı otomatik bul.
    EfficientNetB0 için 'top_conv' döner.
    """
    for layer in reversed(model.layers):
        if 'conv' in layer.name.lower() or 'Conv' in layer.name:
            return layer.name
    return None