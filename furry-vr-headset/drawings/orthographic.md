# Orthographic blueprint sheets

Units: mm. Origin at optical midpoint. Views are schematic callouts matching `cad/assembly.scad`.

## Sheet 1 — Side section (XR)

```
                        cranial exhaust Ø14 x3
                              ↑ fans
     ┌────────────────────────┴─────────────────────────┐
     │                 electronics bay                   │
     │     ┌──────────┐     ┌──────── optical ──────┐   │
     │     │ battery  │     │  pancake+OLED module  │   │
     │     │  +3010   │     │        IPD rails      │   │
     │     └──────────┘     └───────────┬───────────┘   │
     │  occiput                         │ face plate    │
     │  exhaust                         ▼ foam gasket   │
     │                                 (wearer)         │
     │         cheek intake -> face-wash plenum         │
     │                       \                          │
     │                        \ snout mesh intake       │
     └─────────────────────────\────────────────────────┘
           Y+ occiput           \        snout Y-
```

## Sheet 2 — Front (looking at wearer)

```
     [-world cam-]                 [-world cam-]
            \                         /
             \     brow bosses       /
              \         │           /
     cheek     ┌────────┴────────┐     cheek
     intake ══ │  lens   lens    │ ══ intake
               │  L      R       │
               │    mouth cam    │
               └────────┬────────┘
                     chin boss

     Lens centers at ± IPD/2 (nom ±32)
     World cams at X=±85, Z=±35 (approx)
```

## Sheet 3 — Top

```
                 exhaust fans @ X=±30
                      ○     ○
           ┌────────────────────────┐
           │      electronics       │
   cam ○───│────────────────────────│───○ cam
           │   L optic    R optic   │
           │◄──── IPD 56–72 ───────►│
           └────────────┬───────────┘
                        │
                     snout
                   intakes
```

## Sheet 4 — Fastener map

| Joint | Hardware |
|-------|----------|
| Face plate → chassis | 4× M3×12 |
| Optic module → carrier | 4× M3×6 per eye |
| Chassis → shell bosses | 4× M3×10 |
| Fan → shroud | 4× M3×12 per fan |
| Camera cradles | M2×6 |
| Decoration bosses | M3 or #4 wood screw into boss ID 3.2 |

## Revision block

| Rev | Date | Notes |
|-----|------|-------|
| A | 2026-07-25 | Initial prototype package — SeeYa pancake + Quest-class cams + ducted shell |
