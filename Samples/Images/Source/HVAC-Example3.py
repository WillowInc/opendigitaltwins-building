"""Renders Samples/Images/HVAC-Example3.png.

HVAC Basic Relationships with Level: a Fan Powered Box and a Rooftop Unit each feed
an HVAC Zone, and both zones are part of the 1st Floor. The box is located on the
1st Floor; the Rooftop Unit is located on the Roof. Each zone's Zone Air Temperature
Sensor and Zone Air Temperature Setpoint are capabilities of the HVAC Zone, not of
the unit which serves it.

    python Samples/Images/Source/HVAC-Example3.py

Requires Pillow. Uses Segoe UI when available, otherwise DejaVu Sans.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor; drawn at 2x, downscaled at the end
W, H = 2140, 850

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
OUT = os.path.join(HERE, "..", "HVAC-Example3.png")


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


# --- units, the zones they feed, and the levels -------------------------------------
fpb = box(700, 150, "Fan Powered Box", ASSET, w=240)
rtu = box(1120, 150, "Rooftop Unit", ASSET, w=240)
zone_l = box(700, 420, "HVAC Zone", SPACE, w=240)
zone_r = box(1120, 420, "HVAC Zone", SPACE, w=240)
floor1 = box(910, 760, "Level\n1st Floor", SPACE, w=240)
roof = box(1540, 760, "Level\nRoof", SPACE, w=240)

for z, u in ((zone_l, fpb), (zone_r, rtu)):
    arrow(z["cx"], z["t"], u["cx"], u["b"] + 2)
    label(z["cx"] - 14, (z["t"] + u["b"]) / 2, "isFedBy", anchor="rm")

# --- both zones isPartOf the 1st Floor ------------------------------------------
bus_y = 610
for z in (zone_l, zone_r):
    line(z["cx"], z["b"], z["cx"], bus_y)
line(zone_l["cx"], bus_y, zone_r["cx"], bus_y)
arrow(floor1["cx"], bus_y, floor1["cx"], floor1["t"] - 2)
label(floor1["cx"] - 14, (bus_y + floor1["t"]) / 2, "isPartOf", anchor="rm")
callout(floor1["cx"] + 28, (bus_y + floor1["t"]) / 2, 1)

# --- zone air points are capabilities of each HVAC Zone ------------------------------
caps_l = [box(280, 340, "Zone Air\nTemperature Setpoint", CAPABILITY, w=240),
          box(280, 500, "Zone Air\nTemperature Sensor", CAPABILITY, w=240)]
capabilities_of(zone_l, caps_l, "left", 4)
caps_r = [box(1540, 340, "Zone Air\nTemperature Setpoint", CAPABILITY, w=240),
          box(1540, 500, "Zone Air\nTemperature Sensor", CAPABILITY, w=240)]
capabilities_of(zone_r, caps_r, "right")

# --- locatedIn: box on the 1st Floor, Rooftop Unit on the Roof ------------------------
lx = 90
line(fpb["l"], fpb["cy"], lx, fpb["cy"], lx, floor1["cy"])
arrow(lx, floor1["cy"], floor1["l"] - 2, floor1["cy"])
label(lx + 12, 640, "locatedIn", anchor="lm")
callout(lx, 420, 2)

rx = 1730
line(rtu["r"], rtu["cy"], rx, rtu["cy"], rx, roof["cy"])
arrow(rx, roof["cy"], roof["r"] + 2, roof["cy"])
label(rx - 12, 640, "locatedIn", anchor="rm")
callout(rx, 420, 3)

# --- legend -------------------------------------------------------------------
lx0, ly0, lx1, ly1 = 1810, 40, 2110, 520
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
