import requests
import time
import signal
import sys
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
CHAT_ID = 'channel_username_or_channel_id'

app = Client("wallpaper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def fetch_bing_wallpaper():
    url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&cc=cn"
    response = requests.get(url, headers={"Accept-Language": "zh-CN"}) 
    if response.status_code == 200:
        data = response.json()
        if data.get("images"):
            image_data = data["images"][0]
            title = image_data.get("title", "No Title")
            copyright = image_data.get("copyright", "No Copyright")
            enddate = image_data.get("enddate", "Unknown Date")
            image_url = f"https://www.bing.com{image_data['urlbase']}_UHD.jpg"
            return {
                'title': title,
                'copyright': copyright,
                'enddate': enddate,
                'image_url': image_url
            }
    else:
        print(f"请求 Bing 壁纸失败，状态码：{response.status_code}")

def send_wallpaper_to_channel(wallpaper, chat_id):
    caption = f"{wallpaper['title']}\n{wallpaper['copyright']}\nBing Wallpaper 第 [{wallpaper['enddate']}]({wallpaper['image_url']}) 期" 

    # 创建内联按钮
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("下载壁纸", url=wallpaper['image_url']),
            InlineKeyboardButton("Github项目主页", url="https://github.com/zixuanya/TelegramBingWallpaper")
        ]
    ])
    
    try:
        print(f"准备发送图片到 {chat_id}，图片 URL: {wallpaper['image_url']}")
        app.send_photo(
            chat_id=chat_id,
            photo=wallpaper['image_url'],
            caption=caption,
            reply_markup=keyboard  # 添加按钮
        )
        print("壁纸已发送到 Telegram，下面是壁纸信息：" + caption)
    except Exception as e:
        print(f"发送壁纸时出错: {e}")

def monitor_wallpaper():
    previous_wallpaper_url = None
    while True:
        wallpaper = fetch_bing_wallpaper()
        if wallpaper:
            if wallpaper['image_url'] != previous_wallpaper_url:
                send_wallpaper_to_channel(wallpaper, CHAT_ID)
                previous_wallpaper_url = wallpaper['image_url']
        time.sleep(60)

def signal_handler(sig, frame):
    print("\n检测中断，正在关闭相关进程...")
    app.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    with app:
        monitor_wallpaper()
        app.run()
