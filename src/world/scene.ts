import * as THREE from "three";

export type WorldObjects = {
  scene: THREE.Scene;
  floor: THREE.Mesh;
  grabables: THREE.Object3D[];
  teleportTarget: THREE.Mesh;
};

function makeGridTexture(): THREE.CanvasTexture {
  const size = 512;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    throw new Error("Could not create floor texture context");
  }

  const gradient = ctx.createLinearGradient(0, 0, size, size);
  gradient.addColorStop(0, "#163028");
  gradient.addColorStop(1, "#0e1c22");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);

  ctx.strokeStyle = "rgba(62, 207, 142, 0.22)";
  ctx.lineWidth = 2;
  const step = size / 8;
  for (let i = 0; i <= 8; i += 1) {
    const p = i * step;
    ctx.beginPath();
    ctx.moveTo(p, 0);
    ctx.lineTo(p, size);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, p);
    ctx.lineTo(size, p);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(8, 8);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

function createGrabable(
  geometry: THREE.BufferGeometry,
  color: number,
  position: THREE.Vector3,
  name: string,
): THREE.Mesh {
  const material = new THREE.MeshStandardMaterial({
    color,
    roughness: 0.35,
    metalness: 0.15,
    emissive: new THREE.Color(color).multiplyScalar(0.08),
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.copy(position);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.name = name;
  mesh.userData.grabbable = true;
  mesh.userData.homePosition = position.clone();
  return mesh;
}

export function createWorld(): WorldObjects {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color("#08110e");
  scene.fog = new THREE.Fog("#08110e", 8, 28);

  const hemi = new THREE.HemisphereLight(0xb8fff0, 0x1a2a22, 0.85);
  scene.add(hemi);

  const key = new THREE.DirectionalLight(0xfff2d6, 1.15);
  key.position.set(4, 8, 2);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.near = 0.5;
  key.shadow.camera.far = 30;
  key.shadow.camera.left = -10;
  key.shadow.camera.right = 10;
  key.shadow.camera.top = 10;
  key.shadow.camera.bottom = -10;
  scene.add(key);

  const rim = new THREE.PointLight(0x3ecf8e, 12, 18, 2);
  rim.position.set(-3, 2.2, -4);
  scene.add(rim);

  const floor = new THREE.Mesh(
    new THREE.CircleGeometry(12, 64),
    new THREE.MeshStandardMaterial({
      map: makeGridTexture(),
      roughness: 0.92,
      metalness: 0.05,
    }),
  );
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  floor.name = "floor";
  scene.add(floor);

  const ring = new THREE.Mesh(
    new THREE.RingGeometry(11.6, 12, 64),
    new THREE.MeshBasicMaterial({
      color: 0x3ecf8e,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
    }),
  );
  ring.rotation.x = -Math.PI / 2;
  ring.position.y = 0.01;
  scene.add(ring);

  const pedestal = new THREE.Mesh(
    new THREE.CylinderGeometry(0.55, 0.7, 0.35, 32),
    new THREE.MeshStandardMaterial({
      color: 0x243832,
      roughness: 0.7,
      metalness: 0.2,
    }),
  );
  pedestal.position.set(0, 0.175, -2.2);
  pedestal.receiveShadow = true;
  pedestal.castShadow = true;
  scene.add(pedestal);

  const grabables: THREE.Object3D[] = [
    createGrabable(
      new THREE.BoxGeometry(0.28, 0.28, 0.28),
      0x3ecf8e,
      new THREE.Vector3(-0.9, 0.55, -1.6),
      "cube",
    ),
    createGrabable(
      new THREE.SphereGeometry(0.18, 32, 32),
      0xf0a35e,
      new THREE.Vector3(0, 0.7, -2.2),
      "orb",
    ),
    createGrabable(
      new THREE.TetrahedronGeometry(0.24),
      0x6ec8ff,
      new THREE.Vector3(0.95, 0.6, -1.5),
      "crystal",
    ),
  ];

  for (const object of grabables) {
    scene.add(object);
  }

  const teleportTarget = new THREE.Mesh(
    new THREE.RingGeometry(0.18, 0.32, 32),
    new THREE.MeshBasicMaterial({
      color: 0x3ecf8e,
      transparent: true,
      opacity: 0.85,
      side: THREE.DoubleSide,
    }),
  );
  teleportTarget.rotation.x = -Math.PI / 2;
  teleportTarget.visible = false;
  scene.add(teleportTarget);

  // Ambient markers so the space reads clearly in VR.
  for (let i = 0; i < 6; i += 1) {
    const angle = (i / 6) * Math.PI * 2;
    const pillar = new THREE.Mesh(
      new THREE.CylinderGeometry(0.08, 0.12, 1.8, 12),
      new THREE.MeshStandardMaterial({
        color: 0x1d342c,
        emissive: 0x0b1f18,
        roughness: 0.8,
      }),
    );
    pillar.position.set(Math.cos(angle) * 5.5, 0.9, Math.sin(angle) * 5.5);
    pillar.castShadow = true;
    scene.add(pillar);
  }

  return { scene, floor, grabables, teleportTarget };
}
