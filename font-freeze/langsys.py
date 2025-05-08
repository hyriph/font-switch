from typing import Any, Dict, List
from fontTools.ttLib.ttFont import TTFont
from fontTools.ttLib.tables.otTables import Script, LangSys
from fontTools.ttLib.tables.G_S_U_B_ import table_G_S_U_B_
from fontTools.ttLib.tables.otTables import FeatureRecord
from otTables import *

def get_active_features_by_langsys(font: TTFont) -> Dict[str, Dict[str, List[str]]]:
    """
    폰트의 GSUB 테이블을 순회하며,
    각 Script–LangSys 조합별로 활성화된 FeatureTag 목록을 반환합니다.

    반환 형식:
      {
        "ScriptTag1": {
          "default": ["liga", "rlig", ...],
          "JPN ": ["vert", ...],
          ...
        },
        "ScriptTag2": { ... },
        ...
      }
    """
    result: Dict[str, Dict[str, List[str]]] = {}

    # GSUB 테이블을 가져옵니다
    gsub_table: table_G_S_U_B_ = font["GSUB"]  # type: ignore[index]
    gsub: GSUB = gsub_table.table

    # FeatureList와 ScriptList는 동일 레벨에 위치
    feature_records = gsub.FeatureList.FeatureRecord
    script_records   = gsub.ScriptList.ScriptRecord

    for script_record in script_records:
        script_tag = script_record.ScriptTag  # 4-byte ScriptTag
        script  = script_record.Script

        # 결과 딕셔너리 초기화
        result.setdefault(script_tag, {})

        # DefaultLangSys 처리
        if script.DefaultLangSys is not None:
            result[script_tag]["default"] = _collect_features(script.DefaultLangSys, feature_records)

        # 나머지 LangSysRecord 처리
        for lang_sys_record in script.LangSysRecord:
            lang_tag = lang_sys_record.LangSysTag  # 4-byte LangSysTag
            lang_sys = lang_sys_record.LangSys

            result[script_tag][lang_tag] = _collect_features(lang_sys, feature_records)

    return result

def _collect_features(langsys: LangSys, feature_records: list[FeatureRecord]) -> list[str]:
    """
    주어진 LangSys에서 활성화된 FeatureRecord 인덱스를 읽어
    FeatureTag 문자열 리스트를 반환합니다.
    """
    tags: list[str] = []
    for idx in langsys.FeatureIndex:
        record = feature_records[idx]
        tags.append(record.FeatureTag)
    return tags

# 사용 예시
if __name__ == "__main__":
    from loader import Loader
    font_path = Loader.regular()
    font = TTFont(font_path)
    active = get_active_features_by_langsys(font)
    for script, langs in active.items():
        print(f"== Script: {script} ==")
        for lang, feats in langs.items():
            print(f"  [{lang}] → {', '.join(feats)}")
