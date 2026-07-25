# Dimension sheet (prototype v1)

Source of truth: [`cad/params.scad`](../cad/params.scad). Update parameters there, then re-export STLs.

## Outer shell

| Dim | mm | Param |
|-----|---:|-------|
| Length (snout→occiput) | 280 | `shell_len` |
| Width | 220 | `shell_w` |
| Height | 240 | `shell_h` |
| Wall | 3.2 | `shell_wall` |
| Neck opening | 145 × 120 | `neck_opening_*` |

## Optical

| Dim | mm | Param |
|-----|---:|-------|
| Module envelope W×H×D | 42 × 42 × 28 | `optic_*` |
| Chassis W×H×D | 170 × 90 × 55 | `chassis_*` |
| IPD range | 56–72 | `ipd_min/max` |
| Nominal IPD | 64 | `ipd_nominal` |
| Eye relief | 12 | `eye_relief` |
| Lens OD (clearance) | 36 | `optic_lens_od` |

## Face interface

| Dim | mm | Param |
|-----|---:|-------|
| Plate W×H×T | 180 × 120 × 3 | `face_plate_*` |
| Foam channel width | 12 | `foam_channel_w` |
| Nose cutout | 40 × 28 | `nose_bridge_cut_*` |

## Cooling

| Dim | mm | Param |
|-----|---:|-------|
| Fan | 40 × 40 × 10 | `fan_40*` |
| Fan screw pitch | 32 | `fan_screw_pitch` |
| Intake slot | 50 × 18 | `intake_slot_*` |
| Exhaust slot | 60 × 22 | `exhaust_slot_*` |
| Optional blower | 30 × 30 × 10 | `blower_3010_*` |

## In-shell pose bay

| Dim | mm | Param |
|-----|---:|-------|
| Bay W×D×H | 55 × 28 × 40 | `pose_bay_*` |
| Bay center Y / Z | 75 / 5 | `pose_bay_y/z` |
| Mag sensor envelope | 22 × 14 × 10 | `mag_sensor_*` |
| UWB module envelope | 28 × 22 × 5 | `uwb_module_*` |
| Decorator ferrous keep-out R | 45 | `pose_keepout_r` |

## Cameras

| Dim | mm | Param |
|-----|---:|-------|
| Quest cam pocket | 12 × 12 × 5.2 | `quest_cam_*` |
| Quest flex | 8 × 1.2 × 18 | `quest_cam_flex_*` |
| OTS GS board | 24 × 24 × 8 | `ots_gs_cam_*` |
| IR face/eye cam | 8.5 × 8.5 × 5 | `ir_cam_*` |
| World cam lateral | ±85 | `world_cam_lateral` |
| World cam forward | 55 | `world_cam_forward` |
| World cam vertical | ±35 | `world_cam_vertical` |

## Mass budget (estimated)

| Assembly | g |
|----------|--:|
| Shell (PETG, 15% infill, split) | 450–650 |
| Optical chassis + carriers | 80–120 |
| Dual pancake+OLED modules | 80–120 |
| Ducts + fans | 100–150 |
| Boards + hub + IMU | 80–120 |
| Battery (2S–4S small) | 100–200 |
| Cameras + cabling | 40–80 |
| Foam / pads | 40–80 |
| **Total before fur** | **~1.0–1.5 kg** |
| Fur / foam decoration | +200–600 |

Balance point should sit near the upper neck — add occiput ballast only if snout-heavy after decoration.
