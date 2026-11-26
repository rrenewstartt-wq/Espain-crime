// Lit three.js props for the archivos-del-terror sample (own work; three.js MIT, lib/three-LICENSE.txt).
// Every frame is a pure function of scene time t (seconds): draw(t) is called from a GSAP tween's onUpdate.
import * as THREE from "./three.module.min.js";

const TEX = {};
async function tex(name, repeat) {
  const key = name + (repeat ? repeat.join("x") : "");
  if (!TEX[key]) {
    const t = await new THREE.TextureLoader().loadAsync("assets/tex/" + name);
    t.colorSpace = THREE.SRGBColorSpace;
    if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
    t.anisotropy = 4;
    TEX[key] = t;
  }
  return TEX[key];
}
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const lerp = (a, b, k) => a + (b - a) * k;
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const ease = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const easeOut = (x) => 1 - Math.pow(1 - clamp01(x), 3);

function renderer(canvas, exposure) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setSize(1920, 1080, false);
  r.shadowMap.enabled = true;
  r.shadowMap.type = THREE.PCFSoftShadowMap;
  r.toneMapping = THREE.ACESFilmicToneMapping;
  r.toneMappingExposure = exposure || 1;
  r.outputColorSpace = THREE.SRGBColorSpace;
  return r;
}
async function dustPoints(n, box, seed, color, size) {
  const g = new THREE.BufferGeometry();
  const r = rng(seed);
  const base = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { base[i * 3] = lerp(box[0], box[3], r()); base[i * 3 + 1] = lerp(box[1], box[4], r()); base[i * 3 + 2] = lerp(box[2], box[5], r()); }
  g.setAttribute("position", new THREE.BufferAttribute(base.slice(), 3));
  const m = new THREE.PointsMaterial({ map: await tex("glow.png"), color, size, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.9 });
  const pts = new THREE.Points(g, m);
  pts.userData.update = (t) => {
    const a = g.attributes.position.array;
    for (let i = 0; i < n; i++) {
      const s = ((i * 7919) % 1000) / 1000;
      a[i * 3] = base[i * 3] + Math.sin(t * 0.7 + i) * 0.03;
      a[i * 3 + 1] = base[i * 3 + 1] + t * (0.03 + 0.06 * s);
      a[i * 3 + 2] = base[i * 3 + 2] + Math.cos(t * 0.5 + i * 1.3) * 0.03;
    }
    g.attributes.position.needsUpdate = true;
  };
  return pts;
}
function glowSprite(map, color, scale, opacity) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map, color, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity }));
  s.scale.set(scale, scale, 1);
  return s;
}

