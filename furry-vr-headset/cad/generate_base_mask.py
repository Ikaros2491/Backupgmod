#!/usr/bin/env python3
"""
Blank head-shaped hollow mask base.

Skull + cheeks + clear forward muzzle + jaw. Neck opening only at the bottom.
+X right, +Y back, +Z up, snout -Y.
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
from skimage import measure
import trimesh
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STL_PATH = ROOT / "stl" / "base_mask.stl"
SOLID_PATH = ROOT / "stl" / "base_mask_solid.stl"
RENDER_DIR = ROOT / "drawings" / "renders"
ART_DIR = Path("/opt/cursor/artifacts/furry-vr-blueprints")

# Strong, readable anthro head masses (x, y, z, r)
BALLS = [
    # Big cranial egg
    (0, 22, 30, 90),
    (0, 48, 25, 74),
    (0, 10, 68, 62),
    (0, 62, 40, 60),
    # Cheeks
    (56, 0, 8, 44),
    (-56, 0, 8, 44),
    # Brow
    (0, -20, 48, 52),
    # Face root into muzzle
    (0, -42, 18, 48),
    # Long clear muzzle
    (0, -70, 6, 36),
    (0, -98, -2, 27),
    (0, -122, -8, 18),
    (0, -138, -12, 13),
    # Jaw under muzzle
    (0, -55, -28, 36),
    (0, -88, -34, 26),
    (32, -65, -26, 20),
    (-32, -65, -26, 20),
    # Soft throat (no through-hole)
    (0, 12, -42, 42),
]


def build_field(res: int = 108):
    pad = 30
    xs_b = [b[0] for b in BALLS]
    ys_b = [b[1] for b in BALLS]
    zs_b = [b[2] for b in BALLS]
    rs = [b[3] for b in BALLS]
    rmax = max(rs)
    xmin, xmax = min(xs_b) - rmax - pad, max(xs_b) + rmax + pad
    ymin, ymax = min(ys_b) - rmax - pad, max(ys_b) + rmax + pad
    zmin, zmax = min(zs_b) - rmax - pad, max(zs_b) + rmax + pad
    xs = np.linspace(xmin, xmax, res)
    ys = np.linspace(ymin, ymax, res)
    zs = np.linspace(zmin, zmax, res)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    field = np.zeros(X.shape, np.float32)
    for cx, cy, cz, r in BALLS:
        d2 = (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 + 1e-6
        field += (r * r) / d2
    origin = np.array([xmin, ymin, zmin], dtype=np.float64)
    spacing = (
        (xmax - xmin) / (res - 1),
        (ymax - ymin) / (res - 1),
        (zmax - zmin) / (res - 1),
    )
    return field, origin, spacing


def isosurface(field, origin, spacing, level: float) -> trimesh.Trimesh:
    verts, faces, *_ = measure.marching_cubes(field, level=level, spacing=spacing)
    verts = verts + origin
    mesh = trimesh.Trimesh(vertices=verts.astype(np.float64), faces=faces, process=True)
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    mesh.fix_normals()
    return mesh


def normalize(mesh: trimesh.Trimesh, length_mm: float = 300.0) -> trimesh.Trimesh:
    mesh = mesh.copy()
    mesh.apply_scale(length_mm / mesh.extents[1])
    mesh.apply_translation(-mesh.centroid)
    mesh.apply_translation([0, 0, -mesh.bounds[0, 2]])
    return mesh


def open_neck_bottom(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Remove only the bottom neck region — do not tunnel through the head."""
    m = mesh.copy()
    # Delete faces whose centers are in the bottom neck pocket
    c = m.triangles_center
    neck = (
        (c[:, 2] < m.bounds[0, 2] + 55)
        & (np.abs(c[:, 0]) < 70)
        & (c[:, 1] > -20)
        & (c[:, 1] < 55)
    )
    m.update_faces(~neck)
    m.remove_unreferenced_vertices()
    return m


