#!/usr/bin/env python3
"""Render orthographic blueprint sheets as PNG images."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "renders"
ART = Path("/opt/cursor/artifacts/furry-vr-blueprints")
OUT.mkdir(parents=True, exist_ok=True)
ART.mkdir(parents=True, exist_ok=True)

BG = (247, 243, 234)
INK = (26, 26, 26)
DIM = (0, 120, 70)
SHELL = (212, 186, 140)
BAY = (120, 140, 158)
DUCT = (90, 160, 190)
POSE = (180, 90, 60)
CAM = (230, 120, 40)
GUIDE = (160, 160, 160)


def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def save(img, name):
    p1 = OUT / name
    p2 = ART / name
    img.save(p1, "PNG")
    img.save(p2, "PNG")
    print(f"Wrote {p1}")


def title_block(draw, w, h, sheet, title):
    draw.rectangle([20, h - 70, w - 20, h - 20], outline=INK, width=2)
    draw.text((32, h - 58), f"SHEET {sheet}  |  {title}", fill=INK, font=font(16, True))
    draw.text((32, h - 36), "Fursuit VR Blank Shell  ·  Rev B  ·  Units: mm  ·  In-shell magnetic pose", fill=INK, font=font(12))
    draw.text((w - 280, h - 36), "furry-vr-headset/cad", fill=GUIDE, font=font(12))


def dim_h(draw, x1, x2, y, label):
    draw.line([(x1, y), (x2, y)], fill=DIM, width=2)
    draw.line([(x1, y - 6), (x1, y + 6)], fill=DIM, width=2)
    draw.line([(x2, y - 6), (x2, y + 6)], fill=DIM, width=2)
    tw = draw.textlength(label, font=font(13))
    draw.text(((x1 + x2) / 2 - tw / 2, y + 8), label, fill=DIM, font=font(13))


def dim_v(draw, x, y1, y2, label):
    draw.line([(x, y1), (x, y2)], fill=DIM, width=2)
    draw.line([(x - 6, y1), (x + 6, y1)], fill=DIM, width=2)
    draw.line([(x - 6, y2), (x + 6, y2)], fill=DIM, width=2)
    # vertical text approximated by short horizontal label
    draw.text((x + 10, (y1 + y2) / 2 - 6), label, fill=DIM, font=font(13))


def sheet_side():
    w, h = 1200, 850
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((28, 24), "SIDE SECTION — XR (wearer faces −Y / snout left)", fill=INK, font=font(22, True))
    d.text((28, 54), "Optical chassis, face wash, electronics, occiput pose bay, cranial exhaust", fill=INK, font=font(14))

    # Shell silhouette
    d.ellipse([180, 160, 820, 620], fill=SHELL, outline=INK, width=3)
    d.ellipse([90, 300, 320, 520], fill=SHELL, outline=INK, width=2)  # snout

    # Optical bay
    d.rounded_rectangle([360, 300, 560, 420], radius=12, fill=BAY, outline=INK, width=2)
    d.text((390, 340), "optical chassis", fill=INK, font=font(13, True))
    d.text((390, 360), "170 × 90 × 55", fill=INK, font=font(12))

    # Face plate
    d.rectangle([340, 310, 358, 410], fill=(90, 90, 90), outline=INK)
    d.text((250, 280), "face plate\n+ foam", fill=INK, font=font(12))

    # Duct / face wash
    d.rounded_rectangle([300, 360, 360, 430], radius=6, fill=DUCT, outline=INK)
    d.text((200, 400), "cheek intake →", fill=DUCT, font=font(12))

    # Electronics
    d.rounded_rectangle([520, 250, 700, 340], radius=8, fill=(150, 160, 175), outline=INK)
    d.text((540, 275), "electronics bay", fill=INK, font=font(12, True))
    d.text((540, 295), "drivers / hub / IMU", fill=INK, font=font(11))

    # Fans
    d.ellipse([560, 180, 620, 240], outline=INK, width=3)
    d.ellipse([640, 180, 700, 240], outline=INK, width=3)
    d.text((560, 150), "40 mm exhaust fans", fill=INK, font=font(12))

    # Pose bay
    d.rounded_rectangle([640, 360, 760, 440], radius=8, fill=POSE, outline=INK, width=2)
    d.text((652, 380), "POSE BAY", fill=(255, 255, 255), font=font(12, True))
    d.text((652, 400), "magnetic+UWB", fill=(255, 240, 230), font=font(11))

    # World cam markers
    d.ellipse([250, 240, 268, 258], fill=CAM)
    d.ellipse([280, 480, 298, 498], fill=CAM)
    d.text((275, 220), "opt. world cam", fill=CAM, font=font(11))

    # Airflow arrows
    d.line([(140, 380), (300, 390)], fill=(0, 160, 200), width=3)
    d.polygon([(300, 390), (285, 382), (285, 398)], fill=(0, 160, 200))
    d.line([(620, 290), (630, 210)], fill=(0, 160, 200), width=3)

    dim_h(d, 90, 820, 680, "shell_len 280")
    dim_v(d, 860, 160, 620, "shell_h 240")

    d.text((90, 700), "SNDOUT (−Y)", fill=GUIDE, font=font(12))
    d.text((720, 700), "OCCIPUT (+Y)", fill=GUIDE, font=font(12))
    title_block(d, w, h, "1", "Side section blueprint")
    save(im, "blueprint_01_side.png")


def sheet_front():
    w, h = 1200, 850
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((28, 24), "FRONT ELEVATION — looking at wearer", fill=INK, font=font(22, True))
    d.text((28, 54), "Lens centers at ±IPD/2  ·  Decoration bosses  ·  Optional world cams", fill=INK, font=font(14))

    # Head front oval
    d.ellipse([300, 120, 900, 680], fill=SHELL, outline=INK, width=3)
    # Cheeks
    d.ellipse([240, 300, 420, 520], fill=SHELL, outline=INK, width=2)
    d.ellipse([780, 300, 960, 520], fill=SHELL, outline=INK, width=2)

    # Face bay
    d.rounded_rectangle([420, 280, 780, 480], radius=16, fill=BAY, outline=INK, width=2)
    # Lenses
    for cx in (520, 680):
        d.ellipse([cx - 45, 320, cx + 45, 410], fill=(40, 80, 110), outline=INK, width=2)
        # IR LED ring ticks
        for i in range(6):
            import math
            a = i * 60 * math.pi / 180
            x = cx + 55 * math.cos(a)
            y = 365 + 40 * math.sin(a)
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(200, 80, 80))
    d.text((490, 430), "L", fill=(255, 255, 255), font=font(14, True))
    d.text((650, 430), "R", fill=(255, 255, 255), font=font(14, True))
    d.text((560, 450), "mouth IR cam", fill=CAM, font=font(12))
    d.rectangle([585, 468, 615, 488], fill=CAM, outline=INK)

    # Cheek intakes
    d.rectangle([250, 380, 290, 450], fill=DUCT, outline=INK)
    d.rectangle([910, 380, 950, 450], fill=DUCT, outline=INK)
    d.text((200, 460), "intake", fill=DUCT, font=font(12))
    d.text((910, 460), "intake", fill=DUCT, font=font(12))

    # World cams
    for xy in [(360, 180), (820, 180), (360, 560), (820, 560)]:
        d.ellipse([xy[0], xy[1], xy[0] + 16, xy[1] + 16], fill=CAM, outline=INK)

    # Bosses
    for xy in [(600, 150), (400, 220), (800, 220), (600, 620)]:
        d.ellipse([xy[0] - 6, xy[1] - 6, xy[0] + 6, xy[1] + 6], outline=INK, width=2)

    dim_h(d, 240, 960, 720, "shell_w 220")
    dim_h(d, 520, 680, 250, "IPD nom 64 (56–72)")
    title_block(d, w, h, "2", "Front elevation blueprint")
    save(im, "blueprint_02_front.png")


def sheet_top():
    w, h = 1200, 850
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((28, 24), "TOP PLAN — looking down (−Z toward page)", fill=INK, font=font(22, True))
    d.text((28, 54), "IPD rails  ·  Exhaust fans  ·  In-shell pose bay (occiput)  ·  Craft layer unconstrained", fill=INK, font=font(14))

    d.ellipse([220, 180, 980, 620], fill=SHELL, outline=INK, width=3)
    d.ellipse([140, 300, 360, 500], fill=SHELL, outline=INK, width=2)  # snout

    # Optical
    d.rounded_rectangle([400, 300, 720, 480], radius=12, fill=BAY, outline=INK, width=2)
    d.rectangle([430, 340, 520, 440], outline=INK, width=2)
    d.rectangle([600, 340, 690, 440], outline=INK, width=2)
    d.text((445, 375), "L optic", fill=INK, font=font(12))
    d.text((615, 375), "R optic", fill=INK, font=font(12))
    d.line([(430, 460), (690, 460)], fill=DIM, width=2)
    d.text((520, 500), "IPD 56–72", fill=DIM, font=font(12))

    # Fans
    d.ellipse([760, 220, 820, 280], outline=INK, width=3)
    d.ellipse([840, 220, 900, 280], outline=INK, width=3)
    d.text((760, 190), "exhaust fans", fill=INK, font=font(12))

    # Pose bay
    d.rounded_rectangle([780, 380, 920, 480], radius=8, fill=POSE, outline=INK, width=2)
    d.text((795, 410), "POSE BAY", fill=(255, 255, 255), font=font(13, True))
    d.text((795, 432), "mag + UWB", fill=(255, 240, 230), font=font(11))
    d.ellipse([790, 370, 910, 490], outline=(200, 80, 60), width=2)
    d.text((790, 505), "ferrous keep-out Ø90", fill=POSE, font=font(11))

    # Cams
    for xy in [(380, 240), (740, 240), (380, 520), (740, 520)]:
        d.ellipse([xy[0], xy[1], xy[0] + 14, xy[1] + 14], fill=CAM)

    d.text((160, 400), "SNDOUT", fill=GUIDE, font=font(12))
    d.text((930, 400), "OCCIPUT", fill=GUIDE, font=font(12))
    title_block(d, w, h, "3", "Top plan blueprint")
    save(im, "blueprint_03_top.png")


def sheet_stackup():
    w, h = 1200, 850
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((28, 24), "ASSEMBLY STACK-UP — layers outside → inside", fill=INK, font=font(22, True))
    d.text((28, 54), "Buyer craft is exterior only  ·  Pose / optics / cooling stay in the shell kit", fill=INK, font=font(14))

    layers = [
        ("1  Buyer craft", "Fur, foam, paint, ears, horns — freeform", (230, 200, 160)),
        ("2  Outer shell", "Blank PETG shell + decoration bosses", SHELL),
        ("3  Cooling ducts", "Cheek intake → face wash → cranial fans", DUCT),
        ("4  Optical chassis", "Dual pancake modules + IPD rails", BAY),
        ("5  Face interface", "Foam gasket, IR LED rings, light seal", (140, 140, 150)),
        ("6  Pose bay (occiput)", "Magnetic sensor + IMU (+ opt. UWB)", POSE),
        ("7  Wearer", "Eye relief ~12 mm to pancake exit", (220, 220, 220)),
    ]
    y = 100
    for title, desc, color in layers:
        d.rounded_rectangle([80, y, 1120, y + 70], radius=10, fill=color, outline=INK, width=2)
        d.text((100, y + 14), title, fill=INK, font=font(18, True))
        d.text((100, y + 42), desc, fill=INK, font=font(14))
        y += 85

    title_block(d, w, h, "4", "Assembly stack-up")
    save(im, "blueprint_04_stackup.png")


def sheet_pose():
    w, h = 1200, 850
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((28, 24), "IN-SHELL POSE SYSTEM — craft-agnostic room tracking", fill=INK, font=font(22, True))
    d.text((28, 54), "No exterior windows  ·  Magnetic field / UWB radio pass through buyer fur & foam", fill=INK, font=font(14))

    # Room source
    d.rounded_rectangle([80, 120, 320, 280], radius=12, fill=(200, 210, 230), outline=INK, width=2)
    d.text((100, 150), "ROOM", fill=INK, font=font(16, True))
    d.text((100, 180), "Magnetic source", fill=INK, font=font(14))
    d.text((100, 205), "(desk / wall / ceiling)", fill=INK, font=font(12))
    d.text((100, 235), "Optional UWB anchors", fill=INK, font=font(12))

    # Arrow
    d.line([(320, 200), (480, 200)], fill=DIM, width=4)
    d.polygon([(480, 200), (460, 188), (460, 212)], fill=DIM)
    d.text((330, 160), "field / radio\nthrough craft", fill=DIM, font=font(13))

    # Shell with craft
    d.ellipse([500, 100, 1100, 650], fill=(210, 180, 140), outline=INK, width=3)
    d.text((720, 120), "BUYER CRAFT LAYER", fill=INK, font=font(14, True))
    # inner shell dashed approx
    d.ellipse([560, 180, 1040, 580], outline=INK, width=2)
    d.rounded_rectangle([820, 320, 980, 420], radius=8, fill=POSE, outline=INK, width=2)
    d.text((835, 345), "POSE BAY", fill=(255, 255, 255), font=font(14, True))
    d.text((835, 370), "mag sensor", fill=(255, 240, 230), font=font(12))
    d.text((835, 390), "+ UWB + IMU", fill=(255, 240, 230), font=font(12))

    d.rounded_rectangle([620, 300, 780, 420], radius=8, fill=BAY, outline=INK)
    d.text((640, 340), "optics", fill=INK, font=font(13, True))
    d.text((640, 365), "(DIY VR)", fill=INK, font=font(12))

    d.text((560, 620), "Exterior may be fully covered — pose stays inside.", fill=INK, font=font(14, True))
    d.text((560, 650), "Decorator rule: no large steel in occiput keep-out Ø90 mm.", fill=POSE, font=font(13))

    title_block(d, w, h, "5", "In-shell pose / craft contract")
    save(im, "blueprint_05_pose.png")


if __name__ == "__main__":
    sheet_side()
    sheet_front()
    sheet_top()
    sheet_stackup()
    sheet_pose()
    print("Done")
