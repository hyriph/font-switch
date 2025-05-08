from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List

from fontTools.ttLib import TTCollection, TTFont
from fontTools.ttLib.tables._n_a_m_e import (
    NameRecord,
    _MAC_LANGUAGES,
    _WINDOWS_LANGUAGES,
    table__n_a_m_e,
)
from rich.console import Console
from rich.table import Table


def get_language_code(platformID: int, langID: int) -> str:
    if platformID == 1:
        return _MAC_LANGUAGES.get(langID, str(langID))
    if platformID == 3:
        return _WINDOWS_LANGUAGES.get(langID, str(langID))
    return str(langID)


def get_platform_name(platformID: int) -> str:
    return {
        0: "Unicode",
        1: "Macintosh",
        2: "ISO",
        3: "Windows",
        4: "Custom",
    }.get(platformID, "Unknown")

def get_font_name_table(path: str) :
    font: TTFont = TTFont(path)
    name_table: table__n_a_m_e = font["name"]
    names: List[NameRecord] = name_table.names

    records: List[Dict[str, str]] = []
    for record in names:
        records.append(
            {
                "nameID": str(record.nameID),
                "platformID": get_platform_name(record.platformID),
                "platEncID": str(record.platEncID),
                "langID": get_language_code(record.platformID, record.langID),
                "string": record.toUnicode(),
            }
        )

    return records


def display_name_table(path: str | Path) -> None:
    """Rich 테이블로 name 레코드를 출력한다."""
    records = get_font_name_table(str(path))

    table = Table(
        title=f"Name Table — {Path(path).name}",
        show_lines=True,
        expand=True,
    )

    # 열 헤더
    table.add_column("nameID", justify="right", style="cyan", no_wrap=True)
    table.add_column("platformID", style="magenta")
    table.add_column("platEncID", justify="right", style="green")
    table.add_column("langID", justify="right", style="yellow")
    table.add_column("string", style="white")

    # 데이터 삽입
    for rec in records:
        table.add_row(
            rec["nameID"],
            rec["platformID"],
            rec["platEncID"],
            rec["langID"],
            rec["string"],
        )

    Console().print(table)


if __name__ == "__main__":
    from loader import Loader, AvenueLoader
    display_name_table(Loader.variants()[1]['path'])
