"""
Domates Yaprağı Hastalıkları — Türkçe Bilgi Sözlüğü
Streamlit arayüzünde kullanılmak üzere hazırlanmıştır.
"""

DISEASE_INFO = {
    "Tomato___Bacterial_spot": {
        "ad": "Bakteriyel Leke",
        "etken": "Xanthomonas perforans (bakteri)",
        "belirtiler": [
            "Yapraklarda küçük, sulu, yağlı görünümlü lekeler",
            "Lekeler büyüyerek kahverengi-siyah renge döner",
            "Şiddetli durumda yaprak dökümü"
        ],
        "tedavi": [
            "Bakırlı bakterisitler (Bordo bulamacı) uygulayın",
            "Hastalıklı bitki kalıntılarını temizleyin",
            "Sulamayı sabah yapın, yapraklara su gelmesin"
        ],
        "onlem": "Sertifikalı tohum kullanın, münavebe uygulayın",
        "renk": "#e74c3c"
    },
    "Tomato___Early_blight": {
        "ad": "Erken Yaprak Yanıklığı",
        "etken": "Alternaria solani (mantar)",
        "belirtiler": [
            "Alt yapraklarda hedef tahtası benzeri konsantrik halkalı lekeler",
            "Lekelerin etrafında sarı hale",
            "İlerleyen dönemde yapraklar kurur ve dökülür"
        ],
        "tedavi": [
            "Mancozeb veya Chlorothalonil içerikli fungisitler",
            "Hastalıklı yaprakları kesin ve imha edin",
            "Bitki dibini malçlayın"
        ],
        "onlem": "Geniş aralıklı dikim yapın, yeterli havalandırma sağlayın",
        "renk": "#e67e22"
    },
    "Tomato___Late_blight": {
        "ad": "Geç Yaprak Yanıklığı",
        "etken": "Phytophthora infestans (oomycete)",
        "belirtiler": [
            "Yapraklarda büyük, düzensiz, sulu yeşil-kahverengi lekeler",
            "Yaprak alt yüzünde beyaz küf tabakası (nemli havada)",
            "Hızla tüm bitkiye yayılır, ölümcüldür"
        ],
        "tedavi": [
            "Acil olarak sistemik fungisit (Metalaxyl, Cymoxanil)",
            "Şiddetli ise hastalıklı bitkileri sökün ve yakın",
            "Çevre bitkileri koruyucu ilaçlama yapın"
        ],
        "onlem": "Nem kontrolü kritik, tarihte 'İrlanda Patates Kıtlığı'na sebep olmuştur",
        "renk": "#c0392b"
    },
    "Tomato___Leaf_Mold": {
        "ad": "Yaprak Küfü",
        "etken": "Passalora fulva (mantar)",
        "belirtiler": [
            "Yaprak üst yüzünde sarımsı, dağınık lekeler",
            "Yaprak alt yüzünde yeşil-zeytuni küf tabakası",
            "Özellikle serada yaygın"
        ],
        "tedavi": [
            "Bakırlı fungisitler veya Chlorothalonil",
            "Sera havalandırmasını artırın",
            "Yaprakların ıslak kalmasını engelleyin"
        ],
        "onlem": "Düşük nem (%85'in altı), iyi havalandırma",
        "renk": "#f39c12"
    },
    "Tomato___Septoria_leaf_spot": {
        "ad": "Septorya Yaprak Lekesi",
        "etken": "Septoria lycopersici (mantar)",
        "belirtiler": [
            "Çok sayıda küçük, dairesel, gri merkezli lekeler",
            "Lekelerin ortasında siyah noktalar (piknidler)",
            "Alt yapraklardan başlar, yukarı doğru yayılır"
        ],
        "tedavi": [
            "Mancozeb veya bakırlı fungisitler (10 günde bir)",
            "Alt yaprakları temizleyin",
            "Bitki dibinde malçlama yapın"
        ],
        "onlem": "Sulamada yapraklara su sıçratmamaya özen gösterin",
        "renk": "#9b59b6"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "ad": "Kırmızı Örümcek Hasarı",
        "etken": "Tetranychus urticae (akar)",
        "belirtiler": [
            "Yapraklarda sararma ve nokta nokta beneklenme",
            "Yaprak alt yüzünde ince ağ yapısı",
            "Şiddetli hasarda yapraklar kurur"
        ],
        "tedavi": [
            "Akarisitler (Abamektin, Spirodiclofen)",
            "Yaprakları suyla yıkayın (akar nemden hoşlanmaz)",
            "Faydalı akarlar (predator) salınımı"
        ],
        "onlem": "Yüksek nemli ortam akar nüfusunu azaltır",
        "renk": "#d35400"
    },
    "Tomato___Target_Spot": {
        "ad": "Hedef Leke",
        "etken": "Corynespora cassiicola (mantar)",
        "belirtiler": [
            "Hedef tahtası benzeri konsantrik halkalı lekeler",
            "Lekelerin merkezi açık, kenarları koyu kahverengi",
            "Yaprak, sap ve meyvede görülebilir"
        ],
        "tedavi": [
            "Azoxystrobin veya Difenoconazole içerikli fungisitler",
            "Hasta yaprakları temizleyin",
            "Bitki sıralarına yeterli mesafe verin"
        ],
        "onlem": "Sıcak ve nemli iklimde yaygın, havalandırma kritik",
        "renk": "#8e44ad"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "ad": "Sarı Yaprak Kıvırcıklığı Virüsü",
        "etken": "Tomato Yellow Leaf Curl Virus (TYLCV) — beyazsinek taşır",
        "belirtiler": [
            "Yapraklarda yukarı kıvrılma ve sararma",
            "Bitki büyümesi durur, cüceleşme",
            "Çiçek ve meyve oluşumu azalır"
        ],
        "tedavi": [
            "Virüs için doğrudan tedavi YOKTUR",
            "Hastalıklı bitkileri sökün ve imha edin",
            "Beyazsinek mücadelesi yapın (sarı yapışkan tuzaklar, neonikotinoidler)"
        ],
        "onlem": "Dayanıklı çeşit kullanın, beyazsinek kontrolü kritik",
        "renk": "#f1c40f"
    },
    "Tomato___Tomato_mosaic_virus": {
        "ad": "Mozaik Virüsü",
        "etken": "Tomato Mosaic Virus (ToMV) — temasla bulaşır",
        "belirtiler": [
            "Yapraklarda mozaik desenli açık-koyu yeşil alanlar",
            "Yaprak şekil bozuklukları, kıvrılma",
            "Verim ciddi şekilde düşer"
        ],
        "tedavi": [
            "Virüs için doğrudan tedavi YOKTUR",
            "Hastalıklı bitkileri sökün",
            "Aletleri ve ellerini sık sık dezenfekte edin"
        ],
        "onlem": "Sigara içenler bitkilere dokunmadan ellerini yıkamalı (tütünden bulaşabilir)",
        "renk": "#16a085"
    },
    "Tomato___healthy": {
        "ad": "Sağlıklı",
        "etken": "Hastalık tespit edilmedi ✅",
        "belirtiler": [
            "Yaprak yeşil ve canlı görünüyor",
            "Belirgin leke, sararma veya küf yok",
            "Bitki normal gelişim gösteriyor"
        ],
        "tedavi": [
            "Tedavi gerekmiyor",
            "Düzenli sulama ve gübreleme yapın",
            "Önleyici bakım uygulamalarına devam edin"
        ],
        "onlem": "Düzenli kontrol, dengeli sulama, uygun gübreleme",
        "renk": "#27ae60"
    }
}


# Modelin tahmin sırası (klasör adlarının alfabetik sıralı hali)
CLASS_ORDER = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]


def get_disease_info(class_key):
    """Sınıf adından hastalık bilgisini döndür."""
    return DISEASE_INFO.get(class_key, None)


def get_disease_name_tr(class_key):
    """Sınıf adından Türkçe ismi döndür."""
    info = DISEASE_INFO.get(class_key)
    return info["ad"] if info else "Bilinmiyor"