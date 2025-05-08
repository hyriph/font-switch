from loader import Loader, AvenueLoader
from fontTools.ttLib.ttFont import TTFont
from fontTools.ttLib.tables._n_a_m_e import NameRecord, table__n_a_m_e
from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p, CmapSubtable
import fontTools.ttLib.tables.otTables as otTables
from fontTools.ttLib.tables.G_S_U_B_ import table_G_S_U_B_
from otTables import *

from typing import TYPE_CHECKING, cast, Optional


class Instantiate:
    def __init__(self, font: TTFont, /):
        # variations = args.get("variations")

        # options = args.get("options")
        family = font["name"].getBestFamilyName()
        version = font["name"].getDebugName(5)

        manufacturer = font["name"].getDebugName(8)
        description = f"Congelavi from {family} {version} by {manufacturer}."
        # keep_var = cast(bool, options.get("keepVar"))
        # if "fvar" in font and not keep_var:
        #     settings = ", ".join(f"{getAxisName(font, k)}={v}" for k, v in variations.items())
        #     description += f" Sets {settings}."
        #     instantiateVariableFont(font, variations, inplace=True, overlap=True)
        features = ['cv10', 'ss05', 'ss06', 'ss07', 'ss08']
        if len(features) > 0:
            features = ", ".join(features)
            description += f" Stylistic sets {features} activated by default."
        disables = []
        if len(disables) > 0:
            disables = ", ".join(disables)
            description += f" Stylistic sets {disables} deactivated by default."
        # if not hideRemovedFeature:
        #     description += " Use fallback mode."

        self.nameTable: table__n_a_m_e = font["name"]
        # support for pretendard
        splited = self.nameTable.getDebugName(1).split()
        if len(splited) > 1:
            weight = splited[1]
        else:
            weight = self.nameTable.getDebugName(2)
        # weight = self.nameTable.getDebugName(1).split()[1]
        print('weight', weight)

        # self.nameTable.names = []
        family = "Pretendard Avenue"
        # subfamily = options.get("subfamily")
        # typo_family = options.get("typo_family")
        # typo_subfamily = options.get("typo_subfamily")

        # if not typo_family:
        #     typo_family = family

        fullName = f'1.309;HYRI;PretendardAvenue-{weight}'
        # if not typo_subfamily or typo_subfamily == subfamily:
        #     typo_subfamily = subfamily
        #     fullName = f"{family} {subfamily}"
        # else:
        #     fullName = f"{family} {typo_subfamily} {subfamily}"

        # refer to https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids for a list of name codes
        self.setName("Pretendard Avenue", 1)
        self.setName(weight, 2)
        self.setName(fullName, 3)
        self.setName(f"Pretendard Avenue {weight}", 4)
        # self.setName("Version 1.000", 5)
        self.setName(f"PretendardAvenue-{weight}", 6)
        self.setName("FontCon 1.0.0", 8)
        self.setKoreanName("FontCon 1.0.0", 8)
        self.setName(description, 10)
        # 11 is vendor, 12 is designer
        # we change vendor to our website to distinguish from other frozen fonts
        # we don't change designer because no visual changes are made
        self.setName("https://hyri.xyz/", 11)
        # self.setName("https://mutsuntsai.github.io/fontfreeze", 11)
        self.setName("Pretendard Avenue", 16)
        # self.setName(typo_subfamily, 17)
        # self.setName(fullName, 18)

        # try:
        #     font["head"].macStyle = MAC_STYLE[subfamily]
        #     font["OS/2"].fsSelection = Instantiate.makeSelection(font["OS/2"].fsSelection, subfamily)
        # except Exception:
        #     pass

        # if not keep_var:
        #     Instantiate.dropVariationTables(font)
        # if options.get("fixContour"):
        #     Instantiate.setOverlapFlags(font)

    def getPostscriptName(familyName, subfamilyName, /):
        familyName = familyName.replace(" ", "")
        subfamilyName = subfamilyName.replace(" ", "")
        result = f"{familyName}-{subfamilyName}"
        return result[:63]  # The limit is 63 characters
    
    def setKoreanName(self, content: str, index: int, /):
        self.nameTable.setName(
            content,
            index,
            3,
            1,
            0x0412,
        )

    def setName(self, content: str, index: int, /):
        # Setting MAC platform seems to cause trouble in some fonts,
        # so we don't do that anymore.
        self.nameTable.setName(
            content,
            index,
            3,  # PLAT_WINDOWS,
            1,  # ENC_UNICODE_11
            1033,  # LANG_ENGLISH
        )

    def dropVariationTables(font, /):
        for tag in "STAT cvar fvar gvar".split():
            if tag in font.keys():
                del font[tag]

    def setOverlapFlags(font, /):
        glyf = font["glyf"]
        for glyph_name in glyf.keys():
            glyph = glyf[glyph_name]

            if glyph.isComposite():
                glyph.components[0].flags |= 0x0400  # OVERLAP_COMPOUND
            elif glyph.numberOfContours > 0:
                glyph.flags[0] |= 0x40  # OVERLAP_SIMPLE

    def makeSelection(bits, style, /):
        bits = bits ^ bits
        if style == "Regular":
            bits |= 0b1000000
        else:
            bits &= ~0b1000000
        if style == "Bold" or style == "Bold Italic":
            bits |= 0b100000
        else:
            bits &= ~0b100000
        if style == "Italic":
            bits |= 0b1
        else:
            bits &= ~0b1
        if not bits:
            bits = 0b1000000
        return bits



