pairs = [
    ["Segoe UI Light (TrueType)", "segoeuil.ttf", "-ExtraLight", "l"],
    ["Segoe UI Semilight (TrueType)", "segoeuisl.ttf", "-Light", "sl"],
    ["Segoe UI (TrueType)", "segoeui.ttf", "-Regular", ""],
    ["Segoe UI Semibold (TrueType)", "seguisb.ttf", "-Medium", "sb"],
    ["Segoe UI Bold (TrueType)", "segoeuib.ttf", "-SemiBold", "b"],
    ["Segoe UI Black (TrueType)", "seguibl.ttf", "-Bold", "bl"],
    ["Segoe UI Variable (TrueType)", "SegUIVar.ttf", "Variable", "Var"],
]

new = "PrtdAvnuJPSegoeUI"

from fontTools.ttLib import TTFont


def do(pair):
    impt = "./PretendardAvenueJP-1.3.9"
    export = "./PretendardAvenueSegoeJP-1.3.9"
    s_impt = "./segoe"

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
