// Outside-in tracker mast — mounts above the fur line (ear / horn / dorsal spike)
// Default top pad fits a Vive Tracker / Tundra-style puck (tripod bushing + pin circle)
include <params.scad>

/* [Tracker mast] */
mast_height = 90;
mast_od = 22;
mast_id = 14;                 // cable / USB pass
puck_plate_od = 55;
puck_plate_t = 4;
// HTC/Vive tracker tripod insert is 1/4-20; use heat-set or nut trap
tripod_clear = 6.5;
// Optional 3-pin style keep-outs (generic circle; verify against your puck)
pin_circle_d = 30;
pin_d = 3.2;
shell_boss_spread = 28;

module tracker_puck_plate() {
    difference() {
        cylinder(d = puck_plate_od, h = puck_plate_t);
        translate([0, 0, -0.1])
            cylinder(d = tripod_clear, h = puck_plate_t + 0.2);
        for (a = [0:120:240])
            rotate([0, 0, a])
                translate([pin_circle_d/2, 0, -0.1])
                    cylinder(d = pin_d, h = puck_plate_t + 0.2);
        // clearance note: keep fur below this plate
    }
}

module tracker_mast_tube() {
    difference() {
        union() {
            cylinder(d = mast_od, h = mast_height);
            // flare into cranial boss
            translate([0, 0, 0])
                cylinder(d1 = mast_od + 16, d2 = mast_od, h = 18);
            translate([0, 0, mast_height - puck_plate_t])
                tracker_puck_plate();
        }
        translate([0, 0, -0.1])
            cylinder(d = mast_id, h = mast_height + puck_plate_t + 0.2);
        // M3 mount to shell crown bosses
        for (a = [0:90:270])
            rotate([0, 0, a])
                translate([shell_boss_spread/2, 0, 6])
                    rotate([90, 0, 0])
                        cylinder(d = m3_clear, h = 30, center = true);
    }
}

module fur_keepout_guide() {
    // Non-printed visual / cutting guide: clear hemisphere above plate
    color("Lime", 0.15)
        translate([0, 0, mast_height])
            sphere(d = 80);
}

module tracker_mast_assembly(show_keepout = false) {
    tracker_mast_tube();
    if (show_keepout) fur_keepout_guide();
}

tracker_mast_assembly(show_keepout = false);
