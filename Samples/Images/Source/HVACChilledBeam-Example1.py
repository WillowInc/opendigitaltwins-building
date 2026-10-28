"""Renders Samples/Images/HVACChilledBeam-Example1.png.

Active chilled beams: each beam isFedBy the CAV Box (supply air) and the chilled
water pump (chilled water); valve points on the beams, primary air control points
on the CAV Box. Zone air points are not shown here, they belong to the HVAC Zone
(see Example2).

    python Samples/Images/Source/HVACChilledBeam-Example1.py

Requires Pillow. Uses Segoe UI when available, otherwise DejaVu Sans.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor; drawn at 2x, downscaled at the end
W, H = 2460, 940

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
OUT = os.path.join(HERE, "..", "HVACChilledBeam-Example1.png")


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


def fed_by_up(sources, target, bus_y, text, num=None):
    """sources (below) isFedBy target (above): verticals up to a bus, one arrow into target."""
    for c in sources:
        line(c["cx"], c["t"], c["cx"], bus_y)
    if len(sources) > 1:
        line(sources[0]["cx"], bus_y, sources[-1]["cx"], bus_y)
    arrow(target["cx"], bus_y, target["cx"], target["b"] + 2)
    my = (bus_y + target["b"]) / 2
    label(target["cx"] - 16, my, text, anchor="rm")
    if num:
        callout(target["cx"] + 28, my, num)


def fed_by_down(sources, target, bus_y, text, num=None):
    """sources (above) isFedBy target (below): verticals down to a bus, one arrow into target."""
    for c in sources:
        line(c["cx"], c["b"], c["cx"], bus_y)
    if len(sources) > 1:
        line(sources[0]["cx"], bus_y, sources[-1]["cx"], bus_y)
    arrow(target["cx"], bus_y, target["cx"], target["t"] - 2)
    my = (bus_y + target["t"]) / 2
    label(target["cx"] - 16, my, text, anchor="rm")
    if num:
        callout(target["cx"] + 28, my, num)


# --- air path: AHU <- CAV Box <- beams ---------------------------------------
ahu = box(200, 110, "Air Handling Unit", ASSET)
cav = box(940, 110, "CAV Box", ASSET)
arrow(cav["l"], cav["cy"], ahu["r"] + 2, ahu["cy"])
label((cav["l"] + ahu["r"]) / 2, ahu["cy"] - 14, "isFedBy")
cav_caps = [
    box(1600, 70, "Discharge Air\nTemperature Sensor", CAPABILITY),
    box(1600, 190, "Discharge Airflow\nSensor", CAPABILITY),
]
capabilities_of(cav, cav_caps, "right", 3)

beam1 = box(700, 440, "Active Chilled Beam", ASSET, w=220)
beam2 = box(1180, 440, "Active Chilled Beam", ASSET, w=220)
fed_by_up([beam1, beam2], cav, 300, "isFedBy\n(substance: SupplyAir)", num=1)

beam1_caps = [box(280, 440, "Chilled Water Valve\nPosition Actuator", CAPABILITY)]
capabilities_of(beam1, beam1_caps, "left", 2)
beam2_caps = [box(1600, 440, "Chilled Water Valve\nPosition Actuator", CAPABILITY)]
capabilities_of(beam2, beam2_caps, "right")

# --- water path: Chiller <- Chilled Water Pump <- beams ----------------------
pump = box(940, 780, "Chilled Water Pump", ASSET, w=220)
fed_by_down([beam1, beam2], pump, 620, "isFedBy\n(substance: ChilledWater)")
chiller = box(200, 780, "Chiller", ASSET)
arrow(pump["l"], pump["cy"], chiller["r"] + 2, chiller["cy"])
label((pump["l"] + chiller["r"]) / 2, chiller["cy"] - 14, "isFedBy")

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
