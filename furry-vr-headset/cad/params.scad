// =============================================================================
// Fursuit-Integrated DIY VR Headset — Shared Parameters
// Units: millimeters
// Prototype stack: dual SeeYa 1.03" pancake modules + Quest-class cameras
// =============================================================================

$fn = 64;

// --- Human fit ---
ipd_min = 56;
ipd_max = 72;
ipd_nominal = 64;
eye_relief = 12;
head_breadth = 155;          // temple-to-temple clearance target
face_depth = 95;             // brow to back of optical sled allowance
neck_opening_w = 145;
neck_opening_d = 120;

// --- Optical modules (SeeYa 1.03" + pancake pair) ---
// Envelope measured from typical Tindie/Ali pancake+display kits.
optic_w = 42;
optic_h = 42;
optic_d = 28;                // display plane to front of pancake stack
optic_lens_od = 36;
optic_mount_boss = 3;        // M3 clearance around each corner

// Optical chassis sled
chassis_wall = 2.4;
chassis_w = 170;
chassis_h = 90;
chassis_d = 55;
ipd_slot_len = (ipd_max - ipd_min) / 2 + 2;

// --- Outer fursuit shell (blank, decorateable) ---
shell_len = 280;             // snout tip to occiput
shell_w = 220;
shell_h = 240;
shell_wall = 3.2;
shell_cheek_r = 70;
decoration_boss_od = 8;
decoration_boss_id = 3.2;    // M3 heat-set or wood-screw pilot
decoration_boss_h = 6;

// --- Face interface / foam gasket plane ---
face_plate_w = 180;
face_plate_h = 120;
face_plate_t = 3;
foam_channel_w = 12;
nose_bridge_cut_w = 40;
nose_bridge_cut_h = 28;

// --- Active cooling ---
fan_40 = 40;
fan_40_thick = 10;
fan_40_hole = 36;
fan_screw_pitch = 32;
blower_3010_w = 30;
blower_3010_h = 30;
blower_3010_d = 10;
duct_wall = 1.6;
intake_slot_w = 50;
intake_slot_h = 18;
exhaust_slot_w = 60;
exhaust_slot_h = 22;

// --- Cameras (Quest-class + face/eye) ---
// Harvested Quest 2/3 tracking camera approximate envelope (sensor + tiny PCB + lens).
// Flex tails need a 1.2 x 8 channel out of the pocket.
quest_cam_w = 12.0;
quest_cam_h = 12.0;
quest_cam_d = 5.2;
quest_cam_flex_w = 8.0;
quest_cam_flex_h = 1.2;
quest_cam_flex_len = 18;

// OTS global-shutter alternative (Arducam / Waveshare mini OV7251 style)
ots_gs_cam_w = 24;
ots_gs_cam_h = 24;
ots_gs_cam_d = 8;

// Eye / lower-face IR cameras (EyeTrackVR / Project Babble class OV2640 850nm)
ir_cam_w = 8.5;
ir_cam_h = 8.5;
ir_cam_d = 5.0;
ir_led_od = 3.2;

// World-tracking camera placement on outer shell (from optical center)
world_cam_forward = 55;
world_cam_lateral = 85;
world_cam_vertical = 35;
world_cam_down_angle = 15;   // degrees, tip toward floor for floor features

// Face cameras relative to lens centers
eye_cam_offset_x = 18;       // temporal of each eye
eye_cam_offset_y = -8;       // slightly below pupil line
mouth_cam_y = -45;           // below optical chassis
mouth_cam_z = 25;            // forward of face plane

// --- Fasteners ---
m3_clear = 3.3;
m3_tap = 2.5;
m2_clear = 2.2;

// --- Helpers ---
module rounded_box(size, r = 4, center = false) {
    x = size[0]; y = size[1]; z = size[2];
    translate(center ? [-x/2, -y/2, -z/2] : [0, 0, 0])
    hull() {
        for (xi = [r, x - r])
        for (yi = [r, y - r])
        for (zi = [r, z - r])
            translate([xi, yi, zi]) sphere(r = r);
    }
}

module m3_hole(h = 20) {
    cylinder(d = m3_clear, h = h, center = true);
}

module decoration_boss() {
    difference() {
        cylinder(d = decoration_boss_od, h = decoration_boss_h);
        translate([0, 0, -0.1])
            cylinder(d = decoration_boss_id, h = decoration_boss_h + 0.2);
    }
}
