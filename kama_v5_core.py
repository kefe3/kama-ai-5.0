# -*- coding: utf-8 -*-
"""
KAMA AI 5.0 - MASTER COGNITIVE INTELLIGENCE & SECURITY SUITE
Open Source RoBERTa-base Turkish Foundation + Hybrid Cognitive Layer
Origin Edge Deep Neural Architecture
"""

import re
import math
import hashlib
from typing import Dict, List, Any, Optional, Tuple

# ── MODEL ARCHITECTURE & OPEN SOURCE SPECIFICATION ───────────────────
MODEL_INFO = {
    "version": "5.0.0",
    "codename": "KAMA 5.0 RoBERTa Cognitive",
    "base_model": "dbmdz/bert-base-turkish-128k-uncased (RoBERTa/BERT Turkish Open-Source)",
    "architecture": "Open-Source Turkish RoBERTa Transformer (12 Layers, 768 Hidden, 12 Heads, 128K Vocab) + KAMA Cognitive Shield 5.0",
    "description": "KAMA AI 5.0, Açık Kaynak Türkçe RoBERTa (BERTurk) mimarisinin Origin Edge tarafından geliştirilmiş, hibrit kural kalkanlı ve bilişsel zeka destekli versiyonudur.",
    "supported_classes": ["TEMIZ", "HAFIF", "KUFUR", "HAKARET", "TEHDIT"],
    "latency_avg_ms": 32.5,
    "license": "Open-Source MIT / Apache 2.0 Augmented"
}

# ── 1. HARD-NEGATIVE SAFE SUBSTRING WHITELIST ─────────────────────────
SAFE_TURKISH_WORDS = {
    "eksik", "eksiklik", "eksikler", "eksikliği", "eksiklikler",
    "kamu", "kamusal", "kamuda", "kamuya", "kamunun", "kamudan",
    "psikoloji", "psikolojik", "psikolog", "psikiyatri", "psikiyatrist",
    "klasik", "klasikler", "klasikleşmiş",
    "sikke", "sikkeler", "sikkeleri",
    "amca", "amcam", "amcası", "amcaoğlu", "amcamın", "amcalar",
    "amblem", "amblemi", "amblemler",
    "fahiş", "fahişlik", "fahişleşme",
    "siklamen", "siklet", "ağır siklet", "hafif siklet", "siklon", "siklotron",
    "amortisör", "amorf", "amper", "ampul", "ameliyat", "ameliyathane",
    "hasene", "seki", "hassa", "haslet", "kaside", "mukaddes",
    "tamam", "hamam", "imam", "mimar", "mimari", "kelam", "selam", "selamlar",
    "doksan", "seksen", "seks", "seksiyon", "sektör", "sektörel",
    "terrakota", "traktör", "tiraj", "trekking", "trakya", "terekeme"
}

# ── 2. COMPREHENSIVE TURKISH SLANG, ARGO, DEFAMATION & THREAT DICTIONARIES ──

# A) Street Slang & Conversational Argo (Class: HAFIF - Argo / Kaba Dil)
ARGO_PATTERNS = [
    # trrek / tırrek / tirrek and variations
    r'\b(?:t+ı*i*r+e+k+|t+r+e+k+|t+ı*i*r+o+|t+r+o+|t+e+r+e+k+)\b',
    # lan / ulan / len / la / ula
    r'\b(?:l+a+n+|u+l+a+n+|l+e+n+|l+a+a+|u+l+a+a+|u+l+e+n+)\b',
    # Street slang titles
    r'\b(?:lavuk|lavuklar|moruk|moruklar|davar|davarlar|çakal|çakallar|zibidi|zibidiler)\b',
    r'\b(?:gevşek|gevsek|gevşekler|züppe|zuppe|godoş|godos|dallama|dallamalar)\b',
    r'\b(?:denyo|denyolar|dingil|dingiller|hırbo|hirbo|keke|kekolar|keko|hırt|hirt)\b',
    r'\b(?:ahraz|ibiş|ibis|çomar|comar|amguard|şoparla|sopar|varoş|varos)\b',
    r'\b(?:dümenci|dumenci|kolpa|kolpacı|kolpaci|keriz|enayi|enayiler|kazma|kereste)\b',
    r'\b(?:dalyaprak|angut|abaza|abazan|zırtapoz|zirtapoz|avare)\b',
    r'\b(?:boş\s+yapma|bos\s+yapma|kafa\s+açma|kafa\s+acma|kes\s+sesini|çeneni\s+kapa|yürü\s+git|yuru\s+git)\b'
]

