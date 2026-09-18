# 🚀 KAMA AI 5.0 — REST API Dokümantasyonu

**Açık Kaynak Türkçe RoBERTa (BERTurk) Tabanlı Bilişsel ve Güvenlik Zeka Motoru**

---

## 🌐 Genel Bakış ve Base URL

KAMA AI 5.0 REST API, metin toksisite analizi, Türkçe sokak dili ve argo tespiti, 3 tonlu yapay zeka diplomat dönüşümü, KVKK/PII veri maskelemesi ve e-posta oltalama (phishing) koruması sunan yüksek hızlı bir yapay zeka servisidir.

* **Production Base URL:** `https://ai.oedge.xyz`
* **Local Development Base URL:** `http://localhost:8000`
* **Swagger UI Dokümantasyonu:** `https://ai.oedge.xyz/docs`
* **Varsayılan İçerik Tipi:** `application/json; charset=utf-8`

---

## 🔑 Kimlik Doğrulama (Authentication)

Genel sorgular için kimlik doğrulama zorunlu değildir. Yüksek hacimli kurumsal çağrılar ve özel kotalar için `X-API-Key` başlığı kullanılabilir:

```http
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

---

## 📡 Temel Uç Noktalar (Endpoints)

### 1. Ana Hibrit Analiz Motoru (`/kontrol`)

Metni Türkçe RoBERTa transformer modeli, çok katmanlı sokak dili/argo kalkanı, dikkat ısı haritası, duygu & ton analitiği, AI diplomatı ve güvenlik kalkanlarıyla birlikte tam kapsamlı analiz eder.

* **Metot:** `POST`
* **Uç Nokta:** `/kontrol` veya `/kama`
* **İstek Gövdesi (JSON):**

```json
{
  "mesaj": "işler nasıl trrek",
  "dil": "tr"
}
```

#### Parametreler:
| Parametre | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `mesaj` | `string` | **Evet** | Analiz edilecek Türkçe veya İngilizce metin. |
| `dil` | `string` | Hayır | `tr` veya `en`. Belirtilmezse otomatik dil tespiti yapılır. |

#### Örnek Başarılı Yanıt (200 OK):
```json
{
  "mesaj": "işler nasıl trrek",
  "durum": "HAFIF",
  "seviye": "hafif",
  "skor": 1.0,
  "sinif_id": 1,
  "kaynak": "kama_slang_shield",
  "dil": "tr",
  "aciklama": "Metinde argo, sokak dili veya kaba ifadeler tespit edildi: trrek",
  "onemli_kelimeler": ["trrek"],
  "duygu_puani": 0.0,
  "baskin_duygu": "Argo / Kaba & Sabırsız",
  "iletisim_tonu": "Kaba / Gayriresmi Argo",
  "nezaket_puani": 40,
  "kibar_alternatif": "işler nasıl arkadaşım. Bilgilerinize sunar, iyi çalışmalar dileriz.",
  "kibar_alternatif_tonlar": {
    "kurumsal": "işler nasıl arkadaşım. Bilgilerinize sunar, iyi çalışmalar dileriz.",
    "dostane": "işler nasıl dostum Desteğiniz için teşekkürler!",
    "cocuk": "işler nasıl arkadaşım"
  },
  "token_riskleri": [
    { "token": "işler", "risk": 0.0, "seviye": "guvenli" },
    { "token": "nasıl", "risk": 0.0, "seviye": "guvenli" },
    { "token": "trrek", "risk": 0.85, "seviye": "kritik_risk" }
  ],
  "kvkk_pii": {
    "orijinal_metin": "işler nasıl trrek",
    "maskelenmis_metin": "işler nasıl trrek",
    "tespit_edilen_kvkk": [],
    "kvkk_ihlal_sayisi": 0,
    "guvenli_mi": true
  },
  "phishing_guvenlik": {
    "guvenlik_skoru": 100,
    "risk_puani": 0,
    "phishing_riski": "DÜŞÜK RİSK (GÜVENLİ)",
    "tespit_edilen_tehditler": [],
    "link_sayisi": 0,
    "guvenli_mi": true
  }
}
```

---

### 2. Hızlı Nezaket & Toksisite Analizi (`/api/v2/analyze`)

Mikroservisler için hafif ve ultra hızlı (~20ms) yanıt döndüren özet uç nokta.

* **Metot:** `POST`
* **Uç Nokta:** `/api/v2/analyze`
* **İstek Gövdesi:**
```json
{
  "text": "Bu raporda klasik psikoloji ve kamu eksiklikleri bulunuyor."
}
```

* **Yanıt (200 OK):**
```json
{
  "durum": "TEMIZ",
  "nezaket_puani": 85,
  "baskin_duygu": "Nötr & Bilgilendirici",
  "iletisim_tonu": "Standart / Nötr"
}
```

---

### 3. AI Diplomat 5.0 (3 Tonlu Yeniden Yazıcı) (`/api/v2/diplomat`)

Sert, kaba veya argo ifadeleri anlamını ve niyetini koruyarak 3 farklı hedef tona dönüştürür.

* **Metot:** `POST`
* **Uç Nokta:** `/api/v2/diplomat`
* **İstek Gövdesi:**
```json
{
  "text": "çabuk yap lan şu işi bıktım artık senden gerizekalı"
}
```

* **Yanıt (200 OK):**
```json
{
  "kurumsal": "sürecin önceliği sebebiyle teslimatın hızlandırılmasını rica ederiz. konuya yeterince hakim olmayan taraf hakkında bilgilendirme gerekmektedir. Bilgilerinize sunar, iyi çalışmalar dileriz.",
  "dostane": "bu işi biraz daha çabuk bitirebilirsek çok sevinirim. biraz dikkatsiz davranan arkadaşımıza destek olalım. Desteğiniz için teşekkürler!",
  "cocuk": "ödevimizi zamanında tamamlamak için gayret edelim. yanlış anlayan arkadaşımıza yardımcı olalım. Teşekkür eder, iyi günler dilerim!"
}
```

---

### 4. KVKK / PII Veri Maskeleme Kalkanı (`/api/v2/pii-mask`)

Metindeki hassas kişisel verileri (T.C. Kimlik No, TR IBAN, Kredi Kartı Luhn, Telefon, E-posta) algoritmik olarak doğrular ve maskeler.

* **Metot:** `POST`
* **Uç Nokta:** `/api/v2/pii-mask`
* **İstek Gövdesi:**
```json
{
  "text": "Müşteri TC: 10000000146, Telefon: 05511960116, IBAN: TR330006100519786457841324"
}
```

* **Yanıt (200 OK):**
```json
{
  "orijinal_metin": "Müşteri TC: 10000000146, Telefon: 05511960116, IBAN: TR330006100519786457841324",
  "maskelenmis_metin": "Müşteri TC: [T.C. KİMLİK MASKELENDİ], Telefon: [TELEFON MASKELENDİ], IBAN: [IBAN MASKELENDİ]",
  "tespit_edilen_kvkk": [
    { "type": "IBAN", "value_masked": "TR33 **** **** **** 1324", "description": "Banka Hesap / IBAN Numarası" },
    { "type": "TC_KIMLIK", "value_masked": "100******46", "description": "T.C. Kimlik Numarası" },
    { "type": "TELEFON", "value_masked": "0551 *** ** 16", "description": "Telefon Numarası" }
  ],
  "kvkk_ihlal_sayisi": 3,
  "guvenli_mi": false
}
```

---

### 5. EdgeMail Phishing & Güvenlik Kalkanı (`/api/v2/phishing-check`)

E-postalardaki aciliyet manipülasyonlarını, şüpheli linkleri ve kimlik avı (credential harvesting) tuzaklarını tespit eder.

* **Metot:** `POST`
* **Uç Nokta:** `/api/v2/phishing-check`
* **İstek Gövdesi:**
```json
{
  "text": "DİKKAT: Hesabınız askıya alındı! 24 saat içinde http://e-devlet-onay.tk linkine tıklayarak şifrenizi giriniz."
}
```

* **Yanıt (200 OK):**
```json
{
  "guvenlik_skoru": 40,
  "risk_puani": 60,
  "phishing_riski": "YÜKSEK RİSK",
  "tespit_edilen_tehditler": [
    "Aciliyet/Panik Tetikleyicisi Tespit Edildi: 'hesabınız askıya alındı'",
    "Şüpheli/Maskelenmiş Link Tespit Edildi: 'http://e-devlet-onay.tk'",
    "Kimlik/Şifre Oltalama (Credential Harvesting) Deseni Tespit Edildi"
  ],
  "link_sayisi": 1,
  "guvenli_mi": false
}
```

---

### 6. Toplu Mesaj Analizi (`/kontrol/toplu`)

Tek seferde en fazla 100 mesajı toplu olarak analiz eder.

* **Metot:** `POST`
* **Uç Nokta:** `/kontrol/toplu`
* **İstek Gövdesi:**
```json
{
  "mesajlar": [
    "İyi çalışmalar dilerim.",
    "işler nasıl trrek",
    "Sipariş teslimatı ne zaman?"
  ],
  "dil": "tr"
}
```

---

## 💻 Çok Dilli Entegrasyon Kod Örnekleri

### 1. cURL (Komut Satırı)
```bash
curl -X POST "https://ai.oedge.xyz/kontrol" \
  -H "Content-Type: application/json" \
  -d '{"mesaj": "işler nasıl trrek"}'
