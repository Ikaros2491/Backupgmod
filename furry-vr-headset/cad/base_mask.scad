// =============================================================================
// Blank hollow HEAD-shaped mask base
// Toon/anthro head blank: round skull, cheeks, single blunt muzzle, neck hole.
// No cameras/fans/bosses. Units: mm
// +X right, +Y back, +Z up, snout -Y
// =============================================================================

$fn = 96;

module head_outer() {
    union() {
        // Skull — slightly egg-shaped, not a perfect ball
        translate([0, 25, 30])
            scale([1.1, 1.05, 1.22])
                sphere(r = 100);

        // Occiput fullness
        translate([0, 55, 25])
            scale([0.95, 0.85, 1.0])
                sphere(r = 70);

        // Cheeks
        for (s = [-1, 1])
            translate([s * 62, 5, 8])
                scale([1.0, 1.1, 1.05])
                    sphere(r = 52);

        // Brow / forehead
        translate([0, -12, 58])
            scale([1.2, 0.6, 0.55])
                sphere(r = 62);

        // SINGLE blunt muzzle (keeps width forward so it reads as a snout, not a beak)
        hull() {
            // wide root into the face
            translate([0, -32, 6])
                scale([1.1, 0.5, 1.0])
                    sphere(r = 62);
            // thick mid-snout (do not taper early)
            translate([0, -78, 2])
                scale([0.95, 0.75, 0.75])
                    sphere(r = 48);
            translate([0, -108, -2])
                scale([0.9, 0.7, 0.7])
                    sphere(r = 40);
            // blunt nose block
            translate([0, -132, -6])
                scale([0.85, 0.65, 0.6])
                    sphere(r = 30);
            // chin / lower muzzle
            translate([0, -100, -32])
                scale([0.9, 0.7, 0.55])
                    sphere(r = 36);
            // jaw rear
            translate([0, -38, -36])
                scale([1.05, 0.65, 0.55])
                    sphere(r = 52);
        }

        // Throat / neck blend into skull
        translate([0, 20, -45])
            scale([1.1, 1.0, 0.8])
                sphere(r = 58);
    }
}

module head_cavity() {
    union() {
        translate([0, 22, 28])
            scale([0.9, 0.9, 0.95])
                sphere(r = 100);
        translate([0, -30, 0])
            scale([0.72, 1.2, 0.7])
                sphere(r = 52);
        translate([0, -75, -8])
            scale([0.55, 1.05, 0.55])
                sphere(r = 40);
        translate([0, 15, -30])
            scale([0.9, 0.9, 0.75])
                sphere(r = 60);
    }
}

module neck_opening() {
    translate([0, 16, -105])
        rotate([90, 0, 0])
            scale([68, 1, 58])
                cylinder(r = 1, h = 110, center = true);
    translate([0, 14, -130])
        cube([180, 170, 60], center = true);
}

module base_mask() {
    difference() {
        head_outer();
        head_cavity();
        neck_opening();
    }
}

base_mask();
