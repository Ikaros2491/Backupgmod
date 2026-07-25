// Full assembly preview (not for printing as one piece)
include <params.scad>
use <shell_outer.scad>
use <optical_chassis.scad>
use <cooling_ducts.scad>
use <face_interface.scad>

/* [Preview] */
cutaway = true;
explode = 0; // [0:0.5:40]
show_cooling = true;
show_face_plate = true;

module assembly() {
    color("Tan", 0.85)
        shell_outer(cutaway = cutaway);

    color("SlateGray", 0.95)
        translate([0, -5 - explode*0.2, 5])
            optical_chassis_assembly(ipd = ipd_nominal, explode = explode*0.15);

    if (show_face_plate)
        color("Gray", 0.9)
            translate([0, -5, 5 - chassis_d/2 - face_plate_t/2 - explode*0.4])
                rotate([0, 0, 0])
                    face_interface_plate();

    if (show_cooling)
        color("SteelBlue", 0.55)
            translate([0, 0, explode*0.1])
                cooling_assembly(show_airflow = true);
}

assembly();
