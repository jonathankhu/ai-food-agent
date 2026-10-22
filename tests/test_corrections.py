from food_agent.corrections import looks_like_correction, parse_correction


def test_valid_formats():
    assert parse_correction("改成：牛肉麵 650 大卡") == ("牛肉麵", 650.0)
    assert parse_correction("改成:牛肉 麵 650.5大卡") == ("牛肉 麵", 650.5)


def test_invalid_formats():
    for bad in ["改成牛肉麵", "改成：牛肉麵", "改成：牛肉麵 abc 大卡",
                "改成：牛肉麵 99999 大卡", "改成： 650 大卡", "改成：" + "牛" * 60 + " 5 大卡",
                "改成：牛肉麵 -5 大卡", "改成：牛\n肉 5 大卡"]:
        assert parse_correction(bad) is None, bad


def test_looks_like_correction():
    assert looks_like_correction("改成：x")
    assert not looks_like_correction("謝謝")
