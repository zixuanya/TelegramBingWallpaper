# TelegramBingWallpaper
利用更加便捷的Python脚本定时脚本实现将 Bing Wallpaper 自动发送到 Telegram 会话中。

---

您只需要将此脚本部署到任何具有python，并且安装了pyrogram的服务器中，Bot长期监测最新壁纸的更新状态

保活本脚本可使用各种方法，例如常见主流的systemd或者init.d等即可保活。

# 操作方法

使用命令安装需要的插件 

```
pip install pyrogram tgcrypto
```

更改代码内部的变量，使用`python bot.py`即可运行使用