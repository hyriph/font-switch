import os
from pathlib import Path

DIR = Path(__file__).parent
VARIANTS = [
"Regular",
"SemiBold",
"Thin",
"Black",
"Bold",
"ExtraBold",
"ExtraLight",
"Light",
"Medium",
]
class Loader:

    version = "Pretendard-1.3.9"
    prefix = "Pretendard-"
    ext = 'otf'

    @staticmethod
    def load(weight: str):
        path = Path(DIR) / Loader.version / f"{Loader.prefix}{weight}.{Loader.ext}"
        return path.resolve().as_posix()


    @staticmethod
    def regular():
        return Loader.load('Regular')
    
    @staticmethod
    def variants():
        return [
            {
                "variant": variant,
                "path": Loader.load(variant)
            } for variant in VARIANTS
        ]

class AvenueLoader:

    version = "PretendardAvenue-1.3.9"
    prefix = "PretendardAvenue-"
    ext = 'otf'

    @staticmethod
    def load(weight: str):
        path = Path(DIR) / AvenueLoader.version / f"{AvenueLoader.prefix}{weight}.{AvenueLoader.ext}"
        return path.resolve().as_posix()
    
    @staticmethod
    def regular():
        return AvenueLoader.load('Regular')
    
    @staticmethod
    def variants():
        return [
            {
                "variant": variant,
                "path": AvenueLoader.load(variant)
            } for variant in VARIANTS
        ]