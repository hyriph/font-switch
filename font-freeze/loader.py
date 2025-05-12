import os
from pathlib import Path

DIR = Path(__file__).parent
VARIANTS = [
"-Regular",
"-SemiBold",
"-Thin",
"-Black",
"-Bold",
"-ExtraBold",
"-ExtraLight",
"-Light",
"-Medium",
"Variable"
]
class Loader:

    version = "PretendardJP-1.3.9"
    prefix = "PretendardJP"
    ext = 'ttf'

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

    version = "PretendardAvenueJP-1.3.9"
    prefix = "PretendardAvenueJP"
    ext = 'ttf'

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
    
class AvenueSegoeLoader:

    version = "PretendardAvenueSegoeJP-1.3.9"
    prefix = "PretendardAvenueSegoeJP"
    ext = 'ttf'

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
    

class SegoeLoader:
    version = ""
    prefix = "SegoeUI-5.67"
    ext = 'otf'

    @staticmethod
    def load(weight: str):
        path = Path(DIR) / AvenueLoader.version / f"{AvenueLoader.prefix}{weight}.{AvenueLoader.ext}"
        return path.resolve().as_posix()
    