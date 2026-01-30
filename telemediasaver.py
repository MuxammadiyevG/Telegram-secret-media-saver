import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient, events, types
from telethon.errors import FloodWaitError, MediaEmptyError, SessionPasswordNeededError

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(
        "telegram_monitor.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Konfiguratsiya - o'z qiymatlaringizni kiriting
API_ID = ""
API_HASH = ""
PHONE_NUMBER = ""

# Timestamped output papkasini yaratish
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"telegram_media_{timestamp}"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# Telethon clientni ishga tushirish
client = TelegramClient("session_name", API_ID, API_HASH)


async def login_with_phone():
    """
    Telefon raqami orqali login (2FA qo'llab-quvvatlash bilan)
    """
    try:
        phone = PHONE_NUMBER
        if not phone.startswith("+"):
            phone = "+" + phone

        logger.info(f"Telefon raqamiga kod yuborilmoqda: {phone}")
        await client.send_code_request(phone)

        print("\n" + "=" * 60)
        print(f"📱 Telegram'dan kelgan kodni kiriting ({phone})")
        print("Kod kelmasa, bir necha daqiqa kuting")
        print("=" * 60)

        # Kodni so'rash
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                code = input(
                    f"\n🔑 Telegram kodi (urinish {attempt+1}/{max_attempts}): "
                ).strip()

                if not code:
                    print("❌ Kod kiritilmadi, qaytadan urinib ko'ring...")
                    continue

                # Koddan bo'sh joylarni olib tashlash
                code = code.replace(" ", "").replace("-", "")

                # Login urinishi
                logger.info("Kod bilan login qilinmoqda...")
                await client.sign_in(phone, code)

                # Muvaffaqiyatli!
                me = await client.get_me()
                logger.info(f"✓ Muvaffaqiyatli kirildi: {
                    me.first_name} (@{me.username})")
                return True

            except SessionPasswordNeededError:
                # Ikki faktorli autentifikatsiya kerak
                print("\n" + "=" * 60)
                print("🔒 Ikki faktorli autentifikatsiya (2FA) yoqilgan")
                print("=" * 60)

                password_attempts = 3
                for pwd_attempt in range(password_attempts):
                    try:
                        password = input(f"\n🔐 2FA parolingizni kiriting (urinish {
                            pwd_attempt+1}/{password_attempts}): ").strip()

                        if not password:
                            print("❌ Parol kiritilmadi")
                            continue

                        logger.info("2FA parol tekshirilmoqda...")
                        await client.sign_in(password=password)

                        # Muvaffaqiyatli!
                        me = await client.get_me()
                        logger.info(f"✓ 2FA orqali muvaffaqiyatli kirildi: {
                            me.first_name}")
                        return True

                    except Exception as pwd_error:
                        logger.error(f"Parol xato: {pwd_error}")
                        print(f"❌ Xato: {pwd_error}")

                        if pwd_attempt < password_attempts - 1:
                            print("Qaytadan urinib ko'ring...")
                        else:
                            print("❌ Barcha parol urinishlari tugadi")
                            return False

            except Exception as e:
                logger.error(f"Login xatosi: {e}")
                print(f"❌ Xato: {e}")

                if attempt < max_attempts - 1:
                    print("Qaytadan urinib ko'ring...")
                    await asyncio.sleep(2)
                else:
                    print("❌ Barcha urinishlar tugadi")
                    return False

        return False

    except Exception as e:
        logger.error(f"Telefon login xatosi: {str(e)}", exc_info=True)
        return False


