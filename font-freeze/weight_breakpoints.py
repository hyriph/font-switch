from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._n_a_m_e import NameRecord
from typing import List, Tuple, Optional


def get_weight_breakpoints(font: TTFont) -> List[Tuple[str, int]]:
    """
    가변 폰트의 weight(axis='wght')에 정의된 Named Instance들의
    이름과 굵기 값을 리스트로 반환합니다.

    :param font: TTFont 객체(가변 폰트)
    :return: [(인스턴스 이름, 굵기 값), ...]
    """
    # fvar 테이블에서 NamedInstance 목록 가져오기
    fvar = font["fvar"]
    name_table = font["name"]
    breakpoints: List[Tuple[str, int]] = []

    for instance in fvar.instances:  # type: NamedInstance
        coords = instance.coordinates
        # 'wght' 축에 값이 정의된 NamedInstance만 처리
        if "wght" in coords:
            weight_value: int = coords["wght"]
            name_id: int = instance.subfamilyNameID

            # name 테이블에서 영어(플랫폼ID=3, 인코딩ID=1, 언어ID=0x409)로 가져오기
            name_record: Optional[NameRecord] = name_table.getName(
                nameID=name_id,
                platformID=3,
                platEncID=1,
                langID=0x409
            )

            if name_record:
                name_str: str = name_record.toUnicode()
            else:
                name_str = f"NameID {name_id}"

            breakpoints.append((name_str, weight_value))

    return breakpoints


def print_weight_breakpoints(font: TTFont) -> None:
    """
    get_weight_breakpoints()의 결과를 예쁘게 출력합니다.
    """
    for name, value in get_weight_breakpoints(font):
        print(f"{name} – {value}")


if __name__ == "__main__":
    # 테스트용: 파일 경로를 적절히 바꿔 주세요
    # font_path: str = ".\\PretendardAvenueJP-1.3.9\\PretendardAvenueJPVariable.ttf"
    font_path = ".\\segoe\\SEGUIVAR.TTF"
    tt: TTFont = TTFont(font_path)
    print_weight_breakpoints(tt)
