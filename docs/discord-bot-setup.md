# 設定 Discord Bot

這份文件帶你做五件事：

1. 在 **Discord Developer Portal**（Discord 給開發者的管理網站）建立一個 application 和 bot。
2. 打開 **Message Content Intent**（一個必要的權限開關）。
3. 取得 **bot token**（bot 的密碼）。
4. 選好權限，產生邀請連結，把 bot 邀進你的 Server。
5. 把設定填進 `.env`。

> 電腦是 **macOS**。「右鍵」指的是：在觸控板上用兩指點一下，或是按住 `control` 再點一下。
> 畫面如果和這裡不一樣，找意思最接近的字，或是把你看到的描述給我。

**前提**：你已經照 [docs/discord-server-setup.md](discord-server-setup.md) 建好自己的 Server 和 `food-log` 頻道。

---

## 重要警告：bot token

> ### 🔴 bot token 絕對不能：
> - **貼給任何人**（同學、朋友、老師都不行，包含你信任的人）
> - **貼進和 Claude 的對話裡**
> - **貼進任何 Discord 頻道、群組、截圖**
> - **commit 進 git**，或是上傳到 GitHub
>
> **為什麼？** 拿到 token 的人，可以完全控制你的 bot：用它發訊息、讀它看得到的所有訊息，並且冒充你的 bot。
>
> **它只能放在一個地方**：你電腦上專案資料夾裡的 `.env` 檔案。`.env` 已經被 `.gitignore` 擋住，不會被 git 收進去。
>
> **萬一洩漏了**（貼錯地方、截圖到了）：馬上回到 Developer Portal 按 **Reset Token**，舊的 token 立刻失效。**光是刪掉訊息或檔案沒有用**，因為別人可能已經複製走了。

---

## 一、建立 application 和 bot

1. 用瀏覽器打開 https://discord.com/developers/applications 。用你的 Discord 帳號登入。
2. 點畫面**右上角**的藍色按鈕 **「New Application」**。
3. 在「Name」欄位輸入名稱，例如 `食物記錄`。這個名字會是 bot 在 Discord 裡的名字。
4. 勾選同意條款的方塊，點 **「Create」**。
5. 你進到這個 application 的管理頁。看**左邊選單**，點 **「Bot」**。（application 建立時會自動帶一個 bot，不用另外建立。）

---

## 二、打開 Message Content Intent

**這一步一定要做。**

### 為什麼？

Discord 預設不讓 bot 讀取別人訊息的「內容」。bot 只會看到「有人傳了一則訊息」，但看不到：

- **附件**（也就是那張食物照片）
- **文字內容**（例如更正用的「改成：牛肉麵 650 大卡」，以及照片附的備註）

**沒有打開這個開關，bot 連線得上、看起來正常，但收到的照片是「空的」，什麼都不會發生**，而且不會有任何錯誤訊息。這是新手最常卡住的地方。

### 怎麼做

1. 還在左邊選單的 **「Bot」** 頁面。
2. 用滑鼠往下捲，找到一個區塊叫 **「Privileged Gateway Intents」**。
3. 在裡面找到 **「Message Content Intent」**，把右邊的開關**打開**（變成藍色）。
4. 另外兩個（Presence Intent、Server Members Intent）**保持關閉**，我們用不到。
5. 頁面下方會跳出一條提示，點 **「Save Changes」**（儲存變更）。沒按這個，設定不會生效。

---

## 三、取得 bot token

1. 在同一個 **「Bot」** 頁面，往上找到 **「Token」** 區塊。
2. 點 **「Reset Token」**（第一次可能顯示 **Copy**，如果是這樣，直接跳到第 4 步）。
3. 跳出確認視窗，點 **「Yes, do it!」**。如果要求輸入密碼或兩步驟驗證碼，照做。
4. 畫面上會出現一串很長的亂碼，旁邊有 **「Copy」** 按鈕，點它。
5. **只會顯示這一次**，關掉頁面就看不到了（但可以再 Reset 產生新的）。

### 暫存 token 的方式

- **不要**貼到備忘錄的共用資料夾、不要貼到 Line、Email、Discord、這個對話。
- 最好的做法：**不要暫存，直接進行下面「五、填進 .env」**，趁剪貼簿裡還有 token，馬上貼進 `.env`。

---

## 四、選權限、把 bot 邀進你的 Server

### 4-1 讓只有你能邀請這個 bot（建議）

1. 還在左邊選單 **「Bot」** 頁面，找到 **「Public Bot」** 開關。
2. 把它**關閉**。這樣別人拿到你的 bot 資訊，也沒辦法把它邀到他們自己的 Server。
3. 如果頁面下方跳出 **「Save Changes」**，點它。

### 4-2 產生邀請連結

1. 看**左邊選單**，點 **「OAuth2」**。
2. 往下找到 **「OAuth2 URL Generator」**（或 **URL Generator**）。
3. 在 **「Scopes」** 區塊，只勾 **`bot`**。
4. 勾了之後，下面會出現 **「Bot Permissions」** 區塊。**只勾這三個**：

| 權限（英文） | 中文大意 | 為什麼需要 |
|---|---|---|
| **View Channels** | 查看頻道 | 才看得到 `food-log` 頻道 |
| **Send Messages** | 傳送訊息 | 才能回覆「處理中」和結果 |
| **Read Message History** | 讀取訊息歷史 | bot 用「回覆」的方式接在你的訊息下面，Discord 規定要有這個權限 |

