// =============================================================================
// Base hollow mask — blank only
// Nothing mounted: no cameras, fans, bosses, ducts, or VR cutouts.
// Use this as the starting shell for craft / further hard-surface work.
// Units: mm
// =============================================================================

$fn = 96;

// Overall size (snout tip → occiput, temple width, crown height)
mask_len = 280;
mask_w   = 220;
mask_h   = 240;
wall     = 3.0;

// Neck opening
neck_w = 140;
neck_d = 115;

module outer_form() {
    hull() {
        // cranial bulb
        translate([0, 35, 45])
            scale([mask_w * 0.48, mask_len * 0.32, mask_h * 0.40])
                sphere(r = 1);
        // cheeks
        for (s = [-1, 1])
            translate([s * 72, 8, -5])
                scale([0.95, 1.15, 1.05])
                    sphere(r = 68);
        // snout
        translate([0, -mask_len/2 + 58, -18])
            rotate([14, 0, 0])
                scale([0.52, 1.05, 0.52])
                    sphere(r = 72);
        // chin / jaw
        translate([0, -mask_len/2 + 85, -68])
            scale([0.48, 0.72, 0.48])
                sphere(r = 58);
        // brow ridge mass (soft, no features)
        translate([0, -10, 55])
            scale([0.70, 0.45, 0.35])
                sphere(r = 70);
    }
}

module inner_void() {
    // Same silhouette, inset roughly by wall thickness
    hull() {
        translate([0, 35, 45])
            scale([
                mask_w * 0.48 - wall,
                mask_len * 0.32 - wall,
                mask_h * 0.40 - wall
            ]) sphere(r = 1);
        for (s = [-1, 1])
            translate([s * 72, 8, -5])
                scale([0.95, 1.15, 1.05])
                    sphere(r = 68 - wall);
        translate([0, -mask_len/2 + 58, -18])
            rotate([14, 0, 0])
                scale([0.52, 1.05, 0.52])
                    sphere(r = 72 - wall);
        translate([0, -mask_len/2 + 85, -68])
            scale([0.48, 0.72, 0.48])
                sphere(r = 58 - wall);
        translate([0, -10, 55])
            scale([0.70, 0.45, 0.35])
                sphere(r = 70 - wall);
    }
}

module neck_cut() {
    // Open bottom-rear for the neck — only opening in the blank
    translate([0, mask_len/2 - 10, -mask_h/2 + 50])
        rotate([65, 0, 0])
            scale([neck_w/2, neck_d/2, 1])
                cylinder(r = 1, h = 90, center = true);
}

module base_mask() {
    difference() {
        outer_form();
        inner_void();
        neck_cut();
    }
}

base_mask();
