from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._n_a_m_e import NameRecord
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance
from typing import List, Tuple, Dict, Optional


def get_all_axes_info_with_breakpoints(font: TTFont) -> Dict[str, Dict]:
    """
    가변 폰트의 모든 axis에 대해:
    - axis 메타 정보(min, max, default)
    - Named Instance(브레이크포인트) 목록
    을 포함한 구조로 반환합니다.

    :param font: TTFont 객체(가변 폰트)
    :return: {
        "wght": {
            "min": 100.0,
            "max": 900.0,
            "default": 400.0,
            "breakpoints": [("Light", 300.0), ("Bold", 700.0), ...]
        },
        ...
    }
    """
    fvar = font["fvar"]
    name_table = font["name"]
    result: Dict[str, Dict] = {}

    # 축 정보 저장
    for axis in fvar.axes:  # type: Axis
        result[axis.axisTag] = {
            "min": float(axis.minValue),
            "max": float(axis.maxValue),
            "default": float(axis.defaultValue),
            "breakpoints": []
        }

    # Named Instance 정보 저장
    for instance in fvar.instances:  # type: NamedInstance
        coords = instance.coordinates
        name_id = instance.subfamilyNameID
        name_record: Optional[NameRecord] = name_table.getName(
            nameID=name_id,
            platformID=3,
            platEncID=1,
            langID=0x409
        )
        inst_name = name_record.toUnicode() if name_record else f"NameID {name_id}"

        for axis_tag, value in coords.items():
            if axis_tag in result:
                result[axis_tag]["breakpoints"].append((inst_name, float(value)))

    return result


def print_all_axes_info(font: TTFont) -> None:
    """
    get_all_axes_info_with_breakpoints()의 결과를 예쁘게 출력합니다.
    """
    all_axes = get_all_axes_info_with_breakpoints(font)

    for axis_tag, info in all_axes.items():
        print(f"[Axis: {axis_tag}]")
        print(f"  · Min     : {info['min']}")
        print(f"  · Max     : {info['max']}")
        print(f"  · Default : {info['default']}")
        print(f"  · Breakpoints:")
        for name, val in info["breakpoints"]:
            print(f"    – {name} – {val}")
        print()


if __name__ == "__main__":
    # font_path = ".\\segoe\\SEGUIVAR.TTF"
    font_path = ".\\PretendardAvenueJP-1.3.9\\PretendardAvenueJPVariable.ttf"
    tt = TTFont(font_path)
    print_all_axes_info(tt)