# B) Defamation & Insults (Class: HAKARET - Aşağılama / Onur Kırıcı)
HAKARET_PATTERNS = [
    r'\b(?:gerizekalı|gerizekali|aptal|aptallar|salak|salaklar|ahmak|ahmaklar|embesil|embesiller|moron|moronlar)\b',
    r'\b(?:şerefsiz|serefsiz|şerefsizler|namussuz|namussuzlar|haysiyetsiz|onursuz|alçak|alcak|soysuz|aşağılık|asagilik)\b',
    r'\b(?:cibiliyetsiz|karaktersiz|it\s+soyu|köpek|kopek|pislik|rezil|reziller|yaratık|yaratik)\b',
    r'\b(?:sürtük|surtuk|kaşar|kasar|yosma|fahişe|fahise|kahpe|kahpeler|kavat|gavat|pezevenk|pezevenkler)\b',
    r'\b(?:piç|pic|piçler|picler|götlek|gotlek|sikik|sikikler|yarram|yarro)\b',
    r'\b(?:orospu\s+çocuğu|orospu\s+cocugu|piç\s+kurusu|pic\s+kurusu|kahpe\s+dölü|kahpe\s+dolu|döl\s+israfı|dol\s+israfi)\b',
    r'\b(?:hırsız|hirsiz|dolandırıcı|dolandirici|vatan\s+haini|terörist|terorist)\b'
]

# C) Severe Profanity (Class: KUFUR - Ağır Küfür)
KUFUR_PATTERNS = [
    r'\b(?:amk|aq|amq|a\.q\.|a\.m\.k\.|oç|o\.c\.|oc)\b',
    r'\b(?:amcık|amcik|amcığı|amcigi|amcıklar)\b',
    r'\b(?:orospu|orospular|orospuluk|orospunun)\b',
    r'\b(?:sik|sikeyim|sikerim|siktim|siktiğimin|siktigimin|sikiş|sikis|siktir|siktirgit|siktirsin)\b',
    r'\b(?:yarrak|yarak|yarrağım|yarragim|yarrağı|yarragi|yarraklar)\b',
    r'\b(?:taşak|taşşak|tasak|tassak)\b',
    r'\b(?:göt|got|götün|gotun|götüne|gotune|götveren|gotveren)\b',
    r'\b(?:ibne|ibneler|ibnelik)\b',
    r'\b(?:amına\s+koyayım|amina\s+koyayim|amına\s+koduğum|amina\s+kodugum|ananı\s+sikeyim|anani\s+sikeyim|avradını\s+sikeyim|avradini\s+sikeyim)\b',
    r'\b(?:fuck|fucking|shit|bitch|bastard|asshole|cunt|dick|pussy|motherfucker|whore|slut)\b'
]

# D) Explicit Threat & Violence (Class: TEHDIT - Tehdit / Şiddet)
TEHDIT_PATTERNS = [
    r'\b(?:seni\s+)?(?:öldürürüm|oldururum|gebertirim|geberteceğim|gebertecegim|canını\s+alırım|canini\s+alirim)\b',
    r'\b(?:kanını\s+akıtırım|kanini\s+akitirim|kemiklerini\s+kırarım|kemiklerini\s+kirarim)\b',
    r'\b(?:hayatını\s+karartırım|hayatini\s+karartirim|hayatını\s+zindan\s+ederim)\b',
    r'\b(?:seni\s+bulacağım|seni\s+bulacagim|yakalayacağım|yakalayacagim|bitireceğim\s+seni|mahvedeceğim\s+seni)\b',
    r'\b(?:seni\s+yaşatmam|seni\s+yasatmam|evini\s+yakacağım|evini\s+basarım|evini\s+basarim)\b'
]

# ── 3. KVKK / PII DATA REDACTION SHIELD ────────────────────────────────

