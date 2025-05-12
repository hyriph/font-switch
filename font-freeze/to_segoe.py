from loader import AvenueLoader, AvenueSegoeLoader

from .main import load_font

def main():
    avenue_variants = AvenueLoader.variants()
    avenue_segoe_variants = AvenueSegoeLoader.variants()
    segoe_variants = Seg

    def find_variant(v: str):
        for variant in avenue_segoe_variants:
            if variant["variant"] == v:
                return variant
        return None
    
    for variant in avenue_variants:
        input_v = variant["variant"]
        print(input_v)

        input_path = variant["path"]
        output_path = find_variant(input_v)['path']

        font = load_font()