```

### 2. Python (`requests`)
```python
import requests

url = "https://ai.oedge.xyz/kontrol"
payload = {"mesaj": "Harika bir çalışma olmuş, teşekkürler."}

response = requests.post(url, json=payload)
result = response.json()

print(f"Durum: {result['durum']} | Nezaket: {result['nezaket_puani']}/100")
```

### 3. JavaScript / TypeScript (Node.js & Browser)
```javascript
const response = await fetch("https://ai.oedge.xyz/kontrol", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ mesaj: "Toplantı saatini teyit edebilir miyiz?" })
});

const data = await response.json();
console.log(data.durum, data.nezaket_puani);
```

### 4. PHP (cURL)
```php
<?php
$ch = curl_init('https://ai.oedge.xyz/kontrol');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['mesaj' => 'İyi günler dilerim.']));

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
echo "Durum: " . $data['durum'];
?>
```

---

## 🚦 HTTP Durum Kodları

| Durum Kodu | Anlamı | Açıklama |
|---|---|---|
| `200 OK` | Başarılı | İstek başarıyla işlendi ve analiz sonucu döndü. |
| `400 Bad Request` | Geçersiz İstek | Gönderilen JSON formatı hatalı veya `mesaj` parametresi boş. |
| `429 Too Many Requests` | Hız Sınırı | Belirlenen istek limiti aşıldı. |
| `500 Internal Server Error` | Sunucu Hatası | Model çıkarsama veya dahili işleme hatası. |

---

*Dokümantasyon Sürümü: KAMA AI 5.0.0 — Origin Edge Deep Neural Platform.*
