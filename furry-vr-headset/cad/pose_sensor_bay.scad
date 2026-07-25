// In-shell pose sensor bay — magnetic capsule + optional UWB tag
// Fully internal: no exterior windows; works under buyer fur/foam/craft
include <params.scad>

module mag_sensor_cradle() {
    difference() {
        rounded_box([mag_sensor_w + 8, mag_sensor_d + 8, mag_sensor_h + 6], r = 2, center = true);
        cube([mag_sensor_w + 0.4, mag_sensor_d + 0.4, mag_sensor_h + 0.4], center = true);
        // cable exit toward electronics bay (-Y)
        translate([0, -(mag_sensor_d/2 + 2), 0])
            cube([8, 6, 5], center = true);
        for (x = [- (mag_sensor_w/2 + 2), mag_sensor_w/2 + 2])
            translate([x, 0, 0]) m3_hole(16);
    }
}

module uwb_module_cradle() {
    difference() {
        rounded_box([uwb_module_w + 6, uwb_module_d + 6, uwb_module_h + 6], r = 2, center = true);
        cube([uwb_module_w + 0.4, uwb_module_d + 0.4, uwb_module_h + 0.4], center = true);
        // antenna keep-clear notch (no solid plastic tight over chip antenna)
        translate([uwb_module_w/2 - 2, uwb_module_d/2 + 1, 0])
            cube([10, 4, uwb_module_h], center = true);
        for (x = [-10, 10])
            translate([x, 0, 0]) m3_hole(16);
    }
}

module pose_bay_tray() {
    // Tray screws into occiput of shell; holds mag + UWB + cable clips
    difference() {
        union() {
            rounded_box([pose_bay_w, pose_bay_d, pose_bay_h], r = 3, center = true);
            // shell mount flanges
            for (x = [-pose_bay_w/2 - 4, pose_bay_w/2 + 4])
                translate([x, 0, -pose_bay_h/2 + 3])
                    cube([12, pose_bay_d - 4, 6], center = true);
        }
        // hollow
        rounded_box([
            pose_bay_w - 4,
            pose_bay_d - 4,
            pose_bay_h - 4
        ], r = 2, center = true);
        // open toward electronics (-Y) for cable loom
        translate([0, -pose_bay_d/2, 0])
            cube([pose_bay_w - 16, 6, pose_bay_h - 12], center = true);
        // flange screw holes
        for (x = [-pose_bay_w/2 - 4, pose_bay_w/2 + 4])
            translate([x, 0, -pose_bay_h/2 + 3])
                m3_hole(20);
    }

    // cradles seated in tray
    translate([-12, 0, 2]) mag_sensor_cradle();
    translate([14, 0, 2]) uwb_module_cradle();
}

module pose_keepout_marker() {
    // Print-in-place or separate sticker guide for decorators
    difference() {
        cylinder(r = pose_keepout_r, h = 0.8);
        translate([0, 0, -0.1])
            cylinder(r = pose_keepout_r - 2, h = 1);
    }
    // text substitute: triangular "no steel" pips
    for (a = [0:120:240])
        rotate([0, 0, a])
            translate([pose_keepout_r - 8, 0, 0.4])
                cylinder(d = 3, h = 0.8, center = true);
}

module pose_sensor_bay_kit() {
    pose_bay_tray();
    translate([0, 50, 0]) pose_keepout_marker();
}

pose_sensor_bay_kit();