// ---------------------------------------------------------------- filing cabinet with an empty drawer
async function drawer(canvas, o) {
  const r = renderer(canvas, 1.05);
  const s = new THREE.Scene();
  s.background = new THREE.Color(0x05080b);
  s.fog = new THREE.Fog(0x05080b, 4, 11);
  const metal = new THREE.MeshStandardMaterial({ map: await tex("metal.jpg"), metalness: 0.55, roughness: 0.48 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x0c1012, roughness: 0.9 });
  const inner = new THREE.MeshStandardMaterial({ map: await tex("metal.jpg"), color: 0x6b6f6a, metalness: 0.3, roughness: 0.7 });
  const W = 0.9, H = 1.4, D = 0.7;
  const cab = new THREE.Mesh(new THREE.BoxGeometry(W, H, D), metal); cab.position.y = H / 2; cab.castShadow = cab.receiveShadow = true; s.add(cab);
  const label = new THREE.MeshStandardMaterial({ map: await tex("paper_cold.jpg"), roughness: 0.8 });
  const handle = new THREE.MeshStandardMaterial({ color: 0xb9c0c2, metalness: 0.9, roughness: 0.25 });
  const drawers = [];
  for (let k = 0; k < 4; k++) {
    const g = new THREE.Group();
    const fy = H - 0.2 - k * 0.33;
    const front = new THREE.Mesh(new THREE.BoxGeometry(W - 0.06, 0.3, 0.03), metal); front.castShadow = true; g.add(front);
    const h = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.03, 0.04), handle); h.position.set(0, -0.04, 0.03); g.add(h);
    const l = new THREE.Mesh(new THREE.PlaneGeometry(0.16, 0.06), label); l.position.set(0, 0.07, 0.017); g.add(l);
    if (k === 1) { // the drawer that opens: an open box behind its front
      const bw = W - 0.1, bd = D - 0.08, bh = 0.24;
      const bottom = new THREE.Mesh(new THREE.BoxGeometry(bw, 0.01, bd), inner); bottom.position.set(0, -bh / 2, -bd / 2); bottom.receiveShadow = true; g.add(bottom);
      for (const sx of [-1, 1]) { const side = new THREE.Mesh(new THREE.BoxGeometry(0.01, bh, bd), inner); side.position.set(sx * bw / 2, 0, -bd / 2); side.castShadow = side.receiveShadow = true; g.add(side); }
      const back = new THREE.Mesh(new THREE.BoxGeometry(bw, bh, 0.01), inner); back.position.set(0, 0, -bd); g.add(back);
    }
    g.position.set(0, fy, D / 2 + 0.016);
    s.add(g); drawers.push(g);
  }
  const hole = new THREE.Mesh(new THREE.PlaneGeometry(W - 0.06, 0.3), dark); hole.position.set(0, H - 0.2 - 0.33, D / 2 + 0.002); s.add(hole);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(14, 14), new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [4, 4]), color: 0x5a6266, roughness: 0.95 }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; s.add(floor);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(14, 6), new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [3, 1]), color: 0x6c7478, roughness: 1 }));
  wall.position.set(0, 3, -0.6); wall.receiveShadow = true; s.add(wall);
  const sp = new THREE.SpotLight(0xdbe6ee, 38, 9, 0.5, 0.65, 1.6); sp.position.set(0.9, 3.1, 2.2); sp.target.position.set(0, 1.0, 0.3);
  sp.castShadow = true; sp.shadow.mapSize.set(1024, 1024); s.add(sp, sp.target);
  s.add(new THREE.HemisphereLight(0x50606c, 0x0a0c0e, 0.35));
  const rim = new THREE.PointLight(0x8fb0c4, 4, 6); rim.position.set(-1.6, 1.8, -0.2); s.add(rim);
  const dust = await dustPoints(70, [-0.4, 0.9, 0.1, 0.4, 1.6, 0.9], 25, 0xdde8ee, 0.022); s.add(dust);
  const cam = new THREE.PerspectiveCamera(32, 16 / 9, 0.05, 40);
  const cut = o.cut || 99;
  return (t) => {
    const k = easeOut((t - 0.1) / 0.85);
    drawers[1].position.z = D / 2 + 0.016 + 0.5 * k;
    dust.userData.update(t);
    if (t < cut) { cam.position.set(lerp(1.55, 1.35, t / cut), lerp(1.35, 1.3, t / cut), lerp(2.6, 2.3, t / cut)); cam.lookAt(0, 1.0, 0.3); }
    else { const u = (t - cut) / Math.max(0.1, o.d - cut); cam.position.set(0.05, 2.15 - 0.05 * u, 1.35 + 0.02 * u); cam.lookAt(0, 0.95, 0.95); }
    r.render(s, cam);
  };
}

