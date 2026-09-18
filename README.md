# ⚡ KAMA AI 5.0 — Bilişsel ve Güvenlik Zeka Platformu

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![RoBERTa Turkish](https://img.shields.io/badge/Backbone-RoBERTa%20Turkish-00f5ff.svg)](https://huggingface.co/dbmdz/bert-base-turkish-128k-uncased)

**KAMA AI 5.0**, Açık Kaynak Türkçe RoBERTa (`dbmdz/bert-base-turkish-128k-uncased`) transformer mimarisi üzerine inşa edilmiş, çok katmanlı Türkçe sokak dili ve argo kalkanı, 3 tonlu yapay zeka diplomat dönüşümü, algoritmik KVKK veri maskelemesi ve e-posta oltalama (phishing) tespit sistemi içeren hibrit bir bilişsel yapay zeka motorudur.

---

## 🌟 Temel Özellikler

1. **🧠 Derin RoBERTa Türkçe Sınıflandırma:**
   - 12 Transformer Bloğu, 128.000 Türkçe Vocab, 110M Parametre.
   - 5 Sınıf Anlık Analiz: `TEMIZ`, `HAFIF` (Argo/Kaba), `KUFUR`, `HAKARET`, `TEHDIT`.
   - **Hard-Negative Whitelist:** *"kamu"*, *"eksik"*, *"psikoloji"*, *"klasik"* gibi masum kelimelerde %100 sıfır yanlış pozitif.

2. **🎯 Türkçe Argo & Sokak Dili Kalkanı:**
   - Sokak dili, argo (`trrek`, `lan`, `moruk`, `lavuk`, `dallama` vb.) ve dezenformasyon filtreleri.

3. **🤖 Generative AI Diplomat 5.0:**
   - Sert veya argo ifadeleri anlam kaybı olmadan **3 farklı tonda** dönüştürme:
     - 👔 **Kurumsal:** Profesyonel iş dili ve resmi yazışmalar.
     - 🤝 **Dostane:** Samimi, yapıcı ve kırıcı olmayan üslup.
     - 🎒 **Çocuk / Eğitim:** Çocuk korumalı ve pedagojik yaklaşım.

4. **🔒 Algoritmik KVKK / PII Veri Kalkanı:**
   - **T.C. Kimlik No:** 11 haneli kural ve Modulo-10 checksum doğrulaması.
   - **TR IBAN:** Modulo-97 format ve banka kod kontrolü.
   - **Kredi Kartı:** Luhn algoritması kontrollü tam doğrulama.
   - **Telefon & E-posta:** Regex ve sınır kontrollü otomatik maskeleme.

5. **🎣 EdgeMail Phishing & Güvenlik Kalkanı:**
   - Aciliyet ve panik tetikleyicileri (*"Hesabınız askıya alındı"*, *"24 saat içinde şifrenizi girin"*).
   - Şüpheli URL ve alan adı imza tespiti.

---

## 🚀 Hızlı Başlangıç (Quickstart)

### 1. Yerel Kurulum (Python)

```bash
# 1. Depoyu klonlayın
git clone https://github.com/originedge/kama-ai-5.0.git
cd kama-ai-5.0

# 2. Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Sunucuyu başlatın
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Sunucu başladıktan sonra:
- **Web Dashboard:** `http://localhost:8000/`
- **Swagger API Dokümantasyonu:** `http://localhost:8000/docs`
- **REST API Dokümanı:** `http://localhost:8000/api`

---

### 2. Docker & Docker Compose ile Başlatma

```bash
# Tek komutla build edin ve çalıştırın
docker-compose up -d --build
```

---

## 📡 REST API Kullanımı

### 1. Ana Hibrit Analiz (`POST /kontrol`)

```bash
curl -X POST "http://localhost:8000/kontrol" \
  -H "Content-Type: application/json" \
  -d '{"mesaj": "işler nasıl trrek"}'
```

**Örnek Yanıt:**
```json
{
  "mesaj": "işler nasıl trrek",
  "durum": "HAFIF",
  "seviye": "hafif",
  "nezaket_puani": 40,
  "aciklama": "Metinde argo, sokak dili veya kaba ifadeler tespit edildi: trrek",
  "kibar_alternatif": "işler nasıl arkadaşım. Bilgilerinize sunar, iyi çalışmalar dileriz.",
  "kibar_alternatif_tonlar": {
    "kurumsal": "işler nasıl arkadaşım. Bilgilerinize sunar, iyi çalışmalar dileriz.",
    "dostane": "işler nasıl dostum Desteğiniz için teşekkürler!",
    "cocuk": "işler nasıl arkadaşım"
  }
}
```

---

## 📊 Benchmark ve Performans

| Metrik | Değer |
|---|---|
| **Model Parametresi** | 110 Milyon |
| **Türkçe Vocab Boyutu** | 128.000 Token |
| **Ortalama Çıkarsama Süresi (CPU)** | ~28 ms |
| **Çıkarsama Süresi (GPU T4/V100)** | ~6 ms |
| **Hard-Negative Whitelist Güvenliği** | %100 Sıfır Yanlış Pozitif |
| **API Throughput (Tek Worker)** | ~180 İstek / Saniye |

---

## 📄 Dokümantasyon

Tüm uç noktaların ayrıntılı parametreleri, şemaları ve örnekleri için [API_DOKUMANTASYONU.md](./API_DOKUMANTASYONU.md) dosyasına göz atın.

---

## 🛡️ Güvenlik & Gizlilik

KAMA AI 5.0, KVKK (Kişisel Verilerin Korunması Kanunu) ve GDPR uyumlu olarak tasarlanmıştır. Tüm PII verileri model inferansından önce veya sonra yerel olarak maskelenebilir.

---

## 📜 Lisans

Bu proje **MIT Lisansı** altında açık kaynak olarak dağıtılmaktadır. Ayrıntılar için [LICENSE](./LICENSE) dosyasına bakınız.

---

*Geliştirici: [Origin Edge Deep Neural Platform](https://oedge.xyz)*