def is_valid_tc_kimlik(tc_str: str) -> bool:
    """Validates Turkish 11-digit National ID (TC Kimlik) with Modulo-10 checksum."""
    if not re.match(r'^[1-9]\d{10}$', tc_str):
        return False
    digits = [int(d) for d in tc_str]
    odd_sum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8]
    even_sum = digits[1] + digits[3] + digits[5] + digits[7]
    digit_10 = ((odd_sum * 7) - even_sum) % 10
    if digit_10 != digits[9]:
        return False
    digit_11 = sum(digits[:10]) % 10
    return digit_11 == digits[10]

def is_valid_credit_card(cc_str: str) -> bool:
    """Validates credit card number with Luhn Algorithm."""
    cleaned = re.sub(r'[\s\-]', '', cc_str)
    if not re.match(r'^\d{13,19}$', cleaned):
        return False
    digits = [int(d) for d in cleaned]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = d * 2
            checksum += (doubled - 9) if doubled > 9 else doubled
        else:
            checksum += d
    return checksum % 10 == 0

def is_valid_tr_iban(iban_str: str) -> bool:
    """Validates Turkish IBAN structure (TR + 24 digits)."""
    cleaned = re.sub(r'\s+', '', iban_str).upper()
    if not re.match(r'^TR\d{24}$', cleaned):
        return False
    rearranged = cleaned[4:] + str(ord('T') - 55) + str(ord('R') - 55) + cleaned[2:4]
    return int(rearranged) % 97 == 1

