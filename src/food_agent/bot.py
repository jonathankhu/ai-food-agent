"""接 Discord 訊息，決定「是照片？是更正？還是不理」。"""

import asyncio
import logging
from pathlib import PurePath
from typing import Any

import discord

from . import replies
from .config import Config
from .corrections import looks_like_correction, parse_correction
from .storage import FoodLog
from .worker import Job, Worker, send_reply

log = logging.getLogger(__name__)

# 基本防護 b：只收這幾種圖片
PHOTO_EXTENSIONS = {"jpg": "jpg", "jpeg": "jpg", "png": "png", "webp": "webp", "gif": "gif"}


def photo_extension(attachment: Any) -> str | None:
    """是照片就回傳標準化的副檔名，否則回傳 None。"""
    if not (attachment.content_type or "").startswith("image/"):
        return None
    suffix = PurePath(attachment.filename or "").suffix.lstrip(".").lower()
    return PHOTO_EXTENSIONS.get(suffix)


class FoodBot(discord.Client):
    def __init__(self, config: Config, food_log: FoodLog | None = None, worker: Worker | None = None):
        intents = discord.Intents.default()
        intents.message_content = True  # 要在 Developer Portal 也打開
        super().__init__(intents=intents)
        self.config = config
        self.food_log = food_log or FoodLog(config.log_path)
        self.worker = worker or Worker(config, self.food_log)
        self._worker_task: asyncio.Task | None = None

    async def setup_hook(self) -> None:
        self._worker_task = asyncio.create_task(self.worker.run_forever())

    async def on_ready(self) -> None:
        log.info("已登入，只聽頻道 %s", self.config.channel_id)

    async def on_message(self, message: discord.Message) -> None:
        try:
            await self.handle_message(message)
        except Exception:
            log.exception("處理訊息時出錯")

    async def handle_message(self, message: Any) -> None:
        # 基本防護 d：只聽 CHANNEL_ID；bot 的訊息（包含自己的）一律不理
        if message.author.bot or message.channel.id != self.config.channel_id:
            return

        reference = message.reference
        if reference and reference.message_id and looks_like_correction(message.content):
            await self.handle_correction(message, reference.message_id)
            return

        for attachment in message.attachments:
            ext = photo_extension(attachment)
            if ext:
                await self.accept_photo(message, attachment, ext)

    async def accept_photo(self, message: Any, attachment: Any, ext: str) -> None:
        when = message.created_at.astimezone()
        uploader_id = str(message.author.id)
        if not self.worker.can_accept(uploader_id, when):
            await send_reply(message, replies.LIMIT_REACHED)
            return
        # 先登記進隊伍（同步，不會被別張插隊），再回「處理中」
        self.worker.submit(
            Job(
                message=message,
                attachment=attachment,
                ext=ext,
                uploader_id=uploader_id,
                uploader_name=message.author.display_name,
                caption=message.content,
                when=when,
            )
        )
        await send_reply(message, replies.PROCESSING)

    async def handle_correction(self, message: Any, replied_id: int) -> None:
        row = self.food_log.find_by_reply_id(replied_id)
        if row is None:
            return  # 回覆的不是 bot 的結果訊息，當一般訊息不理
        if row.uploader_id != str(message.author.id):
            await send_reply(message, replies.NOT_OWNER)
            return
        parsed = parse_correction(message.content)
        if parsed is None:
            await send_reply(message, replies.CORRECTION_FORMAT_HINT)
            return
        name, kcal = parsed
        _date, total = self.food_log.apply_correction(row.row, name, kcal)
        await send_reply(message, replies.correction_ok(name, kcal, total))