// ---------------------------------------------------------------- stairwell up to a locked door (stairs) / door opening (door)
async function stairs(canvas, o) {
  const r = renderer(canvas, o.mode === "door" ? 1.0 : 1.15);
  const s = new THREE.Scene();
  s.background = new THREE.Color(0x030202);
  s.fog = new THREE.FogExp2(0x0a0604, 0.09);
  const conc = new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [2, 2]), color: 0x8a7a68, roughness: 0.95 });
  const step = new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [1, 0.3]), color: 0x9a8a76, roughness: 0.9 });
  const N = 13, sh = 0.18, sd = 0.3, w = 1.3;
  for (let i = 0; i < N; i++) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, sh * (i + 1), sd), step);
    m.position.set(0, sh * (i + 1) / 2, -i * sd); m.castShadow = m.receiveShadow = true; s.add(m);
  }
  const topY = sh * N, topZ = -N * sd;
  const land = new THREE.Mesh(new THREE.BoxGeometry(w, topY, 1.4), step); land.position.set(0, topY / 2, topZ - 0.55); land.receiveShadow = true; s.add(land);
  for (const sx of [-1, 1]) {
    const wl = new THREE.Mesh(new THREE.PlaneGeometry(9, 6), conc); wl.rotation.y = -sx * Math.PI / 2; wl.position.set(sx * w / 2, 2.4, -2.5); wl.receiveShadow = true; s.add(wl);
  }
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(w, 9), conc); ceil.rotation.x = Math.PI / 2; ceil.position.set(0, topY + 2.4, -2.5); s.add(ceil);
  // end wall with the door opening
  const dz = topZ - 1.2, dw = 0.9, dh = 2.0;
  const wallL = new THREE.Mesh(new THREE.PlaneGeometry((w - dw) / 2, 4), conc); wallL.position.set(-(w + dw) / 4, topY + 2, dz); s.add(wallL);
  const wallR = wallL.clone(); wallR.position.x = (w + dw) / 4; s.add(wallR);
  const wallT = new THREE.Mesh(new THREE.PlaneGeometry(dw, 4 - dh), conc); wallT.position.set(0, topY + dh + (4 - dh) / 2, dz); s.add(wallT);
  // light behind the door (the room)
  const room = new THREE.Mesh(new THREE.PlaneGeometry(4, 4), new THREE.MeshBasicMaterial({ color: 0xfff0d8 }));
  room.position.set(0, topY + 1.5, dz - 1.4); s.add(room);
  const behind = new THREE.SpotLight(0xffe2b8, 0, 12, 0.6, 0.5, 1.2); behind.position.set(0, topY + 1.4, dz - 1.2); behind.target.position.set(0, 0.5, 1.0); behind.castShadow = true; behind.shadow.mapSize.set(1024, 1024); s.add(behind, behind.target);
  const door = new THREE.Group();
  const leaf = new THREE.Mesh(new THREE.BoxGeometry(dw, dh, 0.05), new THREE.MeshStandardMaterial({ map: await tex("wood_door.jpg"), roughness: 0.85 }));
  leaf.position.set(dw / 2, dh / 2, 0); leaf.castShadow = true; door.add(leaf);
  door.position.set(-dw / 2, topY, dz + 0.03); s.add(door);
  const gap = new THREE.Mesh(new THREE.PlaneGeometry(dw, 0.02), new THREE.MeshBasicMaterial({ color: 0xffd9a0 })); gap.position.set(0, topY + 0.012, dz + 0.06); s.add(gap);
  // the tungsten bulb above the door
  const bulb = new THREE.PointLight(0xffa860, 26, 9, 1.4); bulb.position.set(0.0, topY + 2.25, dz + 0.45); bulb.castShadow = true; bulb.shadow.mapSize.set(512, 512); s.add(bulb);
  const gtex = await tex("glow.png");
  const bulbGlow = glowSprite(gtex, 0xffb870, 0.9, 0.9); bulbGlow.position.copy(bulb.position); s.add(bulbGlow);
  const flood = glowSprite(gtex, 0xfff0d8, 5, 0); flood.position.set(0, topY + 1.1, dz + 0.2); s.add(flood);
  s.add(new THREE.AmbientLight(0x2a1c10, 1.6));
  const dust = await dustPoints(160, [-0.6, topY - 0.5, dz - 0.3, 0.6, topY + 2.2, dz + 2.5], 31, 0xffd7a0, 0.03); s.add(dust);
  const cam = new THREE.PerspectiveCamera(o.mode === "door" ? 46 : 52, 16 / 9, 0.05, 40);
  return (t) => {
    dust.userData.update(t);
    if (o.mode === "door") {
      const k = ease((t - 0.08) / 0.62);
      door.rotation.y = -1.45 * k;
      behind.intensity = 60 * k;
      flood.material.opacity = 0.15 + 0.85 * k;
      r.toneMappingExposure = 1.0 + 1.6 * k;
      cam.position.set(0.06, topY + 1.55, dz + 2.0 - 0.5 * ease(t / o.d));
      cam.lookAt(0, topY + 1.2, dz - 0.5);
    } else {
      const u = t / o.d;
      const y = lerp(1.3, topY - 0.4, u), z = lerp(1.6, topZ + 2.4, u);
      cam.position.set(Math.sin(t * 5.1) * 0.015, y + Math.abs(Math.sin(t * 7.6)) * 0.03, z);
      cam.lookAt(0, y + 0.55, z - 3);
    }
    r.render(s, cam);
  };
}

