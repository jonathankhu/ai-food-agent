"""所有回覆的文字。"""


def fmt_num(value: float) -> str:
    value = round(float(value), 1)
    return f"{int(value):,}" if value == int(value) else f"{value:,.1f}"


def _total_line(total: float) -> str:
    return f"**當日已攝取熱量：{fmt_num(total)} 大卡**"


PROCESSING = "處理中⋯"
LIMIT_REACHED = "今天的額度用完了，明天再傳。"
CORRECTION_FORMAT_HINT = "請用「改成：名稱 熱量 大卡」的格式。"
NOT_OWNER = "只有上傳者能更正這筆。"
PROCESSING_ERROR = "這張處理時出錯了，請稍後再傳一次。"


def food_result(name: str, ingredients: list[str], weight_g: float, kcal: float, total: float) -> str:
    return "\n".join(
        [
            f"**{name}**",
            f"成份：{'、'.join(ingredients) if ingredients else '（無）'}",
            f"重量：約 {fmt_num(weight_g)} 公克",
            f"熱量：約 {fmt_num(kcal)} 大卡",
            _total_line(total),
        ]
    )


def not_food(thing: str, total: float) -> str:
    return f"你傳的不是食物，是**{thing}**。\n{_total_line(total)}"


def analysis_failed(total: float) -> str:
    return f"這張分析失敗了，請稍後再傳一次。\n{_total_line(total)}"


def correction_ok(name: str, kcal: float, total: float) -> str:
    return f"已更正：**{name}**，{fmt_num(kcal)} 大卡\n{_total_line(total)}"
