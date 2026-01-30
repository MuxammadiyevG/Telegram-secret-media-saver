# Telegram Media Monitor

Telegram'dagi maxfiy va vaqtinchalik xabarlarni monitoring qilish va saqlash uchun Python dasturi.

## 📋 Tavsif

Ushbu dastur Telegram'dagi turli xil xabarlarni kuzatib boradi va ularning medialarini avtomatik ravishda yuklab oladi. Ayniqsa, quyidagi xabar turlarini qayta ishlaydi:

- ⏱️ **TTL (Time-To-Live) xabarlar** - o'z-o'zidan o'chiradigan xabarlar
- 👁️ **Bir marta ko'rish xabarlari** - faqat bir marta ko'rish mumkin bo'lgan medialar
- 🔒 **Maxfiy chat mediasi** - shifrlangan chatlardan kelgan medialar
- 📸 Rasmlar, videolar, audio fayllar va hujjatlar

## ✨ Asosiy Imkoniyatlar

### 🔐 Login Usullari
- **Telefon raqami va SMS kod** orqali kirish
- **QR kod** orqali kirish (telefondan skanerlash)
- **Ikki faktorli autentifikatsiya (2FA)** qo'llab-quvvatlash
- Avtomatik sessiya saqlash (qayta login talab qilinmaydi)

### 📥 Media Yuklash
- Barcha media turlarini qo'llab-quvvatlash:
  - 📷 Rasmlar (JPEG, PNG, GIF, WebP)
  - 🎥 Videolar (MP4, AVI, MOV)
  - 🎵 Audio fayllar va ovozli xabarlar
  - 📄 Hujjatlar (PDF va boshqalar)
  - 🎬 GIF va stikerlar
- Yuklash jarayoni progress ko'rsatkichi
- FloodWait xatoliklarini avtomatik qayta urinish bilan hal qilish
- Katta hajmli fayllarni yuklab olish

### 📁 Fayl Tashkiloti
- Timestamp bilan ajratilgan papkalar
- Media turlariga qarab avtomatik kategoriyalash:
  - `ttl_chats/` - TTL xabarlar
  - `view_once/` - Bir marta ko'rish xabarlari
  - `secret_chats/` - Maxfiy chatlar
- Har bir media uchun metadata fayli
- Tushunarli fayl nomlari