5. **其他都不要勾**，特別是 **Administrator**（管理員）。給 bot 最少的權限，萬一出事傷害最小。
6. 往下捲到頁面最底下，找到 **「Generated URL」**，旁邊有 **「Copy」** 按鈕，點它。

> 這個「邀請 bot 的連結」和 Server 設定文件裡「邀請同學的連結」是**兩個不同的東西**，不要搞混。
> bot 的邀請連結不是密碼，但還是只自己用，不用傳給別人。

### 4-3 把 bot 加進 Server

1. 打開一個**新的瀏覽器分頁**，把剛剛複製的連結貼到網址列，按 `Enter`。
2. 畫面會問「要把 bot 加到哪個 Server」。點下拉選單，選**你自己的 Server**（例如 `食物記錄實驗室`）。
3. 點 **「繼續」**（**Continue**）。
4. 畫面列出它要的三個權限，確認和上表一樣，點 **「授權」**（**Authorize**）。
5. 如果出現「我不是機器人」的驗證，照著做。
6. 看到「已授權」就成功了。

### 4-4 確認 bot 進來了

1. 回到 Discord，進到你的 Server。
2. 點右上角的 **人像圖示**（顯示成員名單）。
3. 往下看，**「機器人」（BOT）** 分類下面應該有你的 bot，旁邊有一個小小的「BOT」標籤。
4. 它現在顯示 **離線**，這是正常的，因為 agent 程式還沒啟動。

---

## 五、填進 .env

`.env` 是放設定值的檔案，agent 啟動時從這裡讀 token 和頻道編號。

### 5-1 建立 .env

1. 打開 **「終端機」**（Terminal）。按 `command` + `空白鍵` 叫出搜尋，輸入 `終端機` 再按 `Enter`。
2. 輸入下面這行，按 `Enter`，進到專案資料夾：

```
cd ~/Desktop/ai-food-agent
```

3. 輸入下面這行，按 `Enter`，複製出你的 `.env`：

```
cp .env.example .env
```

4. 輸入下面這行，按 `Enter`，用「文字編輯」打開它：

```
open -e .env
```

### 5-2 填入設定

文字編輯會打開一個檔案，內容大概像這樣。**把等號後面換成你的真實值**：

```
DISCORD_TOKEN=請填你的_bot_token
CHANNEL_ID=123456789012345678
CLAUDE_MODEL=claude-sonnet-5-5
DATA_DIR=~/food-agent-data
DAILY_PHOTO_LIMIT=15
```

| 項目 | 要填什麼 |
|---|---|
| `DISCORD_TOKEN` | 這份文件第三步複製的 token。**等號後面直接貼，不要加引號、不要有空格** |
| `CHANNEL_ID` | Server 設定文件第三步複製的頻道編號（純數字） |
| `CLAUDE_MODEL` | 先不用改 |
| `DATA_DIR` | 照片和 Excel 要放的資料夾，先不用改 |
| `DAILY_PHOTO_LIMIT` | 每人每天最多幾張，先不用改 |

填好後按 `command` + `S` 存檔，再關掉。

### 5-3 確認沒有被 git 追蹤

在終端機輸入：

```
git status
```

畫面**不應該**出現 `.env`。如果有出現，**立刻停手，不要 commit**，告訴我。（正常情況下不會，因為 `.gitignore` 已經擋住它。）

---

## 做完後的檢查清單

- [ ] Developer Portal 裡有我的 application，名稱是 `食物記錄`（或我取的名字）
- [ ] **Message Content Intent 已打開**，並且按了 Save Changes
- [ ] 我取得了 bot token，並且**沒有**貼給任何人、沒有貼進 Claude 的對話
- [ ] Public Bot 已關閉
- [ ] 邀請連結只勾了 `bot` 和三個權限（View Channels、Send Messages、Read Message History）
- [ ] Server 的成員名單裡看得到我的 bot（離線是正常的）
- [ ] `.env` 已建立並填好 `DISCORD_TOKEN` 和 `CHANNEL_ID`
- [ ] `git status` 看不到 `.env`

---

## 常見問題

| 狀況 | 可能原因 |
|---|---|
| 看不到「Bot」頁面的 Intents | 往下捲，它在頁面中間偏下 |
| bot 啟動了但傳照片沒反應 | **Message Content Intent 沒打開**，或打開了沒按 Save Changes |
| 啟動時顯示 `LoginFailure`／token 錯誤 | token 貼錯了（多了空格、引號、或漏複製一段），或 token 已經被 Reset 過。回 Developer Portal 重新 Reset Token，再貼一次 |
| bot 在頻道裡沒反應，也沒有錯誤 | `CHANNEL_ID` 填錯了頻道，或 bot 沒有 View Channels／Send Messages 權限 |
| 邀請 bot 時選單裡沒有我的 Server | 你不是那個 Server 的擁有者或管理員，確認是用建立 Server 的那個帳號登入 |
| 不小心洩漏了 token | 立刻到 Developer Portal → Bot → **Reset Token**，再把新的填進 `.env` |

---

## 下一步

資料都就緒了，回到對話告訴我「Discord 設定完成」，我們就可以啟動 agent，傳第一張照片測試。
