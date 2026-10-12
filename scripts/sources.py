"""Per-calculator "Sources & method" lines for E-E-A-T.

Every URL here was checked live (HTTP 200) before being added. Sources are grouped
by the calculator they underpin, so each page cites the specific body that sets the
rate it uses, rather than a generic "we did our research" claim.
"""
from __future__ import annotations

SOURCES: dict[str, list[tuple[str, str]]] = {
    "mulch": [
        ("Penn State Extension, Mulching Landscape Trees",
         "https://extension.psu.edu/mulching-landscape-trees"),
    ],
    "topsoil": [
        ("University of Maryland Extension, Soil to Fill Raised Beds",
         "https://extension.umd.edu/resource/soil-fill-raised-beds"),
    ],
    "soil": [
        ("University of Maryland Extension, Soil to Fill Raised Beds",
         "https://extension.umd.edu/resource/soil-fill-raised-beds"),
    ],
    "gravel": [
        ("Oregon State University Extension, 10-Step Guide to Installing Pavers",
         "https://extension.oregonstate.edu/sites/extd8/files/documents/1/howtoinstallpavers.pdf"),
    ],
    "concrete": [
        ("QUIKRETE concrete bag yield data sheet",
         "https://www.quikrete.com/pdfs/data_sheet-concrete%20mix%201100.pdf"),
        ("QUIKRETE concrete calculator",
         "https://www.quikrete.com/calculator/main.asp"),
    ],
    "paint": [
        ("PaintCare, Buy the Right Amount of Paint",
         "https://www.paintcare.org/buy-right"),
    ],
    "tile": [
        ("Custom Building Products, Installing Large Format Tiles (TCNA methods)",
         "https://www.custombuildingproducts.com/media/736036/large_format_tile_wp103.pdf"),
    ],
    "grass_seed": [
        ("University of Minnesota Extension, Buying turfgrass seed for Minnesota lawns",
         "https://extension.umn.edu/garden-and-home/yard-and-garden/lawns-and-landscapes-in-minnesota/buying-turfgrass-seed-for-minnesota-lawns"),
    ],
    "fertilizer": [
        ("Illinois Extension, Fertilizing Your Lawn",
         "https://extension.illinois.edu/lawns/fertilizing-your-lawn"),
    ],
}


def for_key(key: str) -> list[tuple[str, str]]:
    return SOURCES.get(key or "", [])
