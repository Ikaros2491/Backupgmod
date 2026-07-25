# VR Prototype

WebXR playground for rapid VR interaction experiments. Built with **Vite**, **TypeScript**, and **Three.js**.

## What’s included

- Immersive VR session entry (WebXR) with optional AR when the device supports it
- Tracked controllers with pointer rays
- Grab interaction on sandbox objects (trigger / select)
- Thumbstick teleport across the play floor
- Desktop fallback: click-drag look + WASD move

## Quick start

```bash
npm install
npm run dev
```

Open the local URL Vite prints (usually `http://localhost:5173`).

### Headset testing

WebXR needs a **secure context** (`https://` or `localhost`).

1. Put on a WebXR-capable headset browser (Meta Quest Browser, Chrome on connected PC, etc.).
2. Open the dev server URL.
3. Press **Enter VR**.

For LAN testing from a headset, run:

```bash
npm run dev -- --host 0.0.0.0
```

Then open `https://<your-machine-ip>:5173` via a trusted tunnel or local HTTPS proxy if the browser blocks plain HTTP.

## Scripts

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Vite dev server |
| `npm run build` | Typecheck + production build to `dist/` |
| `npm run preview` | Serve the production build |
| `npm run typecheck` | TypeScript only |

## Project layout

```
src/
  main.ts              App bootstrap, renderer, XR session
  world/scene.ts       Lights, floor, grabables
  xr/controllers.ts    Controller / grip rigs
  xr/interaction.ts    Grab + teleport logic
  desktop/controls.ts  Non-VR camera controls
archives/
  gmod-backup.zip      Legacy Garry’s Mod backup assets (unrelated runtime)
```

## Prototype goals

This repo is a clean workspace for VR experiments — locomotion, interaction, and scene composition — without shipping a full game framework. Extend `src/world/scene.ts` for content and `src/xr/interaction.ts` for input behaviors.

## Notes

- `archives/gmod-backup.zip` preserves older GMod PAC3 / PPM2 / vComputer drafts from the previous dump and is not loaded by the prototype.
- Desktop mode is for layout and iteration; validate feel on a real headset before trusting interaction timing.
