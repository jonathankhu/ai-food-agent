"""排隊與單一工作者：一次只處理一張照片，先進先出。"""

import asyncio
import logging
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Callable

import discord

from . import replies
from .analyzer import AnalysisError, AnalysisResult, analyze_photo
from .config import Config
from .storage import (
    FAILED_NAME,
    NOT_FOOD_NAME,
    FoodLog,
    LogRecord,
    date_of,
    save_photo,
)

log = logging.getLogger(__name__)

# 基本防護 a：回覆時只提及被回覆的人，絕不 @everyone 或 @角色
REPLY_MENTIONS = discord.AllowedMentions(
    everyone=False, roles=False, users=False, replied_user=True
)

Analyze = Callable[[bytes, str, Config], Awaitable[AnalysisResult]]


async def send_reply(message: Any, text: str) -> Any:
    return await message.reply(text, allowed_mentions=REPLY_MENTIONS)


@dataclass
class Job:
    message: Any  # discord.Message：用來回覆
    attachment: Any  # discord.Attachment：用 .read() 下載
    ext: str
    uploader_id: str
    uploader_name: str
    caption: str  # 上傳者打的字，只存進備註欄，絕不交給 claude -p
    when: datetime


class Worker:
    def __init__(self, config: Config, food_log: FoodLog, analyze: Analyze = analyze_photo):
        self.config = config
        self.food_log = food_log
        self.analyze = analyze
        self.queue: asyncio.Queue[Job] = asyncio.Queue()
        self.pending: Counter[str] = Counter()  # 還在排隊、尚未寫進 Excel 的張數

    def can_accept(self, uploader_id: str, when: datetime) -> bool:
        """今天已記錄的張數加上正在排隊的張數，沒超過每人每天上限才收。"""
        used = self.food_log.count_for_user(uploader_id, date_of(when))
        return used + self.pending[uploader_id] < self.config.daily_photo_limit

    def submit(self, job: Job) -> None:
        self.pending[job.uploader_id] += 1
        self.queue.put_nowait(job)

    async def run_forever(self) -> None:
        while True:
            job = await self.queue.get()
            try:
                await self.process(job)
            finally:
                self.pending[job.uploader_id] -= 1
                self.queue.task_done()

    async def process(self, job: Job) -> None:
        """單張出事只會留下紀錄，不會讓整支程式停掉。"""
        try:
            await self._process(job)
        except Exception:
            log.exception("處理照片時出錯")
            try:
                await send_reply(job.message, replies.PROCESSING_ERROR)
            except Exception:
                log.exception("連出錯提示都回不出去")

    async def _process(self, job: Job) -> None:
        photo_bytes = await job.attachment.read()
        try:
            result = await self.analyze(photo_bytes, job.ext, self.config)
        except AnalysisError as exc:
            log.warning("分析失敗，記成失敗列：%s", exc)
            result = None

        if result is None:
            name, ingredients, weight, kcal = FAILED_NAME, "", None, None
        elif result.is_food:
            name = result.name
            ingredients = "、".join(result.ingredients)
            weight, kcal = result.weight_g, result.kcal
        else:
            name, ingredients, weight, kcal = NOT_FOOD_NAME, result.name, None, None

        photo_path = save_photo(
            self.config.photos_dir, photo_bytes, job.ext, name, job.when
        )
        row, total = self.food_log.append(
            LogRecord(
                when=job.when,
                uploader=job.uploader_name,
                name=name,
                ingredients=ingredients,
                weight_g=weight,
                kcal=kcal,
                photo_path=str(photo_path),
                note=job.caption,
                uploader_id=job.uploader_id,
            )
        )

        if result is None:
            text = replies.analysis_failed(total)
        elif result.is_food:
            text = replies.food_result(name, result.ingredients, weight, kcal, total)
        else:
            text = replies.not_food(result.name, total)
        sent = await send_reply(job.message, text)
        self.food_log.set_reply_id(row, sent.id)
