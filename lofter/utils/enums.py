import enum as _enum


class TagType(str, _enum.Enum):
    NEW = "new"
    """最新"""
    DATE = "date"
    """日榜"""
    WEEK = "week"
    """周榜"""
    MONTH = "month"
    """月榜"""
    TOTAL = "total"
    """总榜"""
