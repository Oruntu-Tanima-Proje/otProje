# 🍅 Domates Yaprak Hastalık Tanı Destek Sistemi

> **Ziraat Mühendisleri İçin Derin Öğrenme Tabanlı Domates Yaprak Hastalık Tanı Destek Sistemi**

Bu proje, domates yapraklarındaki 9 farklı hastalığı ve sağlıklı durumu tanımak üzere 3 farklı CNN mimarisini (MobileNetV2, ResNet50, EfficientNetB0) eğiten ve karşılaştıran bir derin öğrenme sistemidir.

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Veri Seti](#-veri-seti)
- [Kullanılan Modeller](#-kullanılan-modeller)
- [Sonuçlar](#-sonuçlar)
- [Proje Yapısı](#-proje-yapısı)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Eğitilmiş Modeller](#-eğitilmiş-modeller)
- [Teknik Detaylar](#-teknik-detaylar)
- [Geliştirme Süreci](#-geliştirme-süreci)
- [Ekip](#-ekip)

---

## 🎯 Proje Hakkında

Tarımda hastalık tespiti, ürün kayıplarını önlemek için kritik bir öneme sahiptir. Bu proje, ziraat mühendislerine ve çiftçilere derin öğrenme destekli bir karar destek sistemi sunmayı amaçlamaktadır.

### Amaç
- Domates yapraklarındaki hastalıkları **otomatik olarak** tespit etmek
- 3 farklı CNN mimarisini **karşılaştırmak**
- **Açıklanabilir AI** (Grad-CAM) ile model kararlarını görselleştirmek
- Ziraat uzmanları için **kullanıcı dostu bir arayüz** sağlamak

### Tanınan Hastalıklar
1. Bakteriyel Leke (Bacterial Spot)
2. Erken Yaprak Yanıklığı (Early Blight)
3. Geç Yaprak Yanıklığı (Late Blight)
4. Yaprak Küfü (Leaf Mold)
5. Septorya Yaprak Lekesi (Septoria Leaf Spot)
6. Kırmızı Örümcek Hasarı (Spider Mites)
7. Hedef Leke (Target Spot)
8. Sarı Yaprak Kıvırcıklığı Virüsü (Yellow Leaf Curl Virus)
9. Mozaik Virüsü (Mosaic Virus)
10. Sağlıklı (Healthy)

---

## 📊 Veri Seti

- **Kaynak**: [New Plant Diseases Dataset (Augmented)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- **Sınıf Sayısı**: 10 (9 hastalık + sağlıklı)
- **Toplam Görüntü**: 22.930
- **Görüntü Boyutu**: 256x256 RGB

### Veri Dağılımı

| Set | Görüntü Sayısı |
|-----|----------------|
| Train (Eğitim) | 18.345 |
| Valid (Doğrulama) | 2.295 |
| Test | 2.290 |
| **Toplam** | **22.930** |

> Sınıflar dengeli dağılıma sahiptir (dengesizlik oranı: ~1.15)

---

## 🧠 Kullanılan Modeller

3 farklı transfer learning mimarisi kullanılmıştır:

| Model | Yıl | Parametre | Boyut | Mimari Felsefesi |
|-------|-----|-----------|-------|------------------|
| **MobileNetV2** | 2018 | 2.4M | 22 MB | Mobil/edge cihazlar için hafiflik |
| **ResNet50** | 2015 | 24M | 204 MB | Skip connections ile derinlik |
| **EfficientNetB0** | 2019 | 5.3M | 30 MB | Compound scaling ile verim-doğruluk dengesi |

### Eğitim Stratejisi (3 model için ortak)

İki aşamalı transfer learning yaklaşımı:

**Phase 1: Feature Extraction**
- ImageNet ön-eğitimli ağırlıklar yüklenir
- Base model **donmuş** durumda
- Sadece üst katmanlar (GlobalAveragePooling + Dense) eğitilir
- Learning Rate: `1e-3`

**Phase 2: Fine-Tuning**
- Base modelin **son 30 katmanı** açılır
- Çok düşük learning rate ile ince ayar
- Learning Rate: `1e-5`

### Veri Artırma (Data Augmentation)
- Rotasyon: ±20°
- Yatay/dikey kaydırma: ±10%
- Yatay çevirme: Etkin
- Zoom: ±10%

### Callbacks
- **ModelCheckpoint**: En iyi val_accuracy'ye sahip modeli kaydet
- **EarlyStopping**: Patience=4-7 epoch
- **ReduceLROnPlateau**: Plato durumunda LR'yi yarıya indir

---

## 🏆 Sonuçlar

### Test Seti Performansı

| Model | Test Acc | F1-Score | Precision | Recall | Boyut |
|-------|----------|----------|-----------|--------|-------|
| MobileNetV2 | %92.40 | 0.9242 | 0.9282 | 0.9240 | 22.74 MB |
| **ResNet50** ⭐ | **%98.65** | **0.9865** | **0.9866** | **0.9865** | 203.90 MB |
| EfficientNetB0 | %96.55 | 0.9657 | 0.9664 | 0.9655 | 29.58 MB |

### 🎯 Öneriler

| Senaryo | Önerilen Model | Sebep |
|---------|----------------|-------|
| Maksimum doğruluk | **ResNet50** | %98.65 accuracy |
| Doğruluk-hız dengesi | **EfficientNetB0** ⭐ | İyi denge, modern mimari |
| Mobil/Edge cihaz | **MobileNetV2** | Hafiflik, 22 MB |

### Görsel Sonuçlar

Tüm karşılaştırma grafikleri ve Grad-CAM analizleri `notebooks/06_karsilastirma.ipynb` ve `notebooks/07_gradcam_analizi.ipynb` dosyalarında bulunabilir.

---

## 📁 Proje Yapısı

```