### 📊 Metadata Saqlash
Har bir yuklangan media uchun quyidagi ma'lumotlar saqlanadi:
- Media turi va manbasi
- Chat va xabar ID'lari
- Yuklash sanasi va vaqti
- Fayl hajmi
- Caption (agar mavjud bo'lsa)
- TTL qiymati (agar mavjud bo'lsa)

### 📝 Logging
- Batafsil log yozuvlari
- Fayl va konsolga chiqarish
- Xatolarni to'liq kuzatish
- Real-time monitoring ma'lumotlari

## 🚀 O'rnatish

### 1. Talablar

Python 3.7 yoki undan yuqori versiya kerak.

### 2. Kutubxonalarni o'rnatish

```bash
pip install telethon qrcode
```

### 3. Telegram API Kalitlarini Olish

1. [https://my.telegram.org](https://my.telegram.org) ga kiring
2. "API development tools" bo'limiga o'ting
3. Yangi ilova yarating
4. `API_ID` va `API_HASH` ni ko'chirib oling

### 4. Konfiguratsiya

Dastur kodida quyidagi qiymatlarni o'zgartiring:

```python
API_ID = "sizning_api_id"
API_HASH = "sizning_api_hash"
PHONE_NUMBER = "+998901234567"  # Telefon raqamingiz
```

## 📖 Foydalanish

### Dasturni Ishga Tushirish

```bash
python telegram_monitor.py
```

### Birinchi Marta Kirish

Dasturni birinchi marta ishga tushirganingizda, login usulini tanlashingiz kerak bo'ladi:

#### Variant 1: Telefon Raqami (Tavsiya Etiladi)

```
🔐 LOGIN USULINI TANLANG:
1. 📱 Telefon raqami va SMS kod (tavsiya etiladi)
2. 📲 QR kod (telefondan skanerlash)

Tanlov (1 yoki 2, Enter = 1): 1
```

1. Telegram'dan kelgan kodni kiriting
2. Agar 2FA yoqilgan bo'lsa, parolingizni kiriting

#### Variant 2: QR Kod

```
Tanlov (1 yoki 2, Enter = 1): 2
```

1. Ekranda QR kod ko'rsatiladi
2. Telegram ilovasini oching (telefonda)
3. **Settings → Devices → Link Desktop Device**
4. QR kodni skanerlang
5. Agar 2FA yoqilgan bo'lsa, parolingizni kiriting

### Monitoring Jarayoni

Muvaffaqiyatli kirganingizdan so'ng:

```
✅ MONITORING BOSHLANDI
👀 Xabarlarni monitoring qilish boshlandi...
⛔ To'xtatish uchun Ctrl+C bosing
```

Dastur avtomatik ravishda:
- Barcha kiruvchi xabarlarni kuzatadi
- TTL va "bir marta ko'rish" xabarlarini aniqlaydi
- Medialarni yuklab oladi
- Loglarni yozadi

### To'xtatish

Dasturni to'xtatish uchun `Ctrl+C` tugmalarini bosing.

## 📂 Chiqish Tuzilmasi

Dastur quyidagi tuzilmada fayllar yaratadi:

```
telegram_media_20240130_143022/
├── ttl_chats/
│   ├── ttl_chat_photo_chat123_456789_20240130_143045_001.jpg
│   ├── ttl_chat_photo_chat123_456789_20240130_143045_001.jpg.txt
│   └── ...
├── view_once/
│   ├── view_once_video_chat456_789012_20240130_143102_002.mp4
│   ├── view_once_video_chat456_789012_20240130_143102_002.mp4.txt
│   └── ...
└── secret_chats/
    └── ...
```

### Fayl Nomlari Tuzilmasi

```
[media_type]_[media_name]_chat[chat_id]_[file_id]_[timestamp].[ext]
```

Misol:
```
ttl_chat_photo_chat123456789_987654321_20240130_143045_123456.jpg
```

### Metadata Fayl Namunasi

```
Media Type: photo
Source: ttl_chat
Chat ID: 123456789
Message ID: 42
Date: 2024-01-30 14:30:45
File Size: 2.45 MB
Extension: .jpg
Caption: Salom dunyo!
TTL: 10 seconds
```

## 🔧 Sozlamalar

### Logging Darajasi

Log darajasini o'zgartirish uchun:

```python
logging.basicConfig(
    level=logging.DEBUG,  # INFO dan DEBUG ga o'zgartirish
    ...
)
```

### Chiqish Papkasi

Chiqish papkasini o'zgartirish:

```python
OUTPUT_DIR = "mening_telegram_media"
```

### Qayta Urinish Soni

Yuklab olishda qayta urinish sonini sozlash:

```python
max_retries = 5  # 3 dan 5 ga o'zgartirish
```

## ⚠️ Muhim Eslatmalar

### Xavfsizlik

- ✅ `session_name.session` faylini **hech kimga bermang**
- ✅ API kalitlaringizni **maxfiy saqlang**
- ✅ Kodni GitHub'ga yuklashdan oldin kalitlarni **o'chirib tashlang**
- ✅ 2FA'ni yoqish **tavsiya etiladi**

### Qonuniylik

- ⚖️ Faqat **o'zingizning xabarlaringiz** uchun foydalaning
- ⚖️ Boshqa odamlarning **ruxsatisiz** xabarlarini saqlamang
- ⚖️ Telegram **Terms of Service**ni hurmat qiling
- ⚖️ Mahalliy **qonunlarga** rioya qiling

### Texnik Cheklovlar

- 📊 Telegram FloodWait cheklovlariga **rioya qiladi**
- 📊 Juda katta fayllar **vaqt talab qiladi**
- 📊 Internet aloqasi **barqaror** bo'lishi kerak
- 📊 Maxfiy chatlar ba'zi qurilmalarda **cheklangan**

## 🐛 Muammolarni Hal Qilish

### Login Qila Olmayapman

**Muammo:** SMS kod kelmayapti
```
✅ Telefon raqamini to'g'ri kiriting (+998 bilan boshlang)
✅ Bir necha daqiqa kuting
✅ Telegram ilovasida "Login code settings" tekshiring
```

**Muammo:** 2FA parol qabul qilinmayapti
```
✅ Parolni to'g'ri kiritganingizni tekshiring
✅ Telegram ilovasida parolni tekshiring
✅ Agar parolni unutgan bo'lsangiz, Telegram support bilan bog'laning
```

**Muammo:** "Session file is corrupted"
```bash
# Session faylini o'chirib, qaytadan login qiling
rm session_name.session
python telegram_monitor.py
```

### Media Yuklanmayapti

**Muammo:** "MediaEmptyError"
```
✅ Media allaqachon o'chirilgan bo'lishi mumkin
✅ Maxfiy chatlarda ba'zi medialar yuklanmaydi
✅ Tarmoq aloqasini tekshiring
```

**Muammo:** "FloodWaitError"
```
✅ Dastur avtomatik kutadi
✅ Telegram limitlariga rioya qiling
✅ Juda ko'p xabarni bir vaqtda yuklamang
```

### Xatolar va Loglar

**Loglarni ko'rish:**
```bash
tail -f telegram_monitor.log
```

**Batafsil debug ma'lumotlari:**
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## 📚 Qo'shimcha Ma'lumotlar

### Qo'llab-quvvatlanadigan Media Turlari

| Tur | Kengaytmalar | Izoh |
|-----|--------------|------|
| Rasmlar | .jpg, .png, .gif, .webp | Barcha rasm formatlari |
| Videolar | .mp4, .avi, .mov | Video fayllar |
| Audio | .mp3, .ogg | Musiqa va ovozli xabarlar |
| Hujjatlar | .pdf, .docx, .xlsx, va boshqalar | Barcha hujjat turlari |
| Stikerlar | .webp, .tgs | Oddiy va animatsion |
| GIF | .mp4, .gif | Animatsion rasmlar |

### Telethon Hujjatlari

Qo'shimcha imkoniyatlar uchun:
- [Telethon Documentation](https://docs.telethon.dev/)
- [Telethon GitHub](https://github.com/LonamiWebs/Telethon)

## 🤝 Hissa Qo'shish

Agar sizda yaxshilash takliflari bo'lsa:

1. Repository'ni fork qiling
2. O'zgarishlar kiriting
3. Pull request yuboring

## 📄 Litsenziya

Ushbu dastur shaxsiy foydalanish uchun taqdim etilgan.

## ⚡ Tez-tez So'raladigan Savollar

**S: Dastur xavfsizmi?**  
J: Ha, barcha ma'lumotlar mahalliy kompyuteringizda saqlanadi. Lekin API kalitlaringizni maxfiy saqlang.

**S: Boshqa odamlarning xabarlarini ko'ra olamanmi?**  
J: Yo'q, faqat sizga yuborilgan xabarlarni ko'rasiz va saqlaysiz.

**S: Eski xabarlarni yuklab olish mumkinmi?**  
J: Yo'q, faqat dastur ishga tushirilgandan keyin kelgan yangi xabarlar yuklanadi.

**S: Qancha xotira kerak?**  
J: Bu yuklanadigan media hajmiga bog'liq. Katta videolar uchun ko'proq joy kerak.

**S: Dastur har doim ishlab turishi kerakmi?**  
J: Ha, xabarlarni monitoring qilish uchun dastur ishlab turishi kerak.

**S: Mobil telefondan ishlatish mumkinmi?**  
J: Yo'q, bu desktop dastur. Lekin Termux orqali Android'da ishlatish mumkin.

## 📞 Yordam

Muammolar yoki savollar uchun:
  https://t.me/cyber_mikro
---

**Eslatma:** Ushbu dasturni mas'uliyat bilan va qonuniy maqsadlarda ishlating. Boshqa odamlarning shaxsiy hayotini hurmat qiling.

