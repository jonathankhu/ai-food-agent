# ai-food-agent

跑在你自己電腦上的 Discord bot：指定頻道有人傳食物照片，它就請 `claude -p` 分析、
記進 Excel、存照片，再回覆上傳者與當日已攝取熱量。設計見 [docs/architecture.md](docs/architecture.md)。

## 第一次設定

1. 到 Discord Developer Portal 建立 bot，**打開 Message Content Intent**，邀請進你的 Server
   （權限只需要：查看頻道、讀取訊息記錄、傳送訊息）。
2. 複製 `.env.example` 成 `.env`，填入 `DISCORD_TOKEN`、`CHANNEL_ID`、`CLAUDE_MODEL`、`DATA_DIR`。
   `.env` 絕對不能公開、不能 commit。
3. 確認終端機能執行 `claude`，而且已經登入。

## 啟動與測試

```
uv sync
uv run python -m food_agent   # 啟動（關掉終端機就停止處理）
uv run pytest                 # 自動測試
```

## 注意

- 每張照片都會用掉你自己的 Claude 額度；每人每天上限由 `DAILY_PHOTO_LIMIT` 控制（預設 15）。
- 使用時請不要同時用 Excel 開著 `food-log.xlsx`，要看請先複製一份。
- bot 沒開時傳的照片不會補處理，請重傳。
