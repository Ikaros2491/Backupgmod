// Optical chassis: dual pancake modules, IPD rails, face-plate interface
include <params.scad>

module optic_pocket(cut = true) {
    // Pocket for one SeeYa pancake + display module
    cube([optic_w + 0.4, optic_h + 0.4, optic_d + 0.4], center = true);
}

module optic_mount_plate() {
    difference() {
        cube([optic_w + 12, optic_h + 12, 3], center = true);
        optic_pocket();
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (optic_w/2 + 3), y * (optic_h/2 + 3), 0])
                m3_hole(10);
    }
}

module ipd_carrier(side = 1) {
    // side: -1 left eye, +1 right eye (wearer perspective)
    difference() {
        union() {
            translate([0, 0, chassis_d/2 - 8])
                cube([optic_w + 16, optic_h + 16, 6], center = true);
            // rail shoes
            for (y = [-chassis_h/2 + 10, chassis_h/2 - 10])
                translate([0, y, 8])
                    cube([18, 10, 8], center = true);
        }
        translate([0, 0, chassis_d/2 - optic_d/2 - 2])
            optic_pocket();
        // IPD rail holes (smooth M3 rods)
        for (y = [-chassis_h/2 + 10, chassis_h/2 - 10])
            rotate([0, 90, 0])
                translate([-8, y, 0])
                    cylinder(d = 3.2, h = 40, center = true);
        // lead-screw nut pocket (M3 threaded rod adjuster)
        translate([0, -chassis_h/2 + 22, 8])
            cube([6.2, 6.2, 10], center = true);
    }
    // visual: lens aperture marker
    color("DeepSkyBlue", 0.35)
        translate([0, 0, chassis_d/2 - 1])
            cylinder(d = optic_lens_od - 2, h = 1);
}

module optical_chassis_frame() {
    difference() {
        rounded_box([chassis_w, chassis_h, chassis_d], r = 6, center = true);
        // hollow interior
        rounded_box([
            chassis_w - 2*chassis_wall,
            chassis_h - 2*chassis_wall,
            chassis_d - 2*chassis_wall
        ], r = 4, center = true);
        // open face toward wearer (-Z in this model: front of headset is +Z snout)
        translate([0, 0, -chassis_d/2])
            cube([chassis_w - 20, chassis_h - 16, chassis_wall + 2], center = true);
        // open front toward snout for ducting / cable exit
        translate([0, 0, chassis_d/2])
            cube([chassis_w - 40, 50, chassis_wall + 2], center = true);
        // IPD through-rods
        for (y = [-chassis_h/2 + 10, chassis_h/2 - 10])
            rotate([0, 90, 0])
                translate([-8, y, 0])
                    cylinder(d = 3.2, h = chassis_w + 4, center = true);
        // center lead screw
        rotate([0, 90, 0])
            translate([-8, -chassis_h/2 + 22, 0])
                cylinder(d = 3.2, h = chassis_w + 4, center = true);
        // face-plate screw bosses
        for (x = [-70, 70], y = [-40, 40])
            translate([x, y, -chassis_d/2])
                cylinder(d = m3_clear, h = 12, center = true);
    }
}

module optical_chassis_assembly(ipd = ipd_nominal, explode = 0) {
    half = ipd / 2;
    optical_chassis_frame();
    translate([-half - explode, 0, 0]) ipd_carrier(-1);
    translate([ half + explode, 0, 0]) ipd_carrier(1);

    // mouth / lower-face camera shelf
    color("Orange", 0.7)
    translate([0, mouth_cam_y, mouth_cam_z - 10])
        difference() {
            cube([36, 14, 10], center = true);
            cube([ir_cam_w + 0.3, ir_cam_h + 0.3, 12], center = true);
            for (x = [-12, 12])
                translate([x, 0, 0]) m3_hole(12);
        }

    // eye IR camera pockets on temporal sides
    for (s = [-1, 1])
        color("Orange", 0.7)
        translate([s * (half + eye_cam_offset_x), eye_cam_offset_y, 6])
            difference() {
                cube([ir_cam_w + 6, ir_cam_h + 6, ir_cam_d + 3], center = true);
                cube([ir_cam_w + 0.3, ir_cam_h + 0.3, ir_cam_d + 4], center = true);
            }
}

optical_chassis_assembly();