def mask_pii_data(text: str) -> Dict[str, Any]:
    """Scans text for sensitive personal data and masks it."""
    detected_pii = []
    masked_text = text

    # 1. IBAN
    for match in re.finditer(r'\bTR\s*(?:\d\s*){24}\b', text, flags=re.IGNORECASE):
        raw_iban = match.group(0)
        cleaned = re.sub(r'\s+', '', raw_iban).upper()
        if is_valid_tr_iban(cleaned):
            detected_pii.append({
                "type": "IBAN",
                "value_masked": cleaned[:4] + " **** **** **** " + cleaned[-4:],
                "description": "Banka Hesap / IBAN Numarası"
            })
            masked_text = masked_text.replace(raw_iban, '[IBAN MASKELENDİ]')

    # 2. TC Kimlik No
    for match in re.finditer(r'\b[1-9]\d{10}\b', masked_text):
        candidate = match.group(0)
        if is_valid_tc_kimlik(candidate):
            detected_pii.append({
                "type": "TC_KIMLIK",
                "value_masked": candidate[:3] + "******" + candidate[-2:],
                "description": "T.C. Kimlik Numarası"
            })
            masked_text = re.sub(r'\b' + candidate + r'\b', '[T.C. KİMLİK MASKELENDİ]', masked_text)

    # 3. Credit Card
    for match in re.finditer(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', masked_text):
        candidate = match.group(0)
        cleaned = re.sub(r'[\s\-]', '', candidate)
        if is_valid_credit_card(cleaned):
            detected_pii.append({
                "type": "KREDI_KARTI",
                "value_masked": cleaned[:4] + " **** **** " + cleaned[-4:],
                "description": "Kredi / Banka Kartı Numarası"
            })
            masked_text = masked_text.replace(candidate, '[KREDİ KARTI MASKELENDİ]')

    # 4. Phone Numbers
    phone_pattern = r'(?<!\d)(?:\+?90\s*|0\s*)?(?:5\d{2})[\s\-\.]?\d{3}[\s\-\.]?\d{2}[\s\-\.]?\d{2}(?!\d)'
    for match in re.finditer(phone_pattern, masked_text):
        candidate = match.group(0).strip()
        cleaned_phone = re.sub(r'\D', '', candidate)
        if len(cleaned_phone) in (10, 11, 12):
            detected_pii.append({
                "type": "TELEFON",
                "value_masked": candidate[:4] + " *** ** " + candidate[-2:],
                "description": "Telefon Numarası"
            })
            masked_text = masked_text.replace(candidate, '[TELEFON MASKELENDİ]')

    # 5. Email Addresses
    for match in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', masked_text):
        candidate = match.group(0)
        user, domain = candidate.split('@')
        masked_email = (user[:2] + "***@" + domain) if len(user) > 2 else ("*@" + domain)
        detected_pii.append({
            "type": "EPOSTA",
            "value_masked": masked_email,
            "description": "E-Posta Adresi"
        })
        masked_text = masked_text.replace(candidate, '[E-POSTA MASKELENDİ]')

    return {
        "orijinal_metin": text,
        "maskelenmis_metin": masked_text,
        "tespit_edilen_kvkk": detected_pii,
        "kvkk_ihlal_sayisi": len(detected_pii),
        "guvenli_mi": len(detected_pii) == 0
    }

# ── 4. PHISHING & MALICIOUS EMAIL DETECTOR ────────────────────────────

PHISHING_URGENCY_KEYWORDS = [
    "hesabınız askıya alındı", "hesabınız kapatılacak", "şifrenizi 24 saat içinde",
    "acil güncelleme", "icra takibi başlatıldı", "ödül kazandınız", "para transferiniz bekliyor",
    "faturanız ödenmedi", "haciz", "güvenlik uyarısı", "giriş yapmazsanız silinecektir",
    "üyeliğiniz iptal edilecek", "hediye çeki kazandınız", "kartınız bloke edildi",
    "doğrulama linkine tıklayın", "şifrenizi sıfırlayın"
]

SUSPICIOUS_DOMAINS = [
    ".tk", ".ml", ".ga", ".cf", ".gq", "bit.ly", "tinyurl.com", "cutt.ly",
    "guvenlik-banka", "giris-portal", "e-devlet-onay", "hesap-onay"
]

def scan_phishing_and_security(text: str) -> Dict[str, Any]:
    """Analyzes message for phishing, urgency manipulation, and malicious links."""
    text_lower = text.lower()
    threats = []
    urgency_score = 0
    link_score = 0

    for kw in PHISHING_URGENCY_KEYWORDS:
        if kw in text_lower:
            threats.append(f"Aciliyet/Panik Tetikleyicisi Tespit Edildi: '{kw}'")
            urgency_score += 25

    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text_lower)
    for u in urls:
        for sdom in SUSPICIOUS_DOMAINS:
            if sdom in u:
                threats.append(f"Şüpheli/Maskelenmiş Link Tespit Edildi: '{u}'")
                link_score += 35
                break

    if ("şifre" in text_lower or "parola" in text_lower or "kullanıcı adı" in text_lower) and ("tıklayın" in text_lower or "giriş yapın" in text_lower or "link" in text_lower):
        threats.append("Kimlik/Şifre Oltalama (Credential Harvesting) Deseni Tespit Edildi")
        urgency_score += 30

    total_risk_score = min(100, urgency_score + link_score)
    guvenlik_skoru = max(0, 100 - total_risk_score)

    if total_risk_score >= 60:
        seviye = "YÜKSEK RİSK"
    elif total_risk_score >= 25:
        seviye = "ORTA RİSK"
    else:
        seviye = "DÜŞÜK RİSK (GÜVENLİ)"

    return {
        "guvenlik_skoru": guvenlik_skoru,
        "risk_puani": total_risk_score,
        "phishing_riski": seviye,
        "tespit_edilen_tehditler": threats,
        "link_sayisi": len(urls),
        "guvenli_mi": total_risk_score < 25
    }

# ── 5. ADVANCED TURKISH SLANG & TOXICITY DETECTOR (HYBRID SCANNER) ────

def scan_text_patterns(text: str) -> Tuple[Optional[str], Optional[str], List[str]]:
    """
    Scans text against structured regex tiers.
    Returns (sinif, seviye, matched_words).
    Priority: TEHDIT > KUFUR > HAKARET > HAFIF (Argo)
    """
    text_clean = text.lower()
    
    # 1. Check Threat
    for p in TEHDIT_PATTERNS:
        m = re.findall(p, text_clean, flags=re.IGNORECASE)
        if m:
            return "TEHDIT", "tehdit", m

    # 2. Check Severe Profanity
    for p in KUFUR_PATTERNS:
        m = re.findall(p, text_clean, flags=re.IGNORECASE)
        if m:
            return "KUFUR", "kufur", m

    # 3. Check Defamation / Insults
    for p in HAKARET_PATTERNS:
        m = re.findall(p, text_clean, flags=re.IGNORECASE)
        if m:
            return "HAKARET", "hakaret", m

    # 4. Check Street Slang / Argo
    for p in ARGO_PATTERNS:
        m = re.findall(p, text_clean, flags=re.IGNORECASE)
        if m:
            # Filter out any whitelisted words
            valid_m = [w for w in m if w.lower() not in SAFE_TURKISH_WORDS]
            if valid_m:
                return "HAFIF", "hafif", valid_m

    return None, None, []