async def login_with_qr_and_password():
    """
    QR kod orqali login (2FA qo'llab-quvvatlash bilan)
    """
    try:
        logger.info("QR kod login usuli tanlandi")
        qr_login = await client.qr_login()

        print("\n" + "=" * 60)
        print("📱 QR KODNI SKANERLANG:")
        print("Telegram ilovasida:")
        print("Settings → Devices → Link Desktop Device")
        print("=" * 60 + "\n")

        # QR kodni ko'rsatish
        try:
            import qrcode

            qr = qrcode.QRCode()
            qr.add_data(qr_login.url)
            qr.print_ascii()
        except ImportError:
            print(f"QR kod URL: {qr_login.url}")
            print("\n💡 Yaxshiroq ko'rish uchun: pip install qrcode")

        print("\n⏳ QR kod skanerlashini kutish (5 daqiqa)...")

        # QR kod tasdiqlanishini kutish
        try:
            await qr_login.wait(timeout=300)
            me = await client.get_me()
            logger.info(f"✓ QR kod orqali muvaffaqiyatli kirildi: {
                me.first_name}")
            return True

        except SessionPasswordNeededError:
            # 2FA parol kerak
            print("\n" + "=" * 60)
            print("🔒 Ikki faktorli autentifikatsiya (2FA) kerak")
            print("=" * 60)

            password_attempts = 3
            for attempt in range(password_attempts):
                try:
                    password = input(f"\n🔐 2FA parolingizni kiriting (urinish {
                        attempt+1}/{password_attempts}): ").strip()

                    if not password:
                        print("❌ Parol kiritilmadi")
                        continue

                    logger.info("2FA parol tekshirilmoqda...")
                    await client.sign_in(password=password)

                    me = await client.get_me()
                    logger.info(f"✓ 2FA orqali muvaffaqiyatli kirildi: {
                        me.first_name}")
                    return True

                except Exception as e:
                    logger.error(f"Parol xato: {e}")
                    print(f"❌ Xato: {e}")

                    if attempt < password_attempts - 1:
                        print("Qaytadan urinib ko'ring...")
                    else:
                        return False

            return False

        except asyncio.TimeoutError:
            logger.error("QR kod vaqti tugadi")
            print("❌ QR kod vaqti tugadi (5 daqiqa)")
            return False

    except Exception as e:
        logger.error(f"QR login xatosi: {str(e)}", exc_info=True)
        print(f"❌ QR login xatosi: {e}")
        return False


async def login_with_retry():
    """
    Telegram'ga login qilish - turli usullar bilan
    """
    try:
        logger.info("Telegram'ga ulanish boshlandi...")

        # Agar allaqachon sessiya mavjud bo'lsa
        if await client.is_user_authorized():
            me = await client.get_me()
            logger.info(f"✓ Allaqachon tizimga kirilgan: {me.first_name}")
            return True

        # Login usulini tanlash
        print("\n" + "=" * 60)
        print("🔐 LOGIN USULINI TANLANG:")
        print("=" * 60)
        print("1. 📱 Telefon raqami va SMS kod (tavsiya etiladi)")
        print("2. 📲 QR kod (telefondan skanerlash)")
        print("=" * 60)

        choice = input("\nTanlov (1 yoki 2, Enter = 1): ").strip()

        if not choice:
            choice = "1"

        if choice == "2":
            # QR kod orqali
            success = await login_with_qr_and_password()
        else:
            # Telefon orqali
            success = await login_with_phone()

        if success:
            print("\n" + "=" * 60)
            print("✅ MUVAFFAQIYATLI LOGIN!")
            print("=" * 60 + "\n")
        else:
            print("\n" + "=" * 60)
            print("❌ LOGIN AMALGA OSHMADI")
            print("=" * 60 + "\n")

        return success

    except Exception as e:
        logger.error(f"Login qilishda xatolik: {str(e)}", exc_info=True)
        return False


async def handle_message(event):
    """
    Kiruvchi xabarlarni qayta ishlash va kerak bo'lsa mediani yuklab olish.

    Args:
        event: Telethon dan kelgan xabar hodisasi
    """
    try:
        message = event.message

        # Media mavjudligini tekshirish
        if not message.media:
            return

        # TTL (o'z-o'zidan o'chiradigan) xabarlarni tekshirish
        if (
            hasattr(message, "ttl_seconds")
            and message.ttl_seconds
            and message.ttl_seconds > 0
        ):
            chat_name = "Unknown"
            if event.chat:
                chat_name = getattr(event.chat, "title", None) or getattr(
                    event.chat, "username", "Private"
                )

            logger.info(f"TTL xabar topildi: {
                message.ttl_seconds}s, Chat: {chat_name}")
            await process_media(message, "ttl_chat", event.chat_id)
            return

        # "Bir marta ko'rish" xabarlarini tekshirish
        if isinstance(
            message.media, (types.MessageMediaPhoto,
                            types.MessageMediaDocument)
        ):
            if hasattr(message.media, "ttl_seconds") and message.media.ttl_seconds:
                logger.info("Bir marta ko'rish xabari topildi")
                await process_media(message, "view_once", event.chat_id)
                return

        # Maxfiy chat medialarini tekshirish
        if event.is_private and hasattr(event, "input_chat"):
            if isinstance(event.input_chat, types.InputEncryptedChat):
                logger.info("Maxfiy chat mediasi topildi")
                await process_media(message, "secret_chat", event.chat_id)
                return

    except Exception as e:
        logger.error(
            f"Xabarni qayta ishlashda xatolik: {
                str(e)}",
            exc_info=True,
        )


