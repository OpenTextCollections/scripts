import lingtypology
from datetime import datetime

m = lingtypology.LingMap(
    (
        "mfum1238",
        "saek1240",
        "phal1254",
        "gawa1246",
        "alyk1238",
        "taly1247",
        "tsak1249",
        "wara1294",
        "bine1240",
        "wara1303",
        "iqui1243",
        "noma1263",
        "orej1242",
        "boro1282",
        "kawe1237",
        "cofa1242",
        "ruul1235",
        "skol1241",
        "komi1277",
        "cent2142",
        "daka1243",
        "valm1241",
        "hinu1240",
        "sanz1248",
        "chir1284",
        "taba1259",
        "sout2940",
        "xooo1239",
        "kara1516",
        "toli1244",
        "ende1246"
    ),
    glottocode=True,
)
m.tiles = "openstreetmap"
m.create_map()
today = datetime.now().strftime("%Y-%m-%d")
fname = f"otclgs{today}.png"
print(f"saving to {fname}")
m.save_static(fname=fname)