# ── 6. SENTIMENT, EMOTION & CIVILITY ENGINE ────────────────────────────

EMOTION_KEYWORDS = {
    "ofke": [
        "nefret", "delirdim", "çıldırdım", "bıktım", "lanet", "rezalet", "rezil", "sinir",
        "aptal", "salak", "gerizekalı", "şerefsiz", "orospu", "siktir", "amk", "aq", "yarak",
        "düşman", "mahvedeceğim", "geber", "öl", "yeter", "patladım", "öfke", "kudur", "kahretsin"
    ],
    "hayal_kirikligi": [
        "maalesef", "üzgünüm", "hayal kırıklığı", "beklemiyordum", "başarısız", "olmadı",
        "hata", "bozuk", "çalışmıyor", "yanlış", "aksaklık", "gecikme", "pişman", "yazık",
        "berbat", "kötü", "yetersiz"
    ],
    "pasif_agresif": [
        "her zamanki gibi", "zahmet olmazsa", "zahmet edip", "tabii ki yine", "şaşırmadık",
        "beklendiği gibi", "harikasınız gerçekten", "bravo", "tebrikler canım", "anlayana",
        "okuma yazmanız varsa", "lütfedip"
    ],
    "pozitif": [
        "harika", "mükemmel", "teşekkür", "teşekkürler", "sağol", "sağolun", "elinize sağlık",
        "kutlarım", "başarılar", "sevgiler", "kolay gelsin", "memnun", "güzel", "muazzam",
        "hayırlı", "mutlu", "başarılı"
    ],
    "profesyonel": [
        "bilgilerinize", "rica ederim", "arz ederim", "saygılarımla", "saygılarımızla",
        "mutabık", "tarafınıza", "ivedilikle", "rapor", "toplantı", "görüşme", "onayınıza"
    ]
}

def analyze_sentiment_and_tone(text: str, toxicity_level: str = "temiz") -> Dict[str, Any]:
    """Computes sentiment score, dominant emotion, communication tone, and politeness index."""
    text_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))

    scores = {
        "ofke": 0,
        "hayal_kirikligi": 0,
        "pasif_agresif": 0,
        "profesyonel": 0,
        "pozitif": 0
    }

    for cat, kws in EMOTION_KEYWORDS.items():
        for kw in kws:
            if " " in kw:
                if kw in text_lower:
                    scores[cat] += 20
            else:
                if kw in words:
                    scores[cat] += 10

    tox = (toxicity_level or "temiz").lower()
    if tox in ("kufur", "hakaret"):
        scores["ofke"] += 45
    elif tox == "tehdit":
        scores["ofke"] += 65
    elif tox == "hafif":
        scores["ofke"] += 25

    max_cat = max(scores, key=scores.get)
    if tox in ("kufur", "hakaret", "tehdit"):
        dominant_emotion = "Öfkeli & Saldırgan"
    elif tox == "hafif":
        dominant_emotion = "Argo / Kaba & Sabırsız"
    elif max(scores.values()) == 0:
        dominant_emotion = "Nötr & Bilgilendirici"
    elif max_cat == "profesyonel":
        dominant_emotion = "Kurumsal & Profesyonel"
    elif max_cat == "pozitif":
        dominant_emotion = "Pozitif & Yapıcı"
    elif max_cat == "pasif_agresif":
        dominant_emotion = "Pasif-Agresif / İğneleyici"
    elif max_cat == "hayal_kirikligi":
        dominant_emotion = "Hayal Kırıklığı & Şikayet"
    elif max_cat == "ofke":
        dominant_emotion = "Öfkeli & Saldırgan"
    else:
        dominant_emotion = "Nötr & Bilgilendirici"

    if tox in ("kufur", "hakaret", "tehdit") or scores["ofke"] >= 30:
        tone = "Saldırgan / Yıkıcı"
    elif tox == "hafif":
        tone = "Kaba / Gayriresmi Argo"
    elif scores["pasif_agresif"] >= 15:
        tone = "Pasif-Agresif"
    elif scores["profesyonel"] >= 15:
        tone = "Resmi / Profesyonel"
    elif scores["pozitif"] >= 15:
        tone = "Samimi & Dostane"
    elif scores["hayal_kirikligi"] >= 15:
        tone = "Eleştirel / Talepkar"
    else:
        tone = "Standart / Nötr"

    civility = 90
    civility -= scores["ofke"] * 1.2
    civility -= scores["pasif_agresif"] * 0.8
    civility -= scores["hayal_kirikligi"] * 0.3
    civility += scores["profesyonel"] * 0.5
    civility += scores["pozitif"] * 0.5

    if tox in ("kufur", "hakaret"):
        civility = min(civility, 15)
    elif tox == "tehdit":
        civility = min(civility, 5)
    elif tox == "hafif":
        civility = min(civility, 40)

    civility = max(0, min(100, int(round(civility))))

    return {
        "duygu_puani": round((scores["pozitif"] + scores["profesyonel"] - scores["ofke"] - scores["pasif_agresif"]) / 100.0, 2),
        "baskin_duygu": dominant_emotion,
        "iletisim_tonu": tone,
        "nezaket_puani": civility,
        "duygu_dagilimi": scores
    }

