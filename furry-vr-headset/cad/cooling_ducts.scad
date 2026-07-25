// Active cooling ducting: cheek intake → face wash → electronics bay → cranial exhaust
include <params.scad>

module duct_tube(path_len, od = 22, id = 18) {
    difference() {
        cylinder(d = od, h = path_len);
        translate([0, 0, -0.1])
            cylinder(d = id, h = path_len + 0.2);
    }
}

module cheek_intake_scoop(side = 1) {
    // Flares from outer cheek grill into soft face-wash plenum
    mirror([side < 0 ? 1 : 0, 0, 0])
    difference() {
        hull() {
            translate([shell_w/2 - 25, -10, -25])
                rotate([0, 90, 0])
                    cube([intake_slot_h + 6, intake_slot_w * 0.55, 4], center = true);
            translate([55, -5, -10])
                cube([20, 40, 24], center = true);
        }
        hull() {
            translate([shell_w/2 - 25, -10, -25])
                rotate([0, 90, 0])
                    cube([intake_slot_h, intake_slot_w * 0.45, 6], center = true);
            translate([55, -5, -10])
                cube([16, 34, 18], center = true);
        }
    }
}

module face_wash_plenum() {
    // Distributes cool air across brow / cheeks / mouth foam channel
    difference() {
        rounded_box([face_plate_w - 10, 28, 70], r = 4, center = true);
        rounded_box([face_plate_w - 18, 20, 62], r = 3, center = true);
        // exit slots toward face foam
        for (x = [-60, -30, 0, 30, 60])
            translate([x, -14, 0])
                cube([10, 8, 40], center = true);
        // entries from cheek scoops
        for (s = [-1, 1])
            translate([s * 70, 0, -10])
                rotate([0, 90, 0])
                    cylinder(d = 16, h = 20, center = true);
    }
}

module electronics_bay_shroud() {
    // Pulls air across display driver boards / MCU / battery
    difference() {
        translate([0, 25, 35])
            rounded_box([120, 70, 50], r = 5, center = true);
        translate([0, 25, 35])
            rounded_box([112, 62, 42], r = 4, center = true);
        // inlet from face plenum
        translate([0, -5, 10])
            cube([40, 20, 20], center = true);
        // outlet to fans
        translate([0, 25, 60])
            cube([80, 50, 10], center = true);
    }
}

module exhaust_fan_shroud() {
    for (x = [-30, 30])
        translate([x, 35, shell_h/2 - 55]) {
            difference() {
                cube([fan_40 + 8, fan_40 + 8, fan_40_thick + 6], center = true);
                cylinder(d = fan_40_hole, h = fan_40_thick + 8, center = true);
                // top exit
                translate([0, 0, fan_40_thick/2 + 2])
                    cube([fan_40 - 4, fan_40 - 4, 6], center = true);
                for (a = [-1, 1], b = [-1, 1])
                    translate([a*fan_screw_pitch/2, b*fan_screw_pitch/2, 0])
                        m3_hole(20);
            }
        }
}

module blower_battery_duct() {
    // Optional 3010 blower dedicated to battery pack under occiput
    translate([0, shell_len/2 - 70, -20])
    difference() {
        cube([blower_3010_w + 6, blower_3010_h + 6, blower_3010_d + 8], center = true);
        cube([blower_3010_w + 0.4, blower_3010_h + 0.4, blower_3010_d + 0.4], center = true);
        translate([0, blower_3010_h/2, 0])
            cube([16, 10, 12], center = true);
    }
}

module cooling_assembly(show_airflow = true) {
    cheek_intake_scoop(1);
    cheek_intake_scoop(-1);
    translate([0, -35, -5]) face_wash_plenum();
    electronics_bay_shroud();
    exhaust_fan_shroud();
    blower_battery_duct();

    if (show_airflow) {
        color("Cyan", 0.25) {
            // schematic airflow ribbons (not printed)
            hull() {
                translate([shell_w/2 - 20, -10, -25]) sphere(3);
                translate([40, -30, -5]) sphere(3);
            }
            hull() {
                translate([-shell_w/2 + 20, -10, -25]) sphere(3);
                translate([-40, -30, -5]) sphere(3);
            }
            hull() {
                translate([0, -30, 5]) sphere(3);
                translate([0, 25, 35]) sphere(4);
            }
            hull() {
                translate([0, 25, 50]) sphere(4);
                translate([0, 40, shell_h/2 - 30]) sphere(5);
            }
        }
    }
}

// Airflow ribbons are preview-only; omit from STL exports
cooling_assembly(show_airflow = false);
