from typing import Any, Dict, List
from fontTools.ttLib.ttFont import TTFont
from fontTools.ttLib.tables.otTables import Script, LangSys
from fontTools.ttLib.tables.G_S_U_B_ import table_G_S_U_B_
from fontTools.ttLib.tables.otTables import FeatureRecord
from otTables import *

def get_features_by_langsys(font: TTFont) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """
    폰트의 GSUB 테이블을 순회하며,
    각 Script–LangSys 조합별로
      - RequiredFeatureIndex로 지정된 필수 피처
      - FeatureIndex로 지정된 지원 피처
    를 함께 반환합니다.

    반환 형식:
      {
        "ScriptTag1": {
          "default":   {"required": [...], "optional": [...]},
          "JPN ":      {"required": [...], "optional": [...]},
          ...
        },
        "ScriptTag2": { ... },
        ...
      }
    """
    result: Dict[str, Dict[str, Dict[str, List[str]]]] = {}

    # GSUB 테이블을 가져옵니다
    gsub_table: table_G_S_U_B_ = font["GSUB"]  # type: ignore[index]
    gsub: GSUB = gsub_table.table

    feature_records: List[FeatureRecord] = gsub.FeatureList.FeatureRecord
    script_records:   Any               = gsub.ScriptList.ScriptRecord

    for script_record in script_records:
        script_tag: str = script_record.ScriptTag
        script: Script  = script_record.Script

        result.setdefault(script_tag, {})

        # default LangSys
        if script.DefaultLangSys is not None:
            req = _collect_required(script.DefaultLangSys, feature_records)
            opt = _collect_optional(script.DefaultLangSys, feature_records)
            result[script_tag]["default"] = {"required": req, "optional": opt}

        # 나머지 LangSysRecord
        for lang_sys_record in script.LangSysRecord:
            lang_tag: str = lang_sys_record.LangSysTag
            lang_sys: LangSys = lang_sys_record.LangSys

            req = _collect_required(lang_sys, feature_records)
            opt = _collect_optional(lang_sys, feature_records)
            result[script_tag][lang_tag] = {"required": req, "optional": opt}

    return result

def _collect_required(langsys: LangSys, feature_records: List[FeatureRecord]) -> List[str]:
    """
    LangSys.ReqFeatureIndex가 가리키는 단일 필수 피처를 반환.
    유효 인덱스가 아니면 빈 리스트 반환.
    """
    idx: int = getattr(langsys, "ReqFeatureIndex", 0xFFFF)
    if idx != 0xFFFF:
        return [feature_records[idx].FeatureTag]
    return []

def _collect_optional(langsys: LangSys, feature_records: List[FeatureRecord]) -> List[str]:
    """
    LangSys.FeatureIndex를 통해
    지원(사용 가능)되는 FeatureTag 목록을 반환.
    """
    return [feature_records[i].FeatureTag for i in langsys.FeatureIndex]

# 사용 예시
if __name__ == "__main__":
    from loader import Loader
    font_path: str = Loader.regular()
    font: TTFont = TTFont(font_path)
    features_map = get_features_by_langsys(font)

    for script, langs in features_map.items():
        print(f"== Script: {script} ==")
        for lang, grp in langs.items():
            req_list = grp["required"]
            opt_list = grp["optional"]
            print(f"  [{lang}] required → {', '.join(req_list) or '(none)'}")
            print(f"  [{lang}] optional → {', '.join(opt_list)}")
