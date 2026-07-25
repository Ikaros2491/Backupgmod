#!/usr/bin/env python3
"""Generate a simple SVG dimension blueprint for the fursuit VR shell."""
from pathlib import Path

W, H = 900, 700
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: "IBM Plex Mono", "Cascadia Code", monospace; fill: #1a1a1a; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .label {{ font-size: 12px; }}
    .dim {{ font-size: 11px; fill: #0b5; }}
    .shell {{ fill: #e8dcc8; stroke: #333; stroke-width: 2; }}
    .bay {{ fill: #9aa7b5; stroke: #222; stroke-width: 1.5; }}
    .duct {{ fill: #6ea8c8; stroke: #174; stroke-width: 1; fill-opacity: 0.55; }}
    .cam {{ fill: #e67e22; stroke: #222; }}
    .thin {{ stroke: #666; stroke-width: 1; fill: none; }}
  </style>
  <rect width="100%" height="100%" fill="#f7f3ea"/>
  <text class="title" x="24" y="36">Fursuit VR Shell — Side Blueprint (Rev A)</text>
  <text class="label" x="24" y="58">Units mm · Origin at optical midpoint · See docs/dimensions.md</text>

  <!-- Side silhouette -->
  <ellipse class="shell" cx="420" cy="320" rx="210" ry="170"/>
  <ellipse class="shell" cx="250" cy="360" rx="90" ry="70"/>
  <rect class="bay" x="330" y="260" width="170" height="90" rx="8"/>
  <rect class="duct" x="300" y="300" width="40" height="50" rx="4"/>
  <rect class="duct" x="500" y="230" width="50" height="40" rx="4"/>
  <circle class="cam" cx="280" cy="250" r="5"/>
  <circle class="cam" cx="300" cy="400" r="5"/>

  <!-- Dimension lines -->
  <path class="thin" d="M210 520 H630"/>
  <path class="thin" d="M210 510 V530 M630 510 V530"/>
  <text class="dim" x="390" y="545">shell_len 280</text>

  <path class="thin" d="M680 150 V490"/>
  <path class="thin" d="M670 150 H690 M670 490 H690"/>
  <text class="dim" x="700" y="330" transform="rotate(90 700 330)">shell_h 240</text>

  <text class="label" x="350" y="310">optical chassis 170x90x55</text>
  <text class="label" x="250" y="240">world cam</text>
  <text class="label" x="510" y="220">40mm exhaust fans</text>
  <text class="label" x="240" y="430">cheek / snout intake</text>

  <text class="label" x="24" y="640">Furry VR Headset Prototype · Blank decorateable shell · Active cooling</text>
  <text class="label" x="24" y="660">CAD: furry-vr-headset/cad/*.scad</text>
</svg>
'''

out = Path(__file__).with_name('side_blueprint.svg')
out.write_text(svg)
print(f'Wrote {out}')