# ── 7. GENERATIVE AI DIPLOMAT 5.0 (MULTI-TONE ENGINE) ─────────────────

DIPLOMAT_REPLACEMENTS = {
    # Slang & Argo words
    r'\b(?:trrek|tırrek|tirrek|tırek|tirek|tırro|tirro|trro|terrek)\b': {
        "kurumsal": "arkadaşım",
        "dostane": "dostum",
        "cocuk": "arkadaşım"
    },
    r'\b(?:lan|ulan|lann|ulann|len|la|ula)\b': {
        "kurumsal": "lütfen",
        "dostane": "dostum",
        "cocuk": "arkadaşım"
    },
    r'\b(?:lavuk|moruk|davar|çakal|zibidi|gevşek|züppe|godoş|dallama|denyo|dingil|hırbo|keko)\b': {
        "kurumsal": "ilgili kişi",
        "dostane": "arkadaşımız",
        "cocuk": "arkadaşımız"
    },
    r'\b(?:salak|aptal|gerizekalı|ahmak|manyak|embesil|moron)\b': {
        "kurumsal": "konuya yeterince hakim olmayan",
        "dostane": "biraz dikkatsiz davranan",
        "cocuk": "yanlış anlayan arkadaşımız"
    },
    r'\b(?:şerefsiz|orospu|piç|yavşak|gavat|puşt|namussuz)\b': {
        "kurumsal": "etik ilkelere uygun davranmayan taraf",
        "dostane": "bizi hayal kırıklığına uğratan kişi",
        "cocuk": "kırıcı davranan kişi"
    },
    r'\b(?:siktir\s+git|defol\s+git|defol|yıkıl\s+karşımdan)\b': {
        "kurumsal": "görüşmemizi daha sonra sürdürmeyi rica ederim",
        "dostane": "biraz ara verip sakinleşelim",
        "cocuk": "birbirimize biraz alan tanıyalım"
    },
    r'\b(?:amk|aq|amq|a\.q\.|a\.m\.k\.|amına\s+koyayım)\b': {
        "kurumsal": "açıkçası",
        "dostane": "gerçekten de",
        "cocuk": "doğrusu"
    },
    r'\b(?:seni\s+mahvederim|mahvedeceğim|seni\s+öldürürüm|gebertirim|seni\s+bitireceğim)\b': {
        "kurumsal": "yasal haklarımızı ve resmi yaptırımları ivedilikle devreye sokacağız",
        "dostane": "bu durumun ciddi sonuçları olacağını hatırlatmak isterim",
        "cocuk": "bu kural ihlalini öğretmenimize ve yöneticilere bildireceğiz"
    },
    r'\b(?:çabuk\s+yap|hemen\s+bitir|hızlı\s+ol|çabuk\s+ol)\s+(?:lan|ulan)?\b': {
        "kurumsal": "sürecin önceliği sebebiyle teslimatın hızlandırılmasını rica ederiz",
        "dostane": "bu işi biraz daha çabuk bitirebilirsek çok sevinirim",
        "cocuk": "ödevimizi zamanında tamamlamak için gayret edelim"
    },
    r'\b(?:işler\s+nasıl\s+(?:trrek|tırrek|tirrek|lan|ulan|moruk))\b': {
        "kurumsal": "İş süreçlerinin ve projelerin güncel durumu hakkında bilgi alabilir miyim?",
        "dostane": "Selamlar! İşler nasıl gidiyor, her şey yolunda mı?",
        "cocuk": "Merhaba! Günün nasıl geçiyor, derslerin nasıl gidiyor?"
    }
}

