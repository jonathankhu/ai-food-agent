"""解析「改成：名稱 熱量 大卡」。由程式自己用固定格式解析，不交給 AI。"""

import re

from .limits import MAX_KCAL, NAME_MAX_LEN

CORRECTION_PREFIX = "改成"
_CORRECTION_RE = re.compile(
    rf"^改成[：:]\s*(\S.{{0,{NAME_MAX_LEN - 1}}}?)\s+(\d+(?:\.\d+)?)\s*大卡\s*$"
)


def looks_like_correction(text: str) -> bool:
    return text.strip().startswith(CORRECTION_PREFIX)


def parse_correction(text: str) -> tuple[str, float] | None:
    """格式正確回傳 (名稱, 熱量)，否則回傳 None。"""
    match = _CORRECTION_RE.match(text.strip())
    if not match:
        return None
    name, kcal = match.group(1).strip(), float(match.group(2))
    if not name or kcal > MAX_KCAL:
        return None
    return name, kcal