// ---------------------------------------------------------------- boxes carried out through a bright doorway
async function boxes(canvas, o) {
  const r = renderer(canvas, 1.15);
  const s = new THREE.Scene();
  s.background = new THREE.Color(0x040302);
  s.fog = new THREE.FogExp2(0x120a05, 0.11);
  const conc = new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [3, 1]), color: 0x6e604f, roughness: 1 });
  const wallL = new THREE.Mesh(new THREE.PlaneGeometry(4, 9), conc); wallL.position.set(-2.6, 4.5, -6); s.add(wallL);
  const wallR = wallL.clone(); wallR.position.x = 2.6; s.add(wallR);
  const wallT = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 6.6), conc); wallT.position.set(0, 5.7, -6); s.add(wallT);
  const outside = new THREE.Mesh(new THREE.PlaneGeometry(8, 6), new THREE.MeshBasicMaterial({ color: 0xfff6e8, fog: false })); outside.position.set(0, 2, -7.5); s.add(outside);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(10, 16), new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [3, 4]), color: 0x5b4c3c, roughness: 1 }));
  floor.rotation.x = -Math.PI / 2; floor.position.z = -2; floor.receiveShadow = true; s.add(floor);
  const sun = new THREE.SpotLight(0xfff2de, 90, 16, 0.5, 0.5, 1.0); sun.position.set(0, 2.2, -7.2); sun.target.position.set(0, 0, 2); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024); s.add(sun, sun.target);
  const lamp = new THREE.PointLight(0xffa058, 3, 6, 1.6); lamp.position.set(1.4, 2.6, 0.5); s.add(lamp);
  s.add(new THREE.AmbientLight(0x1a1008, 0.5));
  const card = new THREE.MeshStandardMaterial({ map: await tex("cardboard.jpg"), color: 0x9c8a74, roughness: 0.92 });
  const figTex = await new THREE.TextureLoader().loadAsync("assets/fig/worker.png"); figTex.colorSpace = THREE.SRGBColorSpace;
  const figMat = new THREE.MeshBasicMaterial({ map: figTex, transparent: true, alphaTest: 0.05, color: 0x2a2420, side: THREE.DoubleSide });
  const items = [];
  for (let i = 0; i < 6; i++) {
    const g = new THREE.Group();
    const b = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.36, 0.4), card); b.position.set(0, 0.18, 0); b.castShadow = true; g.add(b);
    const b2 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.32, 0.38), card); b2.position.set(0.02, 0.52, 0.01); b2.rotation.y = 0.08; b2.castShadow = true; g.add(b2);
    s.add(g); items.push(g);
  }
  const dust = await dustPoints(140, [-1, 0.2, -6.5, 1, 2.6, 1], 48, 0xffe8c8, 0.035); s.add(dust);
  const cam = new THREE.PerspectiveCamera(42, 16 / 9, 0.05, 40);
  return (t) => {
    dust.userData.update(t);
    items.forEach((g, i) => {
      const u = ((t + i * 0.55) % 3.3) / 3.3;              // walking away from camera to the door
      g.position.set(0.05 + Math.sin(i * 1.7) * 0.06, 0, lerp(-0.6, -6.4, u));
      g.rotation.y = Math.PI;
      g.visible = u < 0.97;
    });
    const cutB = o.cut || 99;
    if (t < cutB) { cam.position.set(0.15, 1.45, 3.2 - 0.25 * t); cam.lookAt(0, 1.4, -6); }
    else { cam.position.set(-0.9, 0.55, 1.6 - 0.2 * (t - cutB)); cam.lookAt(0.2, 1.2, -6); }
    r.render(s, cam);
  };
}