def get_media_info(message):
    """Media haqida ma'lumot olish va fayl kengaytmasini aniqlash."""
    media_info = {"file_id": None, "ext": ".bin",
                  "media_name": "unknown", "size": 0}

    if isinstance(message.media, types.MessageMediaPhoto):
        media_info["file_id"] = message.media.photo.id
        media_info["ext"] = ".jpg"
        media_info["media_name"] = "photo"
        if message.media.photo.sizes:
            media_info["size"] = max(
                [s.size if hasattr(s, "size")
                 else 0 for s in message.media.photo.sizes]
            )

    elif isinstance(message.media, types.MessageMediaDocument):
        doc = message.media.document
        media_info["file_id"] = doc.id
        media_info["size"] = doc.size
        media_info["media_name"] = "document"

        mime_to_ext = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "video/mp4": ".mp4",
            "video/avi": ".avi",
            "video/quicktime": ".mov",
            "audio/mpeg": ".mp3",
            "audio/ogg": ".ogg",
            "application/pdf": ".pdf",
        }

        if doc.mime_type in mime_to_ext:
            media_info["ext"] = mime_to_ext[doc.mime_type]

        for attr in doc.attributes:
            if isinstance(attr, types.DocumentAttributeFilename):
                file_ext = os.path.splitext(attr.file_name)[1]
                if file_ext:
                    media_info["ext"] = file_ext.lower()
                media_info["media_name"] = "file"

            elif isinstance(attr, types.DocumentAttributeVideo):
                if not media_info["ext"].startswith("."):
                    media_info["ext"] = ".mp4"
                media_info["media_name"] = "video"

            elif isinstance(attr, types.DocumentAttributeAudio):
                if attr.voice:
                    media_info["media_name"] = "voice"
                    if not media_info["ext"] or media_info["ext"] == ".bin":
                        media_info["ext"] = ".ogg"
                else:
                    media_info["media_name"] = "audio"
                    if not media_info["ext"] or media_info["ext"] == ".bin":
                        media_info["ext"] = ".mp3"

            elif isinstance(attr, types.DocumentAttributeAnimated):
                media_info["media_name"] = "gif"
                if not media_info["ext"] or media_info["ext"] == ".bin":
                    media_info["ext"] = ".mp4"

            elif isinstance(attr, types.DocumentAttributeSticker):
                media_info["media_name"] = "sticker"
                if not media_info["ext"] or media_info["ext"] == ".bin":
                    media_info["ext"] = ".webp"

    return media_info


