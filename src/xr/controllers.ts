import * as THREE from "three";
import { XRControllerModelFactory } from "three/addons/webxr/XRControllerModelFactory.js";

export type ControllerRig = {
  controller: THREE.XRTargetRaySpace;
  grip: THREE.XRGripSpace;
  ray: THREE.Line;
  holding: THREE.Object3D | null;
  squeeze: boolean;
  gamepad: Gamepad | null;
  inputSource: XRInputSource | null;
};

function createRayLine(): THREE.Line {
  const geometry = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(0, 0, -1),
  ]);
  const material = new THREE.LineBasicMaterial({
    color: 0x3ecf8e,
    transparent: true,
    opacity: 0.7,
  });
  const line = new THREE.Line(geometry, material);
  line.scale.z = 4;
  line.name = "pointer-ray";
  return line;
}

export function createControllerRigs(
  renderer: THREE.WebGLRenderer,
  parent: THREE.Object3D,
): ControllerRig[] {
  const factory = new XRControllerModelFactory();
  const rigs: ControllerRig[] = [];

  for (let i = 0; i < 2; i += 1) {
    const controller = renderer.xr.getController(i);
    const grip = renderer.xr.getControllerGrip(i);
    const ray = createRayLine();

    controller.add(ray);
    grip.add(factory.createControllerModel(grip));
    parent.add(controller);
    parent.add(grip);

    const rig: ControllerRig = {
      controller,
      grip,
      ray,
      holding: null,
      squeeze: false,
      gamepad: null,
      inputSource: null,
    };

    controller.addEventListener("selectstart", () => {
      rig.squeeze = true;
    });
    controller.addEventListener("selectend", () => {
      rig.squeeze = false;
    });
    controller.addEventListener("connected", (event) => {
      const inputSource = (event as THREE.Event & { data: XRInputSource }).data;
      rig.inputSource = inputSource;
      rig.gamepad = inputSource.gamepad ?? null;
      rig.ray.visible = inputSource.targetRayMode === "tracked-pointer";
    });
    controller.addEventListener("disconnected", () => {
      rig.ray.visible = false;
      rig.squeeze = false;
      rig.gamepad = null;
      rig.inputSource = null;
    });

    rigs.push(rig);
  }

  return rigs;
}
