"""Renders Samples/Images/Metering-CoolingTowerWater-Example1.png.

Cooling tower makeup and blowdown water metering: the Cooling Tower Group is
servedBy the makeup Water Meter, the blowdown Water Meter is servedBy the group,
each meter's Water Volume Sensor isCapabilityOf the meter, and the makeup meter
is a subMeterOf the domestic Water Meter which serves the Building.

    python Samples/Images/Source/Metering-CoolingTowerWater-Example1.py

Requires Pillow. Uses Segoe UI when available, otherwise DejaVu Sans.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor; drawn at 2x, downscaled at the end
W, H = 1980, 900

SPACE = (123, 0, 255)
ASSET = (16, 210, 150)
CAPABILITY = (58, 68, 160)
COLLECTION = (27, 31, 79)
LINE = (160, 160, 160)
TEXT = (30, 30, 30)
LEGEND = [
    ("Space", SPACE),
    ("Asset", ASSET),
    ("Capability", CAPABILITY),
    ("Agent", (200, 170, 140)),
    ("Document", (255, 45, 106)),
    ("Event", (140, 0, 48)),
    ("Collection", COLLECTION),
    ("Building\nComponent", (10, 107, 76)),
]

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "Metering-CoolingTowerWater-Example1.png")


def font(size, bold=False):
    names = ["segoeuib.ttf", "DejaVuSans-Bold.ttf"] if bold else ["segoeui.ttf", "DejaVuSans.ttf"]
    dirs = ["C:/Windows/Fonts", os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts"),
            "/usr/share/fonts/truetype/dejavu", ""]
    for name in names:
        for d in dirs:
            try:
                return ImageFont.truetype(os.path.join(d, name), size * S)
            except OSError:
                pass
    return ImageFont.load_default()


BOX_FONT = font(19)
LABEL_FONT = font(15)
CALLOUT_FONT = font(15, bold=True)
LEGEND_FONT = font(22)
LEGEND_TITLE = font(24, bold=True)

img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)


def s(*v):
    return [x * S for x in v]


def box(cx, cy, text, color, w=200, h=96):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle(s(x0, y0, x1, y1), radius=18 * S, fill="white", outline=color, width=6 * S)
    d.multiline_text(s(cx, cy), text, font=BOX_FONT, fill=TEXT, anchor="mm", align="center", spacing=3 * S)
    return dict(l=x0, r=x1, t=y0, b=y1, cx=cx, cy=cy)


def line(*pts):
    d.line(s(*pts), fill=LINE, width=2 * S, joint="curve")


def arrow(x0, y0, x1, y1):
    line(x0, y0, x1, y1)
    a = math.atan2(y1 - y0, x1 - x0)
    L, w = 13, 6
    p1 = (x1 - L * math.cos(a) + w * math.sin(a), y1 - L * math.sin(a) - w * math.cos(a))
    p2 = (x1 - L * math.cos(a) - w * math.sin(a), y1 - L * math.sin(a) + w * math.cos(a))
    d.polygon(s(x1, y1, *p1, *p2), fill=LINE)


def label(x, y, text, anchor="mm"):
    d.multiline_text(s(x, y), text, font=LABEL_FONT, fill=TEXT, anchor=anchor, align="center", spacing=4 * S)


def callout(x, y, n):
    r = 14
    d.ellipse(s(x - r, y - r, x + r, y + r), fill="black")
    d.text(s(x, y), str(n), font=CALLOUT_FONT, fill="white", anchor="mm")


def capabilities_of(target, caps, num=None):
    """caps are boxes to the right of target; bracket and arrow into target."""
    bx = caps[0]["l"] - 32
    for c in caps:
        line(c["l"], c["cy"], bx, c["cy"])
    line(bx, caps[0]["cy"], bx, caps[-1]["cy"])
    arrow(bx, target["cy"], target["r"] + 2, target["cy"])
    label((bx + target["r"]) / 2, target["cy"] - 14, "isCapabilityOf")
    if num:
        callout(target["r"] + 32, target["t"] + 8, num)


# --- towers and their group ---------------------------------------------------
ct1 = box(200, 110, "Cooling Tower 1", ASSET)
ct2 = box(200, 290, "Cooling Tower 2", ASSET)
group = box(640, 200, "Cooling Tower\nGroup", COLLECTION)
arrow(ct1["r"], ct1["cy"], group["l"] - 2, group["cy"] - 20)
arrow(ct2["r"], ct2["cy"], group["l"] - 2, group["cy"] + 20)
label((ct1["r"] + group["l"]) / 2, group["cy"], "includedIn")
callout(group["cx"], group["t"] - 26, 3)

# --- makeup meter: group servedBy meter -----------------------------------------
makeup = box(1080, 200, "Makeup\nWater Meter", ASSET)
arrow(group["r"], group["cy"], makeup["l"] - 2, makeup["cy"])
label((group["r"] + makeup["l"]) / 2, group["cy"] - 14, "servedBy")
callout((group["r"] + makeup["l"]) / 2, group["cy"] + 26, 2)
capabilities_of(makeup, [box(1480, 200, "Water Volume\nSensor", CAPABILITY)], num=1)

# --- blowdown meter: meter servedBy group ---------------------------------------
blowdown = box(640, 500, "Blowdown\nWater Meter", ASSET)
arrow(blowdown["cx"], blowdown["t"], group["cx"], group["b"] + 2)
label(group["cx"] - 16, (blowdown["t"] + group["b"]) / 2, "servedBy", anchor="rm")
callout(group["cx"] + 28, (blowdown["t"] + group["b"]) / 2, 4)
bd_sensor = box(200, 500, "Water Volume\nSensor", CAPABILITY)
arrow(bd_sensor["r"], bd_sensor["cy"], blowdown["l"] - 2, blowdown["cy"])
label((bd_sensor["r"] + blowdown["l"]) / 2, blowdown["cy"] - 14, "isCapabilityOf")

# --- makeup meter is a sub-meter of the domestic service meter -------------------
domestic = box(1080, 500, "Domestic\nWater Meter", ASSET)
arrow(makeup["cx"], makeup["b"], domestic["cx"], domestic["t"] - 2)
label(makeup["cx"] - 16, (makeup["b"] + domestic["t"]) / 2, "subMeterOf", anchor="rm")
callout(makeup["cx"] + 28, (makeup["b"] + domestic["t"]) / 2, 5)
building = box(1080, 780, "Building", SPACE)
arrow(building["cx"], building["t"], domestic["cx"], domestic["b"] + 2)
label(domestic["cx"] - 16, (building["t"] + domestic["b"]) / 2, "servedBy", anchor="rm")

# --- legend -------------------------------------------------------------------
lx0, ly0, lx1, ly1 = 1660, 40, 1960, 520
d.rounded_rectangle(s(lx0, ly0, lx1, ly1), radius=16 * S, outline=(215, 215, 215), width=2 * S)
tw = d.textlength("Model", font=LEGEND_TITLE) / S
tx = (lx0 + lx1) / 2
d.rectangle(s(tx - tw / 2 - 22, ly0 - 4, tx + tw / 2 + 22, ly0 + 4), fill="white")
d.text(s(tx, ly0), "Model", font=LEGEND_TITLE, fill="black", anchor="mm")
y = ly0 + 58
for name, color in LEGEND:
    d.ellipse(s(lx0 + 50 - 13, y - 13, lx0 + 50 + 13, y + 13), fill=color)
    d.multiline_text(s(lx0 + 76, y), name, font=LEGEND_FONT, fill="black", anchor="lm", spacing=10 * S) \
        if "\n" not in name else d.multiline_text(s(lx0 + 76, y - 15), name, font=LEGEND_FONT, fill="black",
                                                   anchor="la", spacing=10 * S)
    y += 52

out = img.resize((W, H), Image.LANCZOS)
out.save(os.path.abspath(OUT), optimize=True)
print("wrote", os.path.abspath(OUT))
