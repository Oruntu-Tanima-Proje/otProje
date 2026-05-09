# 🍅 Domates Yaprak Hastalık Tanı Sistemi

Domates yapraklarındaki **9 farklı hastalığı** ve sağlıklı durumu tespit eden derin öğrenme projesi. **Baseline CNN** ile **3 transfer learning modeli** karşılaştırılmıştır.

> **Örüntü Tanıma Dersi** — Final Projesi

---

## 🎯 Amaç

Ziraat mühendisleri ve çiftçiler için domates hastalıklarını otomatik tespit eden bir karar destek sistemi geliştirmek.

---

## 📊 Veri Seti

- **Kaynak**: [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- **Toplam**: 22.930 görüntü
- **Sınıf**: 10 (9 hastalık + sağlıklı)
- **Dağılım**: Train 18.345 / Valid 2.295 / Test 2.290

---

## 🧠 Modeller ve Sonuçlar

| Model | Test Accuracy | F1-Score | Boyut | Yaklaşım |
|-------|---------------|----------|-------|----------|
| Baseline CNN | %85.76 | 0.8571 | 39.61 MB | Sıfırdan eğitim |
| MobileNetV2 | %92.40 | 0.9242 | 22.74 MB | Transfer learning |
| EfficientNetB0 | %96.55 | 0.9657 | 29.58 MB | Transfer learning |
| **ResNet50** ⭐ | **%98.65** | **0.9865** | 203.90 MB | Transfer learning |

### 🔬 Bilimsel Bulgu
**Transfer learning katkısı: +%12.89 puan iyileşme** (Baseline → ResNet50)

### Hangi Model Ne İçin?
- 🏆 **En doğru**: ResNet50
- ⚖️ **En dengeli**: EfficientNetB0
- 📱 **Mobil için**: MobileNetV2
- 🔬 **Kıyaslama**: Baseline CNN