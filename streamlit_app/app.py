"""
🍅 Domates Yaprağı Hastalık Tanı Sistemi
Streamlit Web Uygulaması

Çalıştırma:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
import os
import sys

# utils klasöründeki modülleri import edebilmek için
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.disease_info import DISEASE_INFO, CLASS_ORDER, get_disease_info
from utils.gradcam import make_gradcam_heatmap, overlay_gradcam, find_last_conv_layer

# ============================================================
# SAYFA AYARLARI
# ============================================================
st.set_page_config(
    page_title="🍅 Domates Hastalık Teşhisi",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — Özel Stil
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #e74c3c;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #3498db;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# MODEL YÜKLEME (cache ile - hızlı)
# ============================================================
@st.cache_resource
def load_model():
    """Modeli yükler ve cache'ler."""
    model_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "models",
        "efficientnetb0_final.keras"
    )
    model = tf.keras.models.load_model(model_path)
    return model


# ============================================================
# TAHMİN FONKSİYONU
# ============================================================
def predict_disease(image, model):
    """
    Görüntü üzerinde tahmin yapar.
    
    Returns:
        predictions: Tüm sınıflar için olasılıklar
        top_class_idx: En yüksek olasılıklı sınıfın indeksi
        confidence: Güven skoru (%)
    """
    # Görüntüyü hazırla
    img_resized = image.resize((224, 224))
    img_array = np.array(img_resized).astype(np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    
    # EfficientNetB0 preprocessing
    img_processed = preprocess_input(img_array.copy())
    
    # Tahmin
    predictions = model.predict(img_processed, verbose=0)[0]
    top_class_idx = np.argmax(predictions)
    confidence = predictions[top_class_idx] * 100
    
    return predictions, top_class_idx, confidence, img_processed


# ============================================================
# ANA UYGULAMA
# ============================================================
def main():
    # Başlık
    st.markdown('<div class="main-header">🍅 Domates Yaprağı Hastalık Teşhis Sistemi</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ziraat Mühendisleri için Derin Öğrenme Tabanlı Karar Destek Sistemi</div>', 
                unsafe_allow_html=True)
    
    # ========================================================
    # KENAR ÇUBUĞU
    # ========================================================
    with st.sidebar:
        st.header("ℹ️ Hakkında")
        st.markdown("""
        Bu sistem, domates yapraklarındaki **9 farklı hastalığı** ve sağlıklı durumu 
        otomatik olarak tespit eder.
        
        **Model**: EfficientNetB0  
        **Doğruluk**: %96.55  
        **Boyut**: 30 MB
        """)
        
        st.divider()
        
        st.header("📋 Tanınan Hastalıklar")
        for cls_key in CLASS_ORDER:
            info = DISEASE_INFO[cls_key]
            st.markdown(f"• **{info['ad']}**")
        
        st.divider()
        
        st.header("⚙️ Ayarlar")
        show_gradcam = st.checkbox("Grad-CAM Görselleştirmesi", value=True,
                                    help="Modelin yaprağın hangi bölgesine baktığını gösterir")
        show_top3 = st.checkbox("Top-3 Tahmin Göster", value=True)
    
    # ========================================================
    # MODEL YÜKLE
    # ========================================================
    with st.spinner("🧠 Model yükleniyor..."):
        try:
            model = load_model()
        except Exception as e:
            st.error(f"❌ Model yüklenemedi: {e}")
            st.info("models/ klasöründe efficientnetb0_final.keras dosyasının olduğundan emin olun.")
            return
    
    # ========================================================
    # FOTOĞRAF YÜKLEME
    # ========================================================
    st.header("📸 1. Yaprak Fotoğrafı Yükleyin")
    
    uploaded_file = st.file_uploader(
        "Domates yaprağı fotoğrafı seçin (JPG, PNG)",
        type=['jpg', 'jpeg', 'png'],
        help="Net çekilmiş, tek bir yaprağın görüntüsü en iyi sonucu verir"
    )
    
    if uploaded_file is None:
        st.info("👆 Başlamak için bir yaprak fotoğrafı yükleyin.")
        return
    
    # ========================================================
    # GÖRÜNTÜYÜ İŞLE VE GÖSTER
    # ========================================================
    image = Image.open(uploaded_file).convert('RGB')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📷 Yüklenen Görüntü")
        st.image(image, use_container_width=True)
    
    # ========================================================
    # TAHMİN YAP
    # ========================================================
    with st.spinner("🔍 Analiz ediliyor..."):
        predictions, top_idx, confidence, img_processed = predict_disease(image, model)
    
    predicted_class = CLASS_ORDER[top_idx]
    info = get_disease_info(predicted_class)
    
    # ========================================================
    # SONUCU GÖSTER
    # ========================================================
    with col2:
        st.subheader("🎯 Teşhis Sonucu")
        
        # Ana sonuç kutusu
        st.markdown(f"""
        <div class="prediction-box">
            <h2 style="margin: 0;">{info['ad']}</h2>
            <h3 style="margin: 0.5rem 0;">Güven: %{confidence:.1f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Güven seviyesine göre uyarı
        if confidence > 90:
            st.success("✅ Yüksek güvenle teşhis edildi")
        elif confidence > 70:
            st.warning("⚠️ Orta güvenle teşhis edildi - bir uzmana danışın")
        else:
            st.error("❌ Düşük güven - fotoğrafı yeniden çekin veya uzmana başvurun")
    
    # ========================================================
    # TOP 3 TAHMİN
    # ========================================================
    if show_top3:
        st.divider()
        st.subheader("📊 En Olası 3 Sınıf")
        
        top3_indices = np.argsort(predictions)[-3:][::-1]
        
        cols = st.columns(3)
        for i, idx in enumerate(top3_indices):
            cls = CLASS_ORDER[idx]
            cls_info = DISEASE_INFO[cls]
            with cols[i]:
                st.metric(
                    label=f"#{i+1} {cls_info['ad']}",
                    value=f"%{predictions[idx]*100:.1f}"
                )
    
    # ========================================================
    # GRAD-CAM GÖRSELLEŞTİRMESİ
    # ========================================================
    if show_gradcam:
        st.divider()
        st.subheader("🔥 Grad-CAM: Model Nereye Bakıyor?")
        st.caption("Sıcak renkler (kırmızı/sarı) = Modelin dikkat ettiği bölgeler")
        
        try:
            with st.spinner("Grad-CAM hesaplanıyor..."):
                last_conv = find_last_conv_layer(model)
                heatmap = make_gradcam_heatmap(img_processed, model, last_conv, top_idx)
                gradcam_image = overlay_gradcam(image.resize((224, 224)), heatmap, alpha=0.5)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Orijinal**")
                st.image(image.resize((224, 224)), use_container_width=True)
            with col_b:
                st.markdown("**Grad-CAM**")
                st.image(gradcam_image, use_container_width=True)
        except Exception as e:
            st.warning(f"Grad-CAM oluşturulamadı: {e}")
    
    # ========================================================
    # HASTALIK BİLGİLERİ
    # ========================================================
    st.divider()
    st.subheader("📚 Hastalık Hakkında Bilgi")
    
    tab1, tab2, tab3 = st.tabs(["🔬 Etken & Belirtiler", "💊 Tedavi", "🛡️ Önlem"])
    
    with tab1:
        st.markdown(f"**Etken**: {info['etken']}")
        st.markdown("**Belirtiler**:")
        for belirti in info['belirtiler']:
            st.markdown(f"- {belirti}")
    
    with tab2:
        st.markdown("**Tedavi Önerileri**:")
        for tedavi in info['tedavi']:
            st.markdown(f"- {tedavi}")
    
    with tab3:
        st.markdown(f"**Önlem**: {info['onlem']}")
    
    # ========================================================
    # UYARI
    # ========================================================
    st.divider()
    st.info("""
    ⚠️ **Önemli Uyarı**: Bu sistem bir karar destek aracıdır ve uzman görüşünün yerini alamaz. 
    Kesin teşhis ve tedavi için bir ziraat mühendisine danışınız.
    """)


# ============================================================
# UYGULAMAYI BAŞLAT
# ============================================================
if __name__ == "__main__":
    main()