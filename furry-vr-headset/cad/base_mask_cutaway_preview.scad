use <base_mask.scad>

// Preview helper — not for printing
difference() {
    base_mask();
    translate([0, -250, -250])
        cube([250, 500, 500]);
}
