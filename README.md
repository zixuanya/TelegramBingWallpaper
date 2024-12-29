# TelegramBingWallpaper
使用 Cloudflare Workers 定时脚本实现将 Bing Wallpaper 自动发送到 Telegram 会话中。

---

您只需要将此脚本部署到 Cloudflare Workers 中，然后配置环境变量和 Cron 定时器即可。

在项目设置页面设置环境变量 `TELEGRAM_BOT_TOKEN` 为您的 Telegram Bot API Token，  
将 `TELEGRAM_CHAT_ID` 设置为您要让脚本自动发送 Bing Wallpaper 的 Telegram 的聊天 Chat ID，可频道、群聊、私信。

然后设置触发事件，定义调用 Worker 的事件，  
添加一个 Cron 触发器设置时间即可，注意时区。