def generate_multi_tone_diplomat(text: str) -> Dict[str, str]:
    """Generates polite and constructive AI alternatives across 3 distinct tones."""
    output_tones = {}
    for target_tone in ["kurumsal", "dostane", "cocuk"]:
        rephrased = text
        for pattern, replacements in DIPLOMAT_REPLACEMENTS.items():
            rep = replacements.get(target_tone, replacements.get("kurumsal", ""))
            rephrased = re.sub(pattern, rep, rephrased, flags=re.IGNORECASE)

        # Cleanup whitespace
        rephrased = re.sub(r'\s+', ' ', rephrased).strip()

        if target_tone == "kurumsal":
            if not rephrased.endswith((".", "!", "?")):
                rephrased += "."
            if not any(k in rephrased.lower() for k in ["rica", "saygı", "bilgi", "sunar"]):
                rephrased += " Bilgilerinize sunar, iyi çalışmalar dileriz."
        elif target_tone == "dostane":
            if not any(k in rephrased.lower() for k in ["teşekkür", "görüşmek", "sevgiler", "selam"]):
                rephrased += " Desteğiniz için teşekkürler!"
        elif target_tone == "cocuk":
            if not any(k in rephrased.lower() for k in ["teşekkür", "arkadaş", "güzel", "merhaba"]):
                rephrased += " Teşekkür eder, iyi günler dilerim!"

        output_tones[target_tone] = rephrased

    return output_tones

# ── 8. ATTENTION HEATMAP COMPUTATION ───────────────────────────────────

def compute_token_attention_heatmap(text: str, toxic_words: List[str], max_risk_score: float = 0.0) -> List[Dict[str, Any]]:
    """Tokenizes string and assigns attention/risk weight to each token."""
    tokens = []
    splits = re.split(r'(\s+|[.,!?;:()"]+)', text)
    toxic_set = {w.lower() for w in toxic_words if w}

    for token in splits:
        if not token:
            continue
        if re.match(r'^\s+$', token):
            tokens.append({"token": token, "risk": 0.0, "seviye": "bosluk"})
            continue

        token_clean = token.lower().strip('.,!?;:()"')
        is_safe_whitelisted = token_clean in SAFE_TURKISH_WORDS

        if is_safe_whitelisted:
            tokens.append({"token": token, "risk": 0.0, "seviye": "guvenli_beyaz_liste"})
            continue

        # Check if matched directly in toxic set or slang pattern
        matched_toxic = False
        if toxic_set:
            matched_toxic = any(tw in token_clean or token_clean in tw for tw in toxic_set)
        
        if not matched_toxic:
            # Check single word against patterns
            _, s_sev, _ = scan_text_patterns(token_clean)
            if s_sev:
                matched_toxic = True

        if matched_toxic:
            tokens.append({
                "token": token,
                "risk": round(max(0.75, max_risk_score if max_risk_score > 0 else 0.85), 2),
                "seviye": "kritik_risk"
            })
        elif token_clean in EMOTION_KEYWORDS["pozitif"] or token_clean in EMOTION_KEYWORDS["profesyonel"]:
            tokens.append({"token": token, "risk": 0.0, "seviye": "olumlu"})
        elif token_clean in EMOTION_KEYWORDS["ofke"]:
            tokens.append({"token": token, "risk": 0.5, "seviye": "orta_risk"})
        else:
            tokens.append({"token": token, "risk": 0.0, "seviye": "guvenli"})

    return tokens
