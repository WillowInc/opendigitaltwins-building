"""Renders Samples/Images/HVACDuctHeater-Example2.png.

Duct heater with no terminal unit in the path: the HVAC Zone isFedBy the duct
heater, the duct heater isFedBy the Air Handling Unit, and the AHU has no
relationship to the zone. The heater has a Heating Coil component and its own
discharge air temperature sensor; the zone air points are capabilities of the
HVAC Zone.

    python Samples/Images/Source/HVACDuctHeater-Example2.py

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
OUT = os.path.join(HERE, "..", "HVACDuctHeater-Example2.png")


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


def fed_by_up(source, target, text, num=None):
    """source (below) isFedBy target (above)."""
    arrow(source["cx"], source["t"], target["cx"], target["b"] + 2)
    my = (source["t"] + target["b"]) / 2
    label(target["cx"] - 16, my, text, anchor="rm")
    if num:
        callout(target["cx"] + 28, my, num)


# --- air path: AHU <- Duct Heater <- HVAC Zone ---------------------------------
ahu = box(760, 110, "Air Handling Unit", ASSET)
capabilities_of(ahu, [box(1180, 110, "Discharge Air\nTemperature Sensor", CAPABILITY)])

heater = box(760, 400, "Duct Heater", ASSET)
fed_by_up(heater, ahu, "isFedBy\n(substance: SupplyAir)", num=1)

coil = box(340, 400, "Heating Coil", ASSET)
arrow(coil["r"], coil["cy"], heater["l"] - 2, heater["cy"])
label((coil["r"] + heater["l"]) / 2, heater["cy"] - 14, "isPartOf")
capabilities_of(heater, [box(1180, 340, "Discharge Air\nTemperature Sensor", CAPABILITY),
                         box(1180, 460, "High Temperature\nAlarm State", CAPABILITY)])

zone = box(760, 720, "HVAC Zone", SPACE)
fed_by_up(zone, heater, "isFedBy\n(substance: SupplyAir)", num=2)
capabilities_of(zone, [box(1180, 660, "Zone Air\nTemperature Sensor", CAPABILITY),
                       box(1180, 780, "Zone Air\nTemperature Setpoint", CAPABILITY)], num=3)

# --- callout 4: the AHU has no relationship to the zone --------------------------
callout(ahu["cx"] - 30, ahu["t"] - 26, 4)

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
