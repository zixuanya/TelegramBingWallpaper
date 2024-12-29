addEventListener("scheduled", event => {
  event.waitUntil(handleScheduledEvent());
});

async function handleScheduledEvent() {
  try {
    const wallpaper = await fetchBingWallpaper();
    await sendWallpaperToTelegram(wallpaper);
  } catch (error) {
    console.error("定时任务处理失败：", error.message);
  }
}

async function sendWallpaperToTelegram(wallpaper) {
  const caption = `${wallpaper.title}\n${wallpaper.copyright}\nBing Wallpaper 第 <a href="${wallpaper.imageUrl}">${wallpaper.enddate}</a> 期`;

  const formData = new FormData();
  formData.append("chat_id", TELEGRAM_CHAT_ID);
  formData.append("photo", wallpaper.imageUrl);
  formData.append("caption", caption);
  formData.append("parse_mode", "HTML");

  try {
    const response = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`请求 Telegram API 失败：${errorText}`);
    }
  } catch (error) {
    console.error("向 Telegram 发送壁纸失败：", error.message);
  }
}

async function fetchBingWallpaper() {
  try {
    const response = await fetch(`https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&cc=cn`, {
      headers: { 'Accept-Language': 'zh-CN' }
    });

    if (!response.ok) {
      throw new Error(`获取壁纸数据失败，HTTP 状态码：${response.status}`);
    }

    const data = await response.json();

    if (!data.images || !data.images.length) {
      throw new Error("无法解析壁纸数据：没有图片信息");
    }

    const { enddate, urlbase, title, copyright } = data.images[0];

    if (!enddate || !urlbase || !title || !copyright) {
      throw new Error("壁纸数据不完整");
    }

    return {
      enddate,
      imageUrl: `https://www.bing.com${urlbase}_UHD.jpg`,
      title,
      copyright
    };
  } catch (error) {
    console.error("获取 Bing 壁纸失败：", error.message);
  }
}
