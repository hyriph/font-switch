from typing import List, Dict
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance
from fontTools.ttLib.tables._n_a_m_e import NameRecord


def print_all_instance_axes(font: TTFont) -> None:
    """
    TTFont 객체의 모든 Named Instance(예: ‘Light Text’)에 대해
    정의된 모든 Axis 축(axisTag)과 그 값을 출력합니다.

    :param font: TTFont 객체(가변 폰트)
    """
    fvar = font["fvar"]
    name_table = font["name"]

    axes: List[Axis] = fvar.axes

    for instance in fvar.instances:  # type: NamedInstance
        # 인스턴스 이름 얻기 (영어: platformID=3, platEncID=1, langID=0x409)
        name_rec: NameRecord = name_table.getName(
            nameID=instance.subfamilyNameID,
            platformID=3,
            platEncID=1,
            langID=0x409
        )  # type: ignore

        instance_name: str = (
            name_rec.toUnicode()
            if name_rec is not None
            else f"NameID {instance.subfamilyNameID}"
        )

        print(f"[{instance_name}]")
        coords: Dict[str, float] = instance.coordinates

        for axis in axes:
            # axis.axisTag 으로 태그를 참조합니다
            tag: str = axis.axisTag
            # 값이 없으면 axis.defaultValue 사용
            value: float = coords.get(tag, axis.defaultValue)
            print(f" – {tag}: {value}")
        print()  # 인스턴스별 빈 줄


if __name__ == "__main__":
    font_path = ".\\segoe\\SEGUIVAR.TTF"
    tt: TTFont = TTFont(font_path)
    print_all_instance_axes(tt)