async def process_media(message, media_type, chat_id):
    """
    Xabardagi mediani qayta ishlash va yuklab olish.

    Args:
        message: Telegram xabar obyekti
        media_type: Media manbai turi ("ttl_chat", "view_once", "secret_chat")
        chat_id: Chat identifikatori
    """
    if not message.media:
        return

    try:
        subdir_map = {
            "ttl_chat": "ttl_chats",
            "view_once": "view_once",
            "secret_chat": "secret_chats",
        }

        subdir = subdir_map.get(media_type, "other")
        subdir_path = Path(OUTPUT_DIR) / subdir
        subdir_path.mkdir(exist_ok=True)

        if isinstance(message.media, types.MessageMediaWebPage):
            logger.info("Web sahifa mediasi - o'tkazib yuborildi")
            return

        media_info = get_media_info(message)

        if not media_info["file_id"]:
            logger.warning(
                f"Qo'llab-quvvatlanmaydigan media turi: {type(message.media)}"
            )
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{media_type}_{media_info['media_name']}_chat{
            chat_id}_{media_info['file_id']}_{timestamp}{media_info['ext']}"
        filepath = subdir_path / filename

        size_mb = media_info["size"] / (1024 * 1024)
        size_str = (
            f"{size_mb:.2f} MB"
            if size_mb > 1
            else f"{media_info['size'] / 1024:.2f} KB"
        )

        logger.info(f"Yuklab olinmoqda: {
            media_info['media_name']} ({size_str}) -> {filename}")

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:

                def progress_callback(current, total):
                    percent = (current / total) * 100 if total > 0 else 0
                    if int(percent) % 10 == 0:
                        logger.info(f"Yuklash jarayoni: {
                            percent:.1f}% ({current}/{total} bytes)")

                await client.download_media(
                    message, file=str(filepath), progress_callback=progress_callback
                )
                logger.info(f"✓ Muvaffaqiyatli yuklandi: {filepath}")

                metadata_file = filepath.with_suffix(filepath.suffix + ".txt")
                with open(metadata_file, "w", encoding="utf-8") as f:
                    f.write(f"Media Type: {media_info['media_name']}\n")
                    f.write(f"Source: {media_type}\n")
                    f.write(f"Chat ID: {chat_id}\n")
                    f.write(f"Message ID: {message.id}\n")
                    f.write(f"Date: {message.date}\n")
                    f.write(f"File Size: {size_str}\n")
                    f.write(f"Extension: {media_info['ext']}\n")
                    if message.text:
                        f.write(f"Caption: {message.text}\n")
                    if hasattr(message, "ttl_seconds") and message.ttl_seconds:
                        f.write(f"TTL: {message.ttl_seconds} seconds\n")

                break

            except FloodWaitError as e:
                wait_time = e.seconds
                logger.warning(f"FloodWait: {wait_time} soniya kutish kerak")
                await asyncio.sleep(wait_time)
                retry_count += 1

            except MediaEmptyError:
                logger.error("Media bo'sh - yuklab bo'lmadi")
                break

            except Exception as e:
                logger.error(f"Yuklab olishda xatolik: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(5)
                else:
                    break

    except Exception as e:
        logger.error(
            f"Mediani qayta ishlashda xatolik: {
                str(e)}",
            exc_info=True,
        )


async def main():
    """Telegram clientni ishga tushirish va xabarlarni monitoring qilish."""
    try:
        # Telegram'ga ulanish
        await client.connect()

        # Login qilish
        if not await login_with_retry():
            logger.error("❌ Login amalga oshmadi!")
            print("\n💡 Maslahatlar:")
            print("- Telefon raqami to'g'ri kiritilganligini tekshiring")
            print("- SMS kod kelmasa, bir necha daqiqa kuting")
            print("- 2FA parolingizni to'g'ri kiritganingizga ishonch hosil qiling")
            print("- session_name.session faylini o'chirib, qaytadan urinib ko'ring")
            return

        logger.info(f"📁 Media saqlash papkasi: {OUTPUT_DIR}")

        # Barcha kiruvchi xabarlarni monitoring qilish
        @client.on(events.NewMessage())
        async def handler(event):
            await handle_message(event)

        print("\n" + "=" * 60)
        print("✅ MONITORING BOSHLANDI")
        print("=" * 60)
        logger.info("👀 Xabarlarni monitoring qilish boshlandi...")
        logger.info("⛔ To'xtatish uchun Ctrl+C bosing")

        await client.run_until_disconnected()

    except KeyboardInterrupt:
        logger.info("\n⛔ Foydalanuvchi tomonidan to'xtatildi")
    except Exception as e:
        logger.error(f"Main funksiyada xatolik: {str(e)}", exc_info=True)
    finally:
        await client.disconnect()
        logger.info("👋 Client o'chirildi")


if __name__ == "__main__":
    # Konfiguratsiyani tekshirish
    if API_ID == "your_api_id_here" or API_HASH == "your_api_hash_here":
        logger.error("Iltimos, API_ID va API_HASH ni sozlang!")
        sys.exit(1)

    if PHONE_NUMBER == "your_phone_number_here":
        logger.error("Iltimos, PHONE_NUMBER ni sozlang!")
        sys.exit(1)

    # Asinxron funksiyani ishga tushirish
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Dastur to'xtatildi")
    except Exception as e:
        logger.error(f"Dasturda xatolik: {str(e)}", exc_info=True)
