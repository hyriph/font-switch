import winreg
from winreg import HKEYType
from typing import Tuple, Optional

new = "PrtdAvnuJPSegoeUI"

pairs = [
    ["Segoe UI Light (TrueType)", "l"],
    ["Segoe UI Semilight (TrueType)", "sl"],
    ["Segoe UI (TrueType)", ""],
    ["Segoe UI Semibold (TrueType)", "sb"],
    ["Segoe UI Bold (TrueType)", "b"],
    ["Segoe UI Black (TrueType)", "bl"],
    ["Segoe UI Variable (TrueType)", "Var"],
]

REG_KEY_PATH: str = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"


def open_fonts_key():
    """
    Fonts 레지스트리 키를 읽기 + 쓰기(값 설정) 권한으로 엽니다.
    """
    return winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        REG_KEY_PATH,
        0,
        winreg.KEY_READ | winreg.KEY_SET_VALUE,
    )


def read_string_value(hKey: HKEYType, value_name: str) -> Optional[str]:
    """
    지정한 값 이름이 REG_SZ라면 문자열을 돌려주고,
    없거나 다른 타입이면 None을 반환해요.
    """
    try:
        raw_data, reg_type = winreg.QueryValueEx(hKey, value_name)
    except FileNotFoundError:
        return None

    if reg_type != winreg.REG_SZ:
        return None

    # Python 3.11 기준, 문자열은 str, 이진은 bytes
    if isinstance(raw_data, bytes):
        return raw_data.decode("utf-16le", errors="ignore")

    return str(raw_data)


def set_string_value(hKey: HKEYType, value_name: str, data: str) -> None:
    """
    REG_SZ 값 쓰기. Python은 널 문자와 길이를 자동 처리해 줘서
    C++처럼 직접 길이를 계산할 필요가 없어요.
    """
    winreg.SetValueEx(hKey, value_name, 0, winreg.REG_SZ, data)


def main() -> None:
    hKey = open_fonts_key()

    for [key, value] in pairs:
        ext_value = 'C:\\fonts\\' + new + value +'.ttf'
        # print(ext_value)
        set_string_value(hKey, key, ext_value)

    winreg.CloseKey(hKey)


if __name__ == "__main__":
    main()