def make_meshes():
    field, origin, spacing = build_field(108)
    outer = normalize(isosurface(field, origin, spacing, 1.0))
    inner = isosurface(field, origin, spacing, 1.20)
    inner.invert()
    inner = normalize(inner)
    # Match inner scale/pose already via same normalize from same field extents — good enough
    hollow = trimesh.util.concatenate([outer, inner])
    hollow = open_neck_bottom(hollow)
    outer_open = open_neck_bottom(outer)

    print(
        f"Y snout..occiput {outer.bounds[0,1]:.1f} .. {outer.bounds[1,1]:.1f}  "
        f"extents={outer.extents.tolist()}"
    )
    snout = outer.vertices[:, 1] < outer.bounds[0, 1] + 30
    mid = np.abs(outer.vertices[:, 1] - (outer.bounds[0, 1] * 0.15)) < 25
    print(
        f"widths snout={np.ptp(outer.vertices[snout,0]):.1f} "
        f"midface={np.ptp(outer.vertices[mid,0]):.1f}"
    )
    return hollow, outer, outer_open


def render_views(outer: trimesh.Trimesh):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib.collections import PolyCollection
    from matplotlib.colors import LightSource

    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)

    faces = outer.faces[:: max(1, len(outer.faces) // 40000)]
    tris = outer.vertices[faces]
    v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
    n = np.cross(v1 - v0, v2 - v0)
    nn = np.linalg.norm(n, axis=1)
    ok = nn > 1e-10
    tris, n = tris[ok], n[ok] / nn[ok, None]
    inten = LightSource(315, 50).shade_normals(n, fraction=1.0)
    rgba = np.clip(np.array([0.95, 0.89, 0.78]) * (0.42 + 0.58 * inten[:, None]), 0, 1)
    rgba = np.hstack([rgba, np.ones((len(rgba), 1))])

    def draw3d(elev, azim, name, title):
        fig = plt.figure(figsize=(8, 8), facecolor="#141416")
        ax = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#141416")
        coll = Poly3DCollection(tris, linewidths=0)
        coll.set_facecolor(rgba)
        coll.set_edgecolor(rgba)
        ax.add_collection3d(coll)
        c = outer.bounds.mean(0)
        s = outer.extents.max() * 0.58
        ax.set_xlim(c[0] - s, c[0] + s)
        ax.set_ylim(c[1] - s, c[1] + s)
        ax.set_zlim(c[2] - s, c[2] + s)
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
        try:
            ax.set_box_aspect((1, 1, 1))
        except Exception:
            pass
        ax.set_title(title, color="w", fontsize=14)
        out = RENDER_DIR / name
        fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close(fig)
        Image.open(out).save(ART_DIR / name)
        print("Wrote", out)

    draw3d(8, -90, "cad_base_mask_front.png", "Blank base mask — front")
    draw3d(8, 0, "cad_base_mask_side.png", "Blank base mask — side")
    draw3d(20, -50, "cad_base_mask.png", "Blank base mask — iso")

    # Side silhouette from OUTER only (filled, snout left)
    proj = outer.vertices[outer.faces][:, :, [1, 2]].copy()
    proj[:, :, 0] *= -1  # -Y to the left
    fig, ax = plt.subplots(figsize=(9, 7), facecolor="#f6efe4")
    ax.set_facecolor("#f6efe4")
    ax.add_collection(PolyCollection(proj, facecolors="#c49a6c", edgecolors="none", alpha=0.95))
    ax.autoscale()
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Blank base mask — side silhouette (snout left)")
    ax.set_xlabel("← snout (−Y)     occiput (+Y) →")
    ax.set_ylabel("Z up")
    out = RENDER_DIR / "cad_base_mask_side_silhouette.png"
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    Image.open(out).save(ART_DIR / out.name)
    print("Wrote", out)


def main():
    hollow, outer, outer_open = make_meshes()
    STL_PATH.parent.mkdir(parents=True, exist_ok=True)
    hollow.export(STL_PATH)
    outer_open.export(SOLID_PATH)
    print(f"Wrote {STL_PATH} and {SOLID_PATH}")
    render_views(outer)


if __name__ == "__main__":
    main()
