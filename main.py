from pyrogram import Client
from pyrogram import filters
from pyrogram.types import *
from pyrogram.raw import functions, types
import time
import math
import uvloop


uvloop.install()

bot = Client(
    "my_account",
    api_id=1695325,
    api_hash="16dc6d1578130db531344b941306537e",
    bot_token="2005686417:AAGx9AJDTAKkV2Ounxh6ZwSdVKqCorXseF0",
    # proxy=dict(scheme="socks5", hostname="127.0.0.1", port=10820),
)





async def download_file(client, message):
    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo.file_id
    else:
        print("No downloadable content found.")
        return

    file_path = f"downloads/{file.file_name}"  # مسیر ذخیره فایل

    file_id = file.file_id
    file_access_hash = "16dc6d1578130db531344b941306537e"
    file_reference = 1695325
    file_size = file.file_size

    offset = 0
    limit = 1024 * 1024  # 1 MB chunks

    with open(file_path, "wb") as f:
        while True:
            chunk = await client.invoke(
                functions.upload.GetFile(
                    location=types.InputDocumentFileLocation(
                        id=file_id,
                        access_hash=file_access_hash,
                        file_reference=file_reference,
                        thumb_size=""
                    ),
                    offset=offset,
                    limit=limit
                )
            )

            if not chunk.bytes:
                break

            f.write(chunk.bytes)
            offset += len(chunk.bytes)

            print(f"Downloaded {offset}/{file_size} bytes")

    print(f"File downloaded: {file_path}")






async def progressDownload(current, total):
    print(
        f"""
        Downloading...
        current:{round(current/1024)}
        total:{round(total/1024)}
        {current * 100 / total:.1f}%"""
    )


async def progress(current, total, message):
    percent = current * 100 / total
    percentDetermine = 100 - percent
    total = math.ceil(total / 1024)
    current = math.ceil(current / 1024)
    determine = math.ceil(total - current)
    
    
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=f""" سایز فایل: {total}kb
        دانلود شده:{current}kb
        باقی مانده : {determine}kb
        درصد باقی مانده : {percentDetermine:.1f}%
        در حال دانلود: {percent:.1f}% """,
    )
    time.sleep(50 / 1000)


@bot.on_message()
async def handle_download(client, message):
    sent_message = await bot.send_message(message.chat.id, "دانلود شروع شد...")
    await bot.download_media(message,progress=progress,progress_args=(sent_message,))
    await bot.edit_message_text(client.me.id, sent_message.id, f"""
                                دانلود به اتمام رسید
                                Link:https://colab.research.google.com/tun/m/m-s-23j6h4hha0x4p/files/home/test/downloads/{message.document.file_name}?authuser=1
                                """)
    


bot.run()


# @bot.on_message()
# async def start(client, message):
#     await bot.send_message(message.chat.id, "started")
#     await bot.download_media(message, progress=lambda current, total:progress(current, total, message))




# # آدرس فایل مورد نظر برای دانلود
# url = input("Enter the URL of the file to download: ")

# # ارسال درخواست و دریافت پاسخ
# response = requests.get(url, stream=True)

# # بررسی وضعیت درخواست
# if response.status_code == 200:
#     # دریافت اندازه کل فایل
#     total_size = int(response.headers.get('content-length', 0))
#     contentType  = response.headers.get('Content-Type')


#     # باز کردن فایل برای نوشتن
#     with open("downloaded_file.rar", 'wb') as file:
#         # استفاده از tqdm برای نمایش نوار پیشرفت
#         for data in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB'):
#             file.write(data)
# else:
#     print("Failed to retrieve the file.")
