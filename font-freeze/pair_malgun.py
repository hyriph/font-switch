pairs = [
    ["Malgun Gothic (TrueType)", "malgunsl.ttf", "-Light", "SL"],
    ["Malgun Gothic Bold (TrueType)", "malgun.ttf", "-Regular", ""],
    ["Malgun Gothic SemiLight (TrueType)", "malgunbd.ttf", "-SemiBold", "BD"],
]

new = "PrtdAvnuJPMalgun"

from fontTools.ttLib import TTFont


def do(pair):
    impt = "./PretendardAvenueJP-1.3.9"
    export = "./PretendardAvenueMalgunJP-1.3.9"
    s_impt = "./malgun"

    name = pair[0]
    segoe_path = pair[1]
    prtd_wght = pair[2]
    prtd_style = pair[3]

    segoe = TTFont(f"./{s_impt}/{segoe_path}")
    segoe_name = segoe["name"]
    print("segoe: ", segoe_name.getDebugName(1))

    prtd = TTFont(
        f"{impt}/PretendardAvenueJP{prtd_wght}.ttf",
        recalcBBoxes=False,
        recalcTimestamp=False,
    )
    prtd_name = prtd["name"]
    print("prtd_old: ", prtd_name.getDebugName(1))
    prtd["name"] = segoe_name

    print("prtd_new: ", prtd["name"].getDebugName(1))
    new_prtd = f"./{export}/{new}{prtd_style}.ttf"
    prtd.save(new_prtd)

    prtdsegoe = TTFont(new_prtd)
    print("prtdsegoe: ", prtdsegoe["name"].getDebugName(1))


for pair in pairs:
    do(pair)
