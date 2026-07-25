// Soft-goods interface plate between optical chassis and wearer foam
include <params.scad>

module face_interface_plate() {
    difference() {
        rounded_box([face_plate_w, face_plate_h, face_plate_t], r = 10, center = true);

        // binocular viewing apertures
        for (s = [-1, 1])
            translate([s * ipd_nominal/2, 8, 0])
                cylinder(d = optic_lens_od + 4, h = face_plate_t + 2, center = true);

        // nose bridge relief
        translate([0, -face_plate_h/2 + nose_bridge_cut_h/2, 0])
            cube([nose_bridge_cut_w, nose_bridge_cut_h, face_plate_t + 2], center = true);

        // foam retention channel (glue EVA / scuba foam into this groove)
        difference() {
            rounded_box([
                face_plate_w - 6,
                face_plate_h - 6,
                1.2
            ], r = 8, center = true);
            rounded_box([
                face_plate_w - 6 - 2*foam_channel_w,
                face_plate_h - 6 - 2*foam_channel_w,
                2
            ], r = 6, center = true);
        }

        // mount to optical chassis
        for (x = [-70, 70], y = [-40, 40])
            translate([x, y, 0]) m3_hole(10);

        // IR LED ring holes around each eye (850 nm)
        for (s = [-1, 1])
            for (a = [0:60:300])
                translate([s * ipd_nominal/2, 8, 0])
                    rotate([0, 0, a])
                        translate([optic_lens_od/2 + 3, 0, 0])
                            cylinder(d = ir_led_od, h = face_plate_t + 2, center = true);

        // lower face camera window
        translate([0, mouth_cam_y + 40, 0])
            cube([ir_cam_w + 2, ir_cam_h + 2, face_plate_t + 2], center = true);
    }
}

module foam_guide_ring() {
    // Optional printed guide for cutting face foam
    difference() {
        rounded_box([face_plate_w + 4, face_plate_h + 4, 1], r = 11, center = true);
        for (s = [-1, 1])
            translate([s * ipd_nominal/2, 8, 0])
                cylinder(d = optic_lens_od + 6, h = 3, center = true);
        translate([0, -face_plate_h/2 + nose_bridge_cut_h/2, 0])
            cube([nose_bridge_cut_w + 4, nose_bridge_cut_h + 2, 3], center = true);
    }
}

face_interface_plate();
