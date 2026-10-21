"""Renders Samples/Images/AssetComponents-Example3.png.

Heat exchanger sides and their control valves: the side isFedBy the valve.

    python Samples/Images/Source/AssetComponents-Example3.py

Requires Pillow. Uses Segoe UI when available, otherwise DejaVu Sans.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor; drawn at 2x, downscaled at the end
W, H = 2460, 800

ASSET = (16, 210, 150)
CAPABILITY = (58, 68, 160)
COLLECTION = (27, 31, 79)
LINE = (160, 160, 160)
TEXT = (30, 30, 30)
LEGEND = [
    ("Space", (123, 0, 255)),
    ("Asset", ASSET),
    ("Capability", CAPABILITY),
    ("Agent", (200, 170, 140)),
    ("Document", (255, 45, 106)),
    ("Event", (140, 0, 48)),
    ("Collection", COLLECTION),
    ("Building\nComponent", (10, 107, 76)),
]

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "AssetComponents-Example3.png")


def font(size, bold=False):
    names = ["segoeuib.ttf", "DejaVuSans-Bold.ttf"] if bold else ["segoeui.ttf", "DejaVuSans.ttf"]
    for name in names:
        for d in ["C:/Windows/Fonts", "/usr/share/fonts/truetype/dejavu", ""]:
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
    d.text(s(x, y), text, font=LABEL_FONT, fill=TEXT, anchor=anchor)


def callout(x, y, n):
    r = 14
    d.ellipse(s(x - r, y - r, x + r, y + r), fill="black")
    d.text(s(x, y), str(n), font=CALLOUT_FONT, fill="white", anchor="mm")


def part_of(parent, children, bus_y, num=None):
    for c in children:
        line(c["cx"], c["t"], c["cx"], bus_y)
    line(children[0]["cx"], bus_y, children[-1]["cx"], bus_y)
    arrow(parent["cx"], bus_y, parent["cx"], parent["b"] + 2)
    if num:
        callout(parent["cx"] - 48, bus_y - 22, num)
    label(parent["cx"] + 10, bus_y - 20, "isPartOf", anchor="lm")


def capabilities_of(target, caps, side, num=None):
    """caps are boxes on `side` ('left'/'right') of target; bracket and arrow into target."""
    if side == "left":
        bx = caps[0]["r"] + 32
        for c in caps:
            line(c["r"], c["cy"], bx, c["cy"])
        line(bx, caps[0]["cy"], bx, caps[-1]["cy"])
        arrow(bx, target["cy"], target["l"] - 2, target["cy"])
        label((bx + target["l"]) / 2, target["cy"] - 14, "isCapabilityOf")
        if num:
            callout(target["l"] - 32, target["t"] + 8, num)
    else:
        bx = caps[0]["l"] - 32
        for c in caps:
            line(c["l"], c["cy"], bx, c["cy"])
        line(bx, caps[0]["cy"], bx, caps[-1]["cy"])
        arrow(bx, target["cy"], target["r"] + 2, target["cy"])
        label((bx + target["r"]) / 2, target["cy"] - 14, "isCapabilityOf")
        if num:
            callout(target["r"] + 32, target["t"] + 8, num)


def fed_by(side, valve, num):
    arrow(side["cx"], side["b"], side["cx"], valve["t"] - 2)
    my = (side["b"] + valve["t"]) / 2
    label(side["cx"] - 10, my, "isFedBy", anchor="rm")
    callout(side["cx"] + 28, my, num)


# --- Heat Exchanger (asset) ---------------------------------------------------
hx = box(660, 90, "Heat Exchanger", ASSET)
prim = box(480, 360, "Heat Exchanger\nPrimary Side", ASSET)
sec = box(840, 360, "Heat Exchanger\nSecondary Side", ASSET)
part_of(hx, [prim, sec], 290, 1)

prim_caps = [
    box(140, 300, "Entering Water\nTemperature Sensor", CAPABILITY),
    box(140, 420, "Leaving Water\nTemperature Sensor", CAPABILITY),
]
capabilities_of(prim, prim_caps, "left", 4)
sec_caps = [
    box(1180, 300, "Entering Water\nTemperature Sensor", CAPABILITY),
    box(1180, 420, "Leaving Water\nTemperature Sensor", CAPABILITY),
]
capabilities_of(sec, sec_caps, "right")

valve = box(480, 670, "Heating Hot\nWater Valve", ASSET)
fed_by(prim, valve, 2)
valve_caps = [
    box(140, 610, "Valve Position\nActuator", CAPABILITY),
    box(140, 730, "Valve Position\nState", CAPABILITY),
]
capabilities_of(valve, valve_caps, "left", 3)

# --- divider ------------------------------------------------------------------
for y in range(40, 770, 16):
    line(1350, y, 1350, y + 8)

# --- HVAC Heat Exchanger Group (collection) -----------------------------------
grp = box(1720, 90, "HVAC Heat\nExchanger Group", COLLECTION)
gprim = box(1540, 360, "Heat Exchanger Group\nPrimary Side", COLLECTION, w=220)
gsec = box(1900, 360, "Heat Exchanger Group\nSecondary Side", COLLECTION, w=220)
part_of(grp, [gprim, gsec], 290)
gvalve = box(1540, 670, "Heating Hot\nWater Valve", ASSET)
fed_by(gprim, gvalve, 5)

# --- legend -------------------------------------------------------------------
lx0, ly0, lx1, ly1 = 2140, 40, 2440, 520
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
