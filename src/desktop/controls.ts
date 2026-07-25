import * as THREE from "three";

export type DesktopControls = {
  update: (delta: number) => void;
  dispose: () => void;
};

export function createDesktopControls(
  camera: THREE.PerspectiveCamera,
  domElement: HTMLElement,
): DesktopControls {
  const velocity = new THREE.Vector3();
  const direction = new THREE.Vector3();
  const keys = new Set<string>();
  let dragging = false;
  let yaw = 0;
  let pitch = 0;

  const onKeyDown = (event: KeyboardEvent) => {
    keys.add(event.code);
  };
  const onKeyUp = (event: KeyboardEvent) => {
    keys.delete(event.code);
  };
  const onPointerDown = () => {
    dragging = true;
  };
  const onPointerUp = () => {
    dragging = false;
  };
  const onPointerMove = (event: PointerEvent) => {
    if (!dragging) return;
    yaw -= event.movementX * 0.0025;
    pitch -= event.movementY * 0.0025;
    pitch = Math.max(-1.4, Math.min(1.4, pitch));
  };

  window.addEventListener("keydown", onKeyDown);
  window.addEventListener("keyup", onKeyUp);
  domElement.addEventListener("pointerdown", onPointerDown);
  window.addEventListener("pointerup", onPointerUp);
  window.addEventListener("pointermove", onPointerMove);

  return {
    update(delta: number) {
      direction.set(0, 0, 0);
      if (keys.has("KeyW") || keys.has("ArrowUp")) direction.z -= 1;
      if (keys.has("KeyS") || keys.has("ArrowDown")) direction.z += 1;
      if (keys.has("KeyA") || keys.has("ArrowLeft")) direction.x -= 1;
      if (keys.has("KeyD") || keys.has("ArrowRight")) direction.x += 1;

      if (direction.lengthSq() > 0) {
        direction.normalize();
        const speed = keys.has("ShiftLeft") ? 4.5 : 2.2;
        const sin = Math.sin(yaw);
        const cos = Math.cos(yaw);
        velocity.x = direction.x * cos + direction.z * sin;
        velocity.z = direction.z * cos - direction.x * sin;
        camera.position.x += velocity.x * speed * delta;
        camera.position.z += velocity.z * speed * delta;
      }

      camera.position.y = 1.6;
      camera.rotation.order = "YXZ";
      camera.rotation.y = yaw;
      camera.rotation.x = pitch;
    },
    dispose() {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
      domElement.removeEventListener("pointerdown", onPointerDown);
      window.removeEventListener("pointerup", onPointerUp);
      window.removeEventListener("pointermove", onPointerMove);
    },
  };
}