class Activator:

    font: TTFont
    features: list[str]
    target: str
    singleSub: bool
    
    cmapTables: list[CmapSubtable]
    # unicodeGlyphs

    featureRecords: list[FeatureRecord]
    lookup: list[Lookup]

    def __init__(self, font: TTFont) -> None:
        self.font = font
        self.features = ['cv10', 'ss05', 'ss06', 'ss07', 'ss08']
        self.target = ''
        self.singleSub = True

        if len(self.features) == 0 or "GSUB" not in self.font:
            return

        cmap_table: table__c_m_a_p = self.font['cmap']
        self.cmapTables: list[CmapSubtable] = cmap_table.tables
        self.unicodeGlyphs = {name for table in self.cmapTables for name in cast(dict[int, str], table.cmap).values()}

        gsub_table: table_G_S_U_B_ = self.font['GSUB']
        table: GSUB = gsub_table.table
        self.featureRecords = table.FeatureList.FeatureRecord
        self.lookup = table.LookupList.Lookup

        scriptRecords =  table.ScriptList.ScriptRecord
        for scriptRecord in scriptRecords:
            print("__init__::scriptRecord.ScriptTag", scriptRecord.ScriptTag)
            self.activateInScript(scriptRecord.Script)
    
    def activateInScript(self, script: Script, /):
        if script.DefaultLangSys is not None:
            self.activateInLangSys(script.DefaultLangSys)
        for langSysRecord in script.LangSysRecord:
            print('activateInScript::langSysRecord.LangSysTag', langSysRecord.LangSysTag)
            self.activateInLangSys(langSysRecord.LangSys)

    def activateInLangSys(self, langSys: LangSys, /):
        for index in langSys.FeatureIndex:
            featureRecord = self.featureRecords[index]
            if featureRecord.FeatureTag in self.features:
                if self.singleSub:
                    self.findSingleSubstitution(featureRecord)

    def findSingleSubstitution(self, featureRecord: FeatureRecord, /):
        for lookupIndex in featureRecord.Feature.LookupListIndex:
            lookup = self.lookup[lookupIndex]
            if lookup.LookupType == 1:  # Single substitution
                for sub in lookup.SubTable:
                    for key, value in sub.mapping.items():
                        if key in self.unicodeGlyphs:
                            self.singleSubstitution(key, value)

    def singleSubstitution(self, key: str, value: str, /):
        for table in self.cmapTables:
            cmap: dict[int, str] = table.cmap
            for index in cmap:
                if cmap[index] == key:
                    cmap[index] = value





# Legacy CJK fonts in Big5 encoding in particular might use mixed encoding. For more info, see
# https://docs.microsoft.com/en-us/typography/opentype/spec/name#windows-encoding-ids
def fixEncoding(name, /):
    temp = name.string.decode("utf_16_be")
    temp = bytes(temp, encoding="raw_unicode_escape")
    try:
        temp.decode("big5")
        name.string = temp
    except Exception:
        pass  # We've tried our best


def load_font(filename: str, /):
    font: TTFont = TTFont(
        file=filename,
        recalcBBoxes=False,
        fontNumber=0,  # in case it's a font collection
    )

    name_table: table__n_a_m_e = font["name"]
    name_records: list[NameRecord] = name_table.names

    for name in name_records:
        if name.platformID == 3 and name.platEncID == 4: # Big5
            try:
                name.toStr()
            except Exception:
                fixEncoding(name)


    return font


def main():
    avenue_variants = AvenueLoader.variants()
    def find_variant(v: str):
        for variant in avenue_variants:
            if variant["variant"] == v:
                return variant
        return None

    for variant in Loader.variants():
        print(variant["variant"])
        font = load_font(variant["path"])
        Instantiate(font)
        Activator(font)
        font.save(find_variant(variant["variant"])["path"])

    # print(Loader.variants()[1]['path'])
    # regular_path = Loader.variants()[1]['path']
    # font = load_font(regular_path)
    # Instantiate(font)
    # Activator(font)
    # font.save(AvenueLoader.regular())

if __name__ == "__main__":
    main()
