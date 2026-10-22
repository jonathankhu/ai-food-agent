"""清洗外來文字：防護 3（檔名）與防護 4（Excel 公式）。

每一段防護都用「開始 / 結束」註解框起來。整段註解掉之後，函式仍然能跑，
只是不再清洗。
"""

import re
import unicodedata

FILENAME_MAX_LEN = 20
_FILENAME_BAD_CHARS = re.compile(r'[/\\:*?"<>|]')
_FORMULA_STARTERS = ("=", "+", "-", "@", "\t", "\r", "\n")


def clean_filename_part(text: str, max_len: int = FILENAME_MAX_LEN) -> str:
    """把 AI 回來的食物名稱變成可以安全放進檔名的簡稱。"""
    # >>>>>>>>>> 防護 3 開始：食物名稱當檔名前先清洗 <<<<<<<<<<
    text = _FILENAME_BAD_CHARS.sub("_", text)
    # 控制字元、看不見的方向字元等（Unicode 類別 C 開頭）一律換掉
    text = "".join("_" if unicodedata.category(ch)[0] == "C" else ch for ch in text)
    text = text.replace("..", "_")
    text = re.sub(r"\s+", "_", text)
    text = text.lstrip(".")
    text = text[:max_len]
    if not text:
        text = "未命名"
    # >>>>>>>>>> 防護 3 結束 <<<<<<<<<<
    return text


def write_text_cell(cell, value) -> None:
    """把外來文字寫進 Excel 儲存格。"""
    text = str(value)
    # >>>>>>>>>> 防護 4 開始：以 = + - @ 開頭的文字加單引號 <<<<<<<<<<
    if text.startswith(_FORMULA_STARTERS):
        text = "'" + text
    # >>>>>>>>>> 防護 4 結束 <<<<<<<<<<
    cell.value = text
    # >>>>>>>>>> 防護 4 開始：明確標成文字格式，不讓 Excel 當公式 <<<<<<<<<<
    cell.data_type = "s"
    # >>>>>>>>>> 防護 4 結束 <<<<<<<<<<
