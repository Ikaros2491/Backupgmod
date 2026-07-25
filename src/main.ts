import "./styles.css";
import * as THREE from "three";
import { VRButton } from "three/addons/webxr/VRButton.js";
import { createWorld } from "./world/scene";
import { createControllerRigs } from "./xr/controllers";
import { updateGrabAndTeleport, type InteractionState } from "./xr/interaction";
import { createDesktopControls } from "./desktop/controls";
import { supportsSession } from "./xr/session";

function requireElement<T extends Element>(selector: string): T {
  const element = document.querySelector<T>(selector);
  if (!element) {
    throw new Error(`Missing required DOM node: ${selector}`);
  }
  return element;
}

const canvas = requireElement<HTMLCanvasElement>("#xr-canvas");
const enterVrButton = requireElement<HTMLButtonElement>("#enter-vr");
const enterArButton = requireElement<HTMLButtonElement>("#enter-ar");
const statusEl = requireElement<HTMLParagraphElement>("#status");

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: false,
  powerPreference: "high-performance",
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.xr.enabled = true;

const { scene, floor, grabables, teleportTarget } = createWorld();

const camera = new THREE.PerspectiveCamera(
  70,
  window.innerWidth / window.innerHeight,
  0.05,
  100,
);
camera.position.set(0, 1.6, 3);

const playerRig = new THREE.Group();
playerRig.name = "player-rig";
playerRig.add(camera);
scene.add(playerRig);

const rigs = createControllerRigs(renderer, playerRig);
const interactionState: InteractionState = { highlighted: null };
const desktop = createDesktopControls(camera, canvas);
const clock = new THREE.Clock();

function setStatus(message: string): void {
  statusEl.textContent = message;
}

async function refreshSessionSupport(): Promise<void> {
  if (!navigator.xr) {
    enterVrButton.disabled = true;
    enterArButton.disabled = true;
    enterVrButton.textContent = "WebXR unavailable";
    enterArButton.textContent = "AR unavailable";
    setStatus("This browser has no WebXR. Use desktop WASD + drag, or open in a VR browser.");
    return;
  }

  const [vr, ar] = await Promise.all([
    supportsSession("immersive-vr"),
    supportsSession("immersive-ar"),
  ]);

  enterVrButton.disabled = !vr;
  enterArButton.disabled = !ar;
  enterVrButton.textContent = vr ? "Enter VR" : "VR not supported";
  enterArButton.textContent = ar ? "Enter AR" : "AR not supported";

  if (vr) {
    setStatus("Headset ready. Enter VR, then grab objects or teleport with the stick.");
  } else if (ar) {
    setStatus("AR supported on this device. Desktop preview still available.");
  } else {
    setStatus("No immersive session here — explore with mouse look and WASD.");
  }
}

async function startSession(mode: XRSessionMode): Promise<void> {
  if (!navigator.xr) return;
  const session = await navigator.xr.requestSession(mode, {
    requiredFeatures: ["local-floor"],
    optionalFeatures: ["bounded-floor", "hand-tracking", "layers"],
  });
  await renderer.xr.setSession(session);
  document.body.classList.add("xr-presenting");
  setStatus(mode === "immersive-vr" ? "VR session active" : "AR session active");

  session.addEventListener("end", () => {
    document.body.classList.remove("xr-presenting");
    void refreshSessionSupport();
  });
}

enterVrButton.addEventListener("click", () => {
  void startSession("immersive-vr").catch((error: unknown) => {
    console.error(error);
    setStatus("Could not start VR session. Check headset connection and permissions.");
  });
});

enterArButton.addEventListener("click", () => {
  void startSession("immersive-ar").catch((error: unknown) => {
    console.error(error);
    setStatus("Could not start AR session on this device.");
  });
});

// Keep Three's helper button available for debugging / alternate entry.
const hiddenVrButton = VRButton.createButton(renderer);
hiddenVrButton.style.display = "none";
document.body.appendChild(hiddenVrButton);

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

renderer.setAnimationLoop(() => {
  const delta = clock.getDelta();
  const elapsed = clock.elapsedTime;

  if (!renderer.xr.isPresenting) {
    desktop.update(delta);
  }

  for (const object of grabables) {
    if (object.name === "orb") {
      object.position.y = 0.7 + Math.sin(elapsed * 2) * 0.05;
    } else if (object.name === "crystal") {
      object.rotation.y += delta * 0.8;
      object.rotation.x += delta * 0.35;
    }
  }

  updateGrabAndTeleport({
    rigs,
    grabables,
    floor,
    teleportTarget,
    playerRig,
    state: interactionState,
  });

  renderer.render(scene, camera);
});

void refreshSessionSupport();
