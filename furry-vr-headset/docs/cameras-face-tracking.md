# Cameras & face tracking

DIY stack reuses **Quest-class camera parts** (or the same sensor class) as an *optional* optical layer, plus IR cameras for eye/face.

**Room / headset 6DoF is not solved by these cameras** when buyers cover the shell in craft. See [world-tracking.md](world-tracking.md): **in-shell magnetic + IMU** (optional UWB). LiDAR and inside-out cams fail under pile fur and fight the blank-shell product.

## Roles

| Role | Count | Sensor class | Notes |
|------|------:|--------------|-------|
| World / room pose (primary) | 1 | In-shell magnetic sensor + IMU | Occiput bay; craft-agnostic |
| World / room pose (companion) | 0–1 | In-shell UWB tag | Optional |
| World / SLAM / passthrough (optional) | 4 | Quest 2/3-class global shutter | Experiments only — not required for product pose |
| Eye tracking | 2 | IR OV2640 / Quest Pro-class eye cams | Inward; fur irrelevant |
| Lower face / mouth | 1–2 | IR UVC or ESP-hosted | Inward; fur irrelevant |

## Mechanical pockets

Defined in `cad/params.scad` and cut into `shell_outer` / `optical_chassis`:

| Pocket | Envelope (mm) | Flex |
|--------|---------------|------|
| Quest harvested tracking cam | 12.0 × 12.0 × 5.2 | 8.0 × 1.2 × 18 channel |
| OTS GS adapter board | 24 × 24 × 8 | Use `ots_gs_camera_adapter` |
| IR eye/mouth cam | 8.5 × 8.5 × 5.0 | Side exit toward bay |

Shell outer apertures for world cams are **Ø4.5 mm** so fur can hide them.

## Harvested Quest cameras — practical reality

- Quest tracking cameras are excellent global-shutter modules but use **proprietary flex pinouts** and often pair with a specific ISP/SoC pipeline.  
- **Mechanics in this repo are ready** for the harvested envelope on day one.  
- **Electrical bring-up** for true Quest modules is a separate hardware task (MIPI bridge / FPGA / reverse-engineered flex).  
- Recommended prototype path:
  1. Print pockets + cradles.  
  2. Fit **OTS OV7251/OV9282** boards via adapters for SLAM experiments.  
  3. Run face/eye on ESP32-S3 + 850 nm cams (EyeTrackVR / Babble).  
  4. Swap in harvested Quest modules when a bridge board exists — no shell reprint if envelopes match.

## Face tracking illumination

- Use **850 nm** LEDs in the face-plate rings (`face_interface.scad`).  
- Drive with constant-current or resistor-limited 3.3/5 V rails; PWM for exposure matching.  
- Keep LEDs outside the optical path of the pancake lenses; baffle stray IR from the Micro-OLEDs if needed.

## Software (host)

| Pipeline | Suggested stack |
|----------|-----------------|
| Mouth / face blendshapes | Project Babble → OSC / VRCFaceTracking |
| Eye gaze | EyeTrackVR → VRCFT |
| Head pose v1 | IMU (HadesVR-style) |
| Head pose v2 | Basalt / OpenVSLAM on world cams |

## Calibration

1. Intrinsics per camera (checkerboard / ChArUco).  
2. Extrinsics: world cams → IMU → optical frame (CAD nominals in `params.scad` are the prior).  
3. Eye cams: gaze calibration per wearer.  
4. Mouth cam: Babble trainer with shell on (fur may change IR bounce — recalibrate after decoration).
