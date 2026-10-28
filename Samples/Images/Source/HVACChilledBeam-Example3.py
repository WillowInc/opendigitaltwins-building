"""Renders Samples/Images/HVACChilledBeam-Example3.png.

Passive chilled beam and the HVAC Zone: the beam is fed by chilled water only and
is not in the air path, so the zone isFedBy both the beam and the ventilating VAV
Box. The zone air points are capabilities of the HVAC Zone; the VAV Box carries
its discharge air points and the beam carries only its valve points.

    python Samples/Images/Source/HVACChilledBeam-Example3.py

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
OUT = os.path.join(HERE, "..", "HVACChilledBeam-Example3.png")


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


# --- air path: AHU <- VAV Box -------------------------------------------------------
ahu = box(200, 110, "Air Handling Unit", ASSET)
vav = box(940, 110, "VAV Box", ASSET)
arrow(vav["l"], vav["cy"], ahu["r"] + 2, ahu["cy"])
label((vav["l"] + ahu["r"]) / 2, ahu["cy"] - 14, "isFedBy")
vav_caps = [
    box(1600, 70, "Discharge Air\nTemperature Sensor", CAPABILITY),
    box(1600, 190, "Discharge Airflow\nSensor", CAPABILITY),
]
capabilities_of(vav, vav_caps, "right")

# --- water path: Chiller <- Chilled Water Pump <- Passive Chilled Beam ----------------
chiller = box(200, 800, "Chiller", ASSET)
pump = box(200, 480, "Chilled Water Pump", ASSET, w=220)
arrow(pump["cx"], pump["b"], chiller["cx"], chiller["t"] - 2)
label(pump["cx"] - 12, (pump["b"] + chiller["t"]) / 2, "isFedBy", anchor="rm")

beam = box(620, 480, "Passive Chilled Beam", ASSET, w=230)
arrow(beam["l"], beam["cy"], pump["r"] + 2, pump["cy"])
label((beam["l"] + pump["r"]) / 2, pump["cy"] - 26, "isFedBy\n(substance: ChilledWater)")
callout((beam["l"] + pump["r"]) / 2, pump["cy"] + 28, 1)
beam_caps = [box(620, 760, "Chilled Water Valve\nPosition Actuator", CAPABILITY)]
line(beam_caps[0]["cx"], beam_caps[0]["t"], beam["cx"], beam["b"] + 2)
arrow(beam_caps[0]["cx"], beam_caps[0]["t"], beam["cx"], beam["b"] + 2)
label(beam["cx"] + 12, (beam["b"] + beam_caps[0]["t"]) / 2, "isCapabilityOf", anchor="lm")

# --- HVAC Zone (space): two feeders ---------------------------------------------------
zone = box(1180, 800, "HVAC Zone", SPACE)
# zone isFedBy VAV Box (supply air): straight up
arrow(zone["cx"] - 60, zone["t"], zone["cx"] - 60, vav["b"] + 2)
label(zone["cx"] - 74, 300, "isFedBy\n(substance: SupplyAir)", anchor="rm")
# zone isFedBy Passive Chilled Beam (chilled water): up to the beam's row, then left into it
line(zone["cx"] + 60, zone["t"], zone["cx"] + 60, beam["cy"])
arrow(zone["cx"] + 60, beam["cy"], beam["r"] + 2, beam["cy"])
label((beam["r"] + zone["cx"] - 60) / 2, beam["cy"] - 26, "isFedBy\n(substance: ChilledWater)")
callout(zone["l"] - 32, zone["t"] + 8, 2)

zone_caps = [
    box(1600, 740, "Zone Air\nTemperature Sensor", CAPABILITY),
    box(1600, 860, "Zone Air\nTemperature Setpoint", CAPABILITY),
]
capabilities_of(zone, zone_caps, "right", 3)

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
