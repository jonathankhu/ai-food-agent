# ai-food-agent

一支跑在本機的 Discord bot：頻道裡有人傳食物照片，就用 `claude -p` 分析、記進 Excel、存照片，並回覆上傳者與當日已攝取熱量。

## 開始任何工作前

先讀 `docs/architecture.md`。需求在 `docs/requirements.md`。不要加入文件裡沒有的功能；要加，先跟使用者確認。

## 四段防護

下面四段防護在程式裡都要用清楚的註解標出「開始 / 結束」，格式如下，**一開始全部開啟**：

```python
# >>>>>>>>>> 防護 N 開始：說明 <<<<<<<<<<
...
# >>>>>>>>>> 防護 N 結束 <<<<<<<<<<
```

| 編號 | 防護 | 位置 |
|---|---|---|
| 1 | claude -p 讀不到 DATA_DIR（工作目錄、只開 Read 工具、禁止讀 DATA_DIR） | `src/food_agent/analyzer.py` |
| 2 | 照片裡的字與上傳者打的字只能當資料，不能當指令 | `src/food_agent/analyzer.py` |
| 3 | 食物名稱當檔名前清洗，並確認路徑沒跑出照片資料夾 | `src/food_agent/sanitize.py`、`storage.py` |
| 4 | 寫進 Excel 的文字若以 `=`、`+`、`-`、`@` 開頭要變純文字 | `src/food_agent/sanitize.py` |

之後上課會把這四段逐段關掉做對照，所以每一段都要能整段註解掉、程式仍能跑。**不要擅自關掉、移動或合併這些區塊。**

## 不可以 commit 的東西

- **`.env`**：裡面有 `DISCORD_TOKEN`，絕對不能 commit 或公開。只 commit `.env.example`。
- **`DATA_DIR` 裡的照片和 Excel**：不要 commit。`DATA_DIR` 預設在 repo 之外；`.gitignore` 也已擋掉 `*.xlsx` 與 `photos/`。

commit 之前先看 `git status`，確認沒有上面這些檔案。

## 常用指令

```
uv sync                       # 安裝套件
uv run python -m food_agent   # 啟動 bot
uv run pytest                 # 自動測試
```
