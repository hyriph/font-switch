from fontTools.ttLib.tables.otConverters import (Version, Table as Offset, LTable as LOffset, Tag)
from typing import Optional

class LookupOrder:
    ...

class ScriptList:
    ScriptCount: int
    ScriptRecord: list["ScriptRecord"]

class ScriptRecord:
    ScriptTag: Tag
    Script: "Script"

class Script:
    DefaultLangSys: Optional["LangSys"]
    LangSysCount: int
    LangSysRecord: list["LangSysRecord"]

class LangSysRecord:
    LangSysTag: Tag
    LangSys: "LangSys"

class LangSys:
    LookupOrder: "LookupOrder"
    ReqFeatureIndex: int
    FeatureCount: int
    FeatureIndex: list[int]

class FeatureList:
    FeatureCount: int
    FeatureRecord: list["FeatureRecord"]

class FeatureRecord:
    FeatureTag: Tag
    Feature: "Feature"

class Feature:
    FeatureParams: "FeatureParams"
    LookupCount: int
    LookupListIndex: list[int]

class FeatureParams:
    ...

# class FeatureParamsSize:
#     DesignSize: "DeciPoints"
#     SubfamilyID: int
#     RangeStart: "DeciPoints"
#     RangeEnd: "DeciPoints"

# 중략

class LookupList:
    LookupCount: int
    Lookup: list["Lookup"]

class Lookup:
    LookupType: int
    SubTableCount: int
    SubTable: list["Offset"]
    MarkFilteringSet: int

class GSUB:
    Version: Version
    ScriptList: "ScriptList"
    FeatureList: "FeatureList"
    LookupList: "LookupList"
    FeatureVariations: LOffset
    


