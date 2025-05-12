from fontTools.ttLib import TTFont
from PIL import Image            # Pillow
import io
import tempfile
from pathlib import Path
from typing import Final
import freetype                  # freetype-py

def export_glyph_A_to_png(
    font: TTFont,
    output_path: str | Path,
    *,
    pixel_size: int = 256,       # 1 em 기준 높이 (px) – 원하면 조정하세요
    margin: int = 32             # 이미지 테두리 여백 (px)
) -> Path:
    """
    주어진 TTFont 객체에서 'A' 글리프를 추출해 PNG로 저장합니다.

    Parameters
    ----------
    font: TTFont
        fontTools 가 제공하는 TTFont 객체.
    output_path: str | pathlib.Path
        저장할 PNG 경로.
    pixel_size: int, optional
        글리프 em 높이를 몇 px 로 랜더링할지 – 기본 256 px.
    margin: int, optional
        이미지 테두리 여백 – 기본 32 px.

    Returns
    -------
    pathlib.Path
        실제로 저장된 PNG 경로.
    """

    # 1️⃣ TTFont → 임시 .ttf 파일 (freetype 은 파일/버퍼 단위로만 읽어요)
    with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as tmp:
        font.save(tmp.name)
        font_path: Final[str] = tmp.name

    # 2️⃣ FreeType 로드 & 'A' 글리프 렌더링
    face = freetype.Face(font_path)
    face.set_char_size(pixel_size * 64)            # 26.6 fixed-point
    face.load_char("A", freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
    bitmap = face.glyph.bitmap

    # 3️⃣ Pillow 이미지로 변환
    # buffer(list) → bytes 로 변환
    glyph_img = Image.frombytes(
        mode="L",
        size=(bitmap.width, bitmap.rows),
        data=bytes(bitmap.buffer)
    )

    # 4️⃣ 캔버스(배경) 만들고 가운데 배치
    canvas_size = (bitmap.width + margin * 2, bitmap.rows + margin * 2)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))   # 투명 배경
    canvas.paste(
        glyph_img.convert("RGBA"),
        box=(margin, margin),
        mask=glyph_img                  # 알파 채널로 사용
    )

    # 5️⃣ 저장
    output_path = Path(output_path).with_suffix(".png")
    canvas.save(output_path)

    return output_path

def load_font(path):
    return TTFont(path)

if __name__ == "__main__":
    inter = load_font('./Inter-Regular.otf')
    prtd = load_font('./PretendardAvenueJP-Regular.ttf')
    export_glyph_A_to_png(inter, 'output/inter_A.png')
    export_glyph_A_to_png(prtd, 'output/prtd_A.png')