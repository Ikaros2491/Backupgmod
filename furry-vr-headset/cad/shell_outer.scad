// Blank decorateable fursuit head outer shell with VR bay + cooling apertures
include <params.scad>

module shell_envelope() {
    // Stylized toon-head hull — species-agnostic blank
    hull() {
        // cranial bulb
        translate([0, 30, 40])
            scale([shell_w/2, shell_len*0.35, shell_h*0.42])
                sphere(r = 1);
        // cheek masses
        for (s = [-1, 1])
            translate([s * (shell_w/2 - shell_cheek_r*0.55), 10, -10])
                scale([0.9, 1.1, 1.0])
                    sphere(r = shell_cheek_r);
        // snout block
        translate([0, -shell_len/2 + 55, -20])
            rotate([12, 0, 0])
                scale([0.55, 1.0, 0.55])
                    sphere(r = 70);
        // jaw / chin
        translate([0, -shell_len/2 + 80, -70])
            scale([0.5, 0.7, 0.45])
                sphere(r = 60);
    }
}

module shell_cavity() {
    // Wearer + VR bay void
    hull() {
        translate([0, 25, 20])
            scale([
                (shell_w/2) - shell_wall - 8,
                shell_len*0.28,
                shell_h*0.34
            ]) sphere(r = 1);
        translate([0, -20, -15])
            scale([70, 60, 55]) sphere(r = 1);
        translate([0, -shell_len/2 + 70, -25])
            scale([45, 50, 40]) sphere(r = 1);
    }
}

module neck_opening() {
    translate([0, shell_len/2 - 20, -shell_h/2 + 40])
        rotate([70, 0, 0])
            scale([neck_opening_w/2, neck_opening_d/2, 40])
                cylinder(r = 1, h = 1, center = true);
}

module world_camera_pocket(side = 1, elevation = 1) {
    // elevation: +1 upper, -1 lower (Quest-style 4-camera array)
    x = side * world_cam_lateral;
    y = -world_cam_forward + (elevation > 0 ? 10 : -5);
    z = elevation * world_cam_vertical;
    translate([x, y, z])
    rotate([world_cam_down_angle * (elevation > 0 ? 1 : -0.3), 0, side * 35]) {
        cube([quest_cam_w + 0.4, quest_cam_d + 0.4, quest_cam_h + 0.4], center = true);
        // flex exit toward cranial cavity
        translate([-side * quest_cam_flex_len/2, quest_cam_d/2, 0])
            cube([quest_cam_flex_len, quest_cam_flex_h + 0.4, quest_cam_flex_w + 0.4], center = true);
        // outer aperture (keep small so fur can hide it)
        translate([0, -quest_cam_d/2 - 2, 0])
            rotate([90, 0, 0])
                cylinder(d = 4.5, h = 8, center = true);
    }
}

module cooling_apertures() {
    // Cheek intakes (left/right) — draw cool air across face foam
    for (s = [-1, 1])
        translate([s * (shell_w/2 - 18), -10, -25])
            rotate([0, 90, 0])
                hull() {
                    translate([0, -12, 0]) cylinder(d = intake_slot_h, h = 20, center = true);
                    translate([0,  12, 0]) cylinder(d = intake_slot_h, h = 20, center = true);
                }
    // Snout secondary intake (mesh behind nose)
    translate([0, -shell_len/2 + 40, -15])
        rotate([90, 0, 0])
            for (x = [-15, 0, 15])
                translate([x, 0, 0])
                    cylinder(d = 8, h = 30, center = true);
    // Cranial exhaust (top of head) — hot electronics + wearer air out
    translate([0, 40, shell_h/2 - 25])
        for (x = [-25, 0, 25])
            translate([x, 0, 0])
                cylinder(d = 14, h = 30, center = true);
    // Occiput / neck exhaust assist
    translate([0, shell_len/2 - 45, 10])
        rotate([90, 0, 0])
            hull() {
                translate([-20, 0, 0]) cylinder(d = exhaust_slot_h, h = 25, center = true);
                translate([ 20, 0, 0]) cylinder(d = exhaust_slot_h, h = 25, center = true);
            }
}

module fan_mount_bosses() {
    // Dual 40mm axial fans at cranial exhaust plenum
    for (x = [-30, 30])
        translate([x, 35, shell_h/2 - 55]) {
            difference() {
                cube([fan_40 + 6, fan_40 + 6, 4], center = true);
                cylinder(d = fan_40_hole, h = 6, center = true);
                for (a = [-1, 1], b = [-1, 1])
                    translate([a*fan_screw_pitch/2, b*fan_screw_pitch/2, 0])
                        m3_hole(10);
            }
        }
}

module decoration_boss_field() {
    // Glue / screw pads so makers can attach foam, fur, ears, horns, etc.
    positions = [
        [0, -shell_len/2 + 50, 30],          // snout bridge
        [-90, 0, 40], [90, 0, 40],           // cheeks
        [-60, 40, 90], [60, 40, 90],         // brow / ear roots
        [0, 80, 100],                        // crown
        [-70, 70, 20], [70, 70, 20],         // occiput sides
        [0, -20, -90]                        // chin
    ];
    for (p = positions)
        translate(p) decoration_boss();
}

module shell_outer(cutaway = false) {
    difference() {
        shell_envelope();
        shell_cavity();
        neck_opening();
        cooling_apertures();
        // VR bay registration pocket (mates with optical chassis)
        translate([0, -5, 5])
            cube([chassis_w + 1, chassis_h + 1, chassis_d + 1], center = true);
        // world cameras
        for (s = [-1, 1], e = [-1, 1])
            world_camera_pocket(s, e);
        if (cutaway)
            translate([0, -200, -200])
                cube([200, 400, 400]);
    }
    fan_mount_bosses();
    decoration_boss_field();
}

shell_outer();
