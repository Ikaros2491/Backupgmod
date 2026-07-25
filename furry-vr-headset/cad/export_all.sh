#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
STL_DIR="$(cd "$ROOT/../stl" && pwd)"
mkdir -p "$STL_DIR"

parts=(
  "optical_chassis.scad:optical_chassis.stl"
  "shell_outer.scad:shell_outer.stl"
  "cooling_ducts.scad:cooling_ducts.stl"
  "face_interface.scad:face_interface.stl"
  "camera_mounts.scad:camera_mounts.stl"
)

for entry in "${parts[@]}"; do
  src="${entry%%:*}"
  dst="${entry##*:}"
  echo "Exporting $src -> $dst"
  openscad -o "$STL_DIR/$dst" "$ROOT/$src"
done

echo "Done. STLs in $STL_DIR"
