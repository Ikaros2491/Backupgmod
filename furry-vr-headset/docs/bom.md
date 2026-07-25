# Bill of Materials — Prototype v1

All dimensions in millimeters unless noted. Prefer the **primary** line; **alt** is drop-in where noted in CAD parameters (`cad/params.scad`).

## Optics & display

| Qty | Part | Key dims / notes | Source class |
|-----|------|------------------|--------------|
| 2 | SeeYa 1.03" Si-OLED 2560×2560 + pancake optical module | Module envelope **42×42×28**; FOV ~90°; IPD travel 56–72; eye relief ~12 | Tindie / Ali “pancake VR optical module” kits |
| 2 | MIPI → HDMI (or DP) driver / adapter board for SeeYa | Match vendor bundle; keep within electronics bay **120×70×50** | Bundled with display kit |
| 2 | M3×55 smooth rod | IPD guide rails | Hardware |
| 1 | M3 threaded rod + opposing nuts / printed nut shoes | IPD adjuster | Hardware |

## World tracking (primary — required for fur-covered shell)

| Qty | Part | Key dims / notes | Source class |
|-----|------|------------------|--------------|
| 1 | Tundra Tracker / Vive Tracker 3.0 (or equiv.) | Mounts on printed mast plate; keep ≥40 mm clear of fur at tip | SteamVR ecosystem |
| 2 | SteamVR Base Station 1.0 or 2.0 | Room outside-in reference | SteamVR |
| 1 | Printed tracker mast | `tracker_mast.stl` — ear/horn/dorsal spike | Print |
| 1 | *Alt:* magnetic tracker source + sensor | Tracks **through** fur/foam; watch metal distortion | Polhemus-class / OEM |

> Do **not** buy LiDAR expecting it to see through fur. See [world-tracking.md](world-tracking.md).

## Cameras (Quest-class + face)

| Qty | Part | Key dims / notes | Source class |
|-----|------|------------------|--------------|
| 4 | Quest 2 or Quest 3 **tracking camera** modules (harvested) | Pocket **12.0×12.0×5.2**; flex tail **8.0×1.2**; aperture Ø4.5 in shell | Donor headset tear-down |
| 4 | *Alt:* OV7251 / OV9282 global-shutter mini board | Use `ots_gs_camera_adapter` if board is **24×24×8** | Arducam / Waveshare |
| 2 | IR eye cameras (OV2640 850 nm or Quest Pro–class eye cams) | **8.5×8.5×5.0** | EyeTrackVR / Ali 850 nm modules |
| 1–2 | Lower-face / mouth IR camera | Same **8.5** envelope | Project Babble style |
| 12–16 | 850 nm IR LED (e.g. XL-3216HIRC-850 or 3 mm) | Face plate rings + mouth fill | LCSC / DigiKey |
| 2–3 | Seeed XIAO ESP32-S3 Sense *or* USB UVC bridge | Per-eye / mouth streaming to host | EyeTrackVR stack |

> Native Quest camera flex pinouts are proprietary. Harvested modules need a custom MIPI/USB bridge **or** use host software only after a known-good breakout. For first bring-up, run **OTS OV7251 + ESP/UVC IR cams** in the same mechanical pockets, then swap harvested Quest modules when the bridge is ready.

## Compute, sensing, power

| Qty | Part | Key dims / notes | Source class |
|-----|------|------------------|--------------|
| 1 | Host PC with dual HDMI/DP + USB3 | v1 tethered | — |
| 1 | BNO085 or ICM-42688 IMU breakout | 3/6DoF fusion with cameras | Adafruit / SparkFun |
| 1 | USB hub (small) | Inside electronics bay | Any |
| 1 | 2S–4S LiPo **or** USB-C PD bank | Fit occiput bay; use protected pack | Hobby / Anker-class |
| 1 | Buck 5 V / 3.3 V power board | Fan + MCU + IR LED rails | Any |
| 1 | Illuminated kill switch + 5 A fuse | Mount at neck | Hardware |

## Cooling

| Qty | Part | Key dims / notes | Source class |
|-----|------|------------------|--------------|
| 2 | 40×40×10 mm axial fan (5 V) | Screw pitch **32**; hole Ø36 | Noctua / generic |
| 1 | 30×30×10 mm blower (optional) | Battery bay | Generic 3010 |
| — | Dust mesh / speaker cloth | Behind cheek & snout intakes | Fabric |
| — | Thermal pads | Display driver ICs → duct walls | — |

## Soft goods & structure

| Qty | Part | Key dims / notes | Source class |
|-----|------|------------------|--------------|
| 1 | Printed outer shell (split) | ~**280 L × 220 W × 240 H** blank | `shell_outer.stl` |
| 1 | Optical chassis + IPD carriers | `optical_chassis.stl` | Print |
| 1 | Face interface plate | `face_interface.stl` | Print |
| 1 | Cooling duct set | `cooling_ducts.stl` | Print |
| 1 set | Camera cradles / adapters | `camera_mounts.stl` | Print |
| — | EVA / scuba foam face gasket | Cut from foam guide | Craft |
| — | M2 / M3 screws + heat-set inserts | See assembly doc | Hardware |
| — | Fur, foam, paint, ears | Buyer decoration — not part of rigid kit | — |

## Fastener budget (typical)

| Qty | Fastener |
|-----|----------|
| 40 | M3×8 button |
| 20 | M3×12 button |
| 20 | M2×6 |
| 30 | M3 heat-set inserts (short) |

## Rough power budget

| Load | Estimate |
|------|----------|
| Dual Micro-OLED + drivers | 3–6 W |
| Fans (2×40 + 3010) | 1–3 W |
| Cameras + MCUs + IR | 2–4 W |
| USB hub / IMU | ~1 W |
| **Total (tethered displays from PC)** | **~7–14 W on headset rails** |
