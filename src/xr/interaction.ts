import * as THREE from "three";
import type { ControllerRig } from "./controllers";

const _origin = new THREE.Vector3();
const _direction = new THREE.Vector3();
const _matrix = new THREE.Matrix4();
const _hitPoint = new THREE.Vector3();
const _worldPos = new THREE.Vector3();
const _localOffset = new THREE.Vector3();

export type InteractionState = {
  highlighted: THREE.Object3D | null;
};

function setHighlight(object: THREE.Object3D | null, active: boolean): void {
  if (!object || !(object instanceof THREE.Mesh)) return;
  const material = object.material;
  if (Array.isArray(material) || !(material instanceof THREE.MeshStandardMaterial)) {
    return;
  }
  material.emissiveIntensity = active ? 1.4 : 1;
  material.emissive = active
    ? new THREE.Color(0xffffff).multiplyScalar(0.18)
    : new THREE.Color(material.color).multiplyScalar(0.08);
}

export function updateGrabAndTeleport(options: {
  rigs: ControllerRig[];
  grabables: THREE.Object3D[];
  floor: THREE.Object3D;
  teleportTarget: THREE.Mesh;
  playerRig: THREE.Group;
  state: InteractionState;
}): void {
  const { rigs, grabables, floor, teleportTarget, playerRig, state } = options;
  const raycaster = new THREE.Raycaster();
  let nextHighlight: THREE.Object3D | null = null;
  let showTeleport = false;

  for (const rig of rigs) {
    _matrix.identity().extractRotation(rig.controller.matrixWorld);
    _origin.setFromMatrixPosition(rig.controller.matrixWorld);
    _direction.set(0, 0, -1).applyMatrix4(_matrix).normalize();
    raycaster.set(_origin, _direction);

    if (rig.holding) {
      rig.controller.getWorldPosition(_worldPos);
      _localOffset.set(0, 0, -0.15).applyMatrix4(_matrix);
      rig.holding.position.copy(_worldPos).add(_localOffset);
      rig.holding.quaternion.setFromRotationMatrix(_matrix);

      if (!rig.squeeze) {
        rig.holding = null;
      }
      continue;
    }

    const hits = raycaster.intersectObjects(grabables, false);
    const hit = hits[0]?.object ?? null;

    if (hit?.userData.grabbable) {
      nextHighlight = hit;
      rig.ray.scale.z = Math.max(hits[0].distance, 0.2);
      if (rig.squeeze) {
        rig.holding = hit;
      }
    } else {
      const floorHits = raycaster.intersectObject(floor, false);
      if (floorHits[0]) {
        _hitPoint.copy(floorHits[0].point);
        teleportTarget.position.set(_hitPoint.x, 0.02, _hitPoint.z);
        showTeleport = true;
        rig.ray.scale.z = Math.max(floorHits[0].distance, 0.2);

        const axes = rig.gamepad?.axes ?? rig.inputSource?.gamepad?.axes ?? [];
        // Common WebXR mapping: axes[2]/axes[3] are thumbstick X/Y.
        const forward = axes[3] ?? axes[1] ?? 0;
        if (forward < -0.65) {
          playerRig.position.x = _hitPoint.x;
          playerRig.position.z = _hitPoint.z;
        }
      } else {
        rig.ray.scale.z = 4;
      }
    }
  }

  if (state.highlighted !== nextHighlight) {
    setHighlight(state.highlighted, false);
    setHighlight(nextHighlight, true);
    state.highlighted = nextHighlight;
  }

  teleportTarget.visible = showTeleport;
}
