// Camera pockets and adapter plates for Quest-harvested and OTS modules
include <params.scad>

module quest_camera_cradle() {
    // Holds a harvested Quest 2/3 tracking camera module
    difference() {
        cube([quest_cam_w + 4, quest_cam_d + 6, quest_cam_h + 4], center = true);
        cube([quest_cam_w + 0.35, quest_cam_d + 0.35, quest_cam_h + 0.35], center = true);
        // flex escape
        translate([0, quest_cam_d/2 + 1, 0])
            cube([quest_cam_flex_w + 0.4, 4, quest_cam_flex_h + 0.4], center = true);
        // retention screw
        translate([0, 0, quest_cam_h/2 + 1])
            cylinder(d = m2_clear, h = 8, center = true);
    }
}

module ots_gs_camera_adapter() {
    // Adapts a 24x24 OTS OV7251/OV9282 board into the Quest pocket footprint
    difference() {
        union() {
            cube([ots_gs_cam_w + 4, ots_gs_cam_d + 4, ots_gs_cam_h + 4], center = true);
            // locator pegs matching shell pocket
            translate([0, -ots_gs_cam_d/2 - 2, 0])
                cube([quest_cam_w, 3, quest_cam_h], center = true);
        }
        cube([ots_gs_cam_w + 0.4, ots_gs_cam_d + 0.4, ots_gs_cam_h + 0.4], center = true);
        // lens bore
        rotate([90, 0, 0])
            cylinder(d = 8, h = 30, center = true);
        for (x = [-8, 8], z = [-8, 8])
            translate([x, 0, z])
                rotate([90, 0, 0])
                    cylinder(d = m2_clear, h = 20, center = true);
    }
}

module ir_face_camera_bracket() {
    // EyeTrackVR / Project Babble style 8.5mm IR camera
    difference() {
        cube([ir_cam_w + 8, ir_cam_d + 6, ir_cam_h + 8], center = true);
        cube([ir_cam_w + 0.3, ir_cam_d + 0.3, ir_cam_h + 0.3], center = true);
        rotate([90, 0, 0])
            cylinder(d = 5, h = 20, center = true);
        for (x = [- (ir_cam_w/2 + 2), ir_cam_w/2 + 2])
            translate([x, 0, 0])
                m3_hole(16);
    }
}

module camera_mount_kit() {
    translate([-40, 0, 0]) quest_camera_cradle();
    translate([0, 0, 0]) ots_gs_camera_adapter();
    translate([45, 0, 0]) ir_face_camera_bracket();
    // print 4x quest cradles, 2x eye IR, 1-2x mouth IR
}

camera_mount_kit();