// ---------------------------------------------------------------- police building, cold morning
async function exterior(canvas, o) {
  const r = renderer(canvas, o.dim ? 0.85 : 1.15);
  const s = new THREE.Scene();
  s.background = await tex("sky_cold.jpg");
  s.fog = new THREE.Fog(o.dim ? 0x58687a : 0xa9bccb, 18, 80);
  const conc = new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [3, 1]), color: 0xb4b8b6, roughness: 0.95 });
  const glass = new THREE.MeshStandardMaterial({ color: 0x0b1014, metalness: 0.4, roughness: 0.25 });
  const bar = new THREE.MeshStandardMaterial({ color: 0x1b1f22, metalness: 0.6, roughness: 0.5 });
  const BW = 22, BH = 7.4, BD = 10;
  const b = new THREE.Mesh(new THREE.BoxGeometry(BW, BH, BD), conc); b.position.set(0, BH / 2, -BD / 2); b.castShadow = b.receiveShadow = true; s.add(b);
  const par = new THREE.Mesh(new THREE.BoxGeometry(BW + 0.4, 0.5, 0.5), conc); par.position.set(0, BH + 0.05, 0.05); par.castShadow = true; s.add(par);
  for (let row = 0; row < 2; row++) for (let i = 0; i < 9; i++) {
    const x = -BW / 2 + 1.6 + i * 2.35; const y = 1.6 + row * 3.3;
    if (row === 0 && i === 4) continue;
    const win = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.7, 0.1), glass); win.position.set(x, y, 0.02); s.add(win);
    const sill = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.12, 0.25), conc); sill.position.set(x, y - 0.92, 0.1); sill.castShadow = true; s.add(sill);
    for (let k = -2; k <= 2; k++) { const bb = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.7, 0.04), bar); bb.position.set(x + k * 0.24, y, 0.12); bb.castShadow = true; s.add(bb); }
  }
  const doorM = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.5, 0.12), new THREE.MeshStandardMaterial({ map: await tex("wood_door.jpg"), color: 0x8a8070, roughness: 0.8 }));
  doorM.position.set(-BW / 2 + 1.6 + 4 * 2.35, 1.25, 0.03); s.add(doorM);
  const awn = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.15, 1.1), conc); awn.position.set(doorM.position.x, 2.75, 0.5); awn.castShadow = true; s.add(awn);
  const plate = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.45, 0.05), new THREE.MeshStandardMaterial({ map: await tex("paper_cold.jpg"), color: 0xc9cbc6, roughness: 0.7 }));
  plate.position.set(doorM.position.x, 3.2, 0.04); s.add(plate);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 80), new THREE.MeshStandardMaterial({ map: await tex("concrete.jpg", [10, 6]), color: 0x6e6a62, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.position.z = 10; ground.receiveShadow = true; s.add(ground);
  // fence in front of the building
  const iron = new THREE.MeshStandardMaterial({ color: 0x101315, metalness: 0.5, roughness: 0.6 });
  for (let x = -16; x <= 16; x += 0.32) { if (Math.abs(x) < 0.9) continue; const p = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.9, 0.05), iron); p.position.set(x, 0.95, 4.5); p.castShadow = true; s.add(p); }
  for (const y of [0.3, 1.7]) { const rail = new THREE.Mesh(new THREE.BoxGeometry(32, 0.06, 0.06), iron); rail.position.set(0, y, 4.5); s.add(rail); }
  const treeMat = new THREE.MeshBasicMaterial({ map: await tex("tree.png"), transparent: true, alphaTest: 0.3, color: o.dim ? 0x30383a : 0x5a6462, fog: true });
  for (const [x, z, h] of [[-15, 1.5, 9], [16, 2.5, 8], [-21, -6, 10]]) { const tr = new THREE.Mesh(new THREE.PlaneGeometry(h * 0.86, h), treeMat); tr.position.set(x, h / 2, z); s.add(tr); }
  const sun = new THREE.DirectionalLight(0xfff0dc, o.dim ? 1.6 : 4.6); sun.position.set(-26, 16, 30); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -20, right: 20, top: 14, bottom: -6, far: 120 }); s.add(sun);
  s.add(new THREE.HemisphereLight(0x9fb6c8, 0x2a2622, o.dim ? 0.5 : 1.1));
  const gtex = await tex("glow.png");
  const sunGlow = glowSprite(gtex, 0xfff3e0, 22, o.dim ? 0.15 : 0.55); sunGlow.position.set(-30, 14, -30); s.add(sunGlow);
  let fig = null;
  if (o.figure) {
    const ft = await new THREE.TextureLoader().loadAsync("assets/fig/" + o.figure + ".png"); ft.colorSpace = THREE.SRGBColorSpace;
    fig = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 1.7), new THREE.MeshBasicMaterial({ map: ft, transparent: true, alphaTest: 0.05, color: 0x1c2024 }));
    s.add(fig);
  }
  const dust = await dustPoints(120, [-8, 0.2, 2, 8, 5, 8], 9, 0xfff2e0, 0.05); s.add(dust);
  const cam = new THREE.PerspectiveCamera(38, 16 / 9, 0.1, 200);
  const shots = o.shots;               // [[t0, fromPos, toPos, fromLook, toLook], ...]
  return (t) => {
    dust.userData.update(t);
    let sh = shots[0];
    for (const x of shots) if (t >= x[0]) sh = x;
    const t1 = shots[shots.indexOf(sh) + 1] ? shots[shots.indexOf(sh) + 1][0] : o.d;
    const u = clamp01((t - sh[0]) / (t1 - sh[0]));
    cam.position.set(lerp(sh[1][0], sh[2][0], u), lerp(sh[1][1], sh[2][1], u), lerp(sh[1][2], sh[2][2], u));
    cam.lookAt(lerp(sh[3][0], sh[4][0], u), lerp(sh[3][1], sh[4][1], u), lerp(sh[3][2], sh[4][2], u));
    if (fig) { const k = clamp01(t / o.d); fig.position.set(lerp(o.figFrom[0], o.figTo[0], k), lerp(o.figFrom[1], o.figTo[1], k) + 0.85 * 1.0, lerp(o.figFrom[2], o.figTo[2], k)); fig.scale.setScalar(1); fig.lookAt(cam.position.x, fig.position.y, cam.position.z); }
    r.render(s, cam);
  };
}

export async function mount(canvasId, kind, opts) {
  const canvas = document.getElementById(canvasId);
  const f = { drawer, stairs, boxes, exterior }[kind];
  return await f(canvas, opts);
}
