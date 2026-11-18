/* Canvas projection for the three Cobalt character models. */
(() => {
  'use strict';

  const RAMP = '.:+*#%@';
  const QUARTER = Math.PI / 2;
  const AMBIENT_LIMIT = 3800;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const themes = [
    [0, 1, 2, 3, 4, 5, 6],
    [0, 0, 1, 2, 3, 4, 5],
  ];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  function box(x, y, z, width, height, depth, material, inset = 0) {
    const center = [x, y, z];
    const lengths = [width, height, depth];
    const points = [];
    for (let axis = 0; axis < 3; axis++) {
      const across = (axis + 1) % 3;
      const up = (axis + 2) % 3;
      const cols = Math.ceil(lengths[across] / 0.065);
      const rows = Math.ceil(lengths[up] / 0.065);
      for (const sign of [-1, 1]) {
        const faceTone = typeof material === 'number' ? material : material(axis, sign);
        const normal = [0, 0, 0];
        normal[axis] = sign;
        for (let row = 0; row <= rows; row++) {
          for (let col = 0; col <= cols; col++) {
            const pos = [...center];
            pos[axis] += sign * lengths[axis] / 2;
            pos[across] += (col / cols - 0.5) * lengths[across];
            pos[up] += (row / rows - 0.5) * lengths[up];
            const edge = Math.min(col / cols, 1 - col / cols, row / rows, 1 - row / rows);
            points.push({ pos, normal, tone: edge < inset ? 0 : faceTone });
          }
        }
      }
    }
    return points;
  }

  function line(vertices, tone) {
    const points = [];
    let distance = 0;
    for (let i = 1; i < vertices.length; i++) {
      const a = vertices[i - 1], b = vertices[i];
      const delta = b.map((value, axis) => value - a[axis]);
      const length = Math.hypot(...delta);
      const steps = Math.ceil(length / 0.045);
      for (let step = 0; step <= steps; step++) {
        const fraction = step / steps;
        points.push({ pos: a.map((value, axis) => value + delta[axis] * fraction),
          tone, distance: distance + length * fraction });
      }
      distance += length;
    }
    return points;
  }

  function circuit() {
    const points = box(0, -0.24, 0, 4.9, 0.22, 3.25, 1);
    points.push(...box(0, 0.025, 0, 1.55, 0.35, 1.37, 4));
    for (const side of [-1, 1]) {
      for (let pin = -2; pin <= 2; pin++) {
        const z = pin * 0.235;
        points.push(...box(side * 0.87, -0.08, z, 0.24, 0.1, 0.11, 3));
        points.push(...line([[side * 0.99, -0.095, z], [side * (1.22 + Math.abs(pin) * 0.15), -0.095, z],
          [side * (1.58 + Math.abs(pin) * 0.12), -0.095, z + pin * 0.22], [side * 2.1, -0.095, z + pin * 0.22]], 2));
        points.push(...box(side * 2.14, -0.095, z + pin * 0.22, 0.24, 0.08, 0.17, 3));
      }
    }
    for (const x of [-1.83, 1.83]) {
      points.push(...box(x, -0.05, -1.26, 0.5, 0.15, 0.27, 3));
      points.push(...box(x, -0.05, 1.26, 0.5, 0.15, 0.27, 3));
    }
    const trace = line([[0, 0.21, 0], [0.73, 0.21, 0], [1.03, 0.04, 0], [1.28, 0.01, 0],
      [1.63, 0.01, 0.39], [2.14, 0.01, 0.39]], 2);
    const length = trace.at(-1).distance;
    return {
      yaw: -0.32, pitch: 0.84, size: 6.15,
      flow: x => [0.22 + 0.13 * Math.sin(x * 5 - 0.65),
        0.43 + 0.15 * Math.sin(x * 6 + 0.4), 0.68 + 0.15 * Math.sin(x * 5 - 2)],
      paint(put, at, state) {
        points.forEach(point => put(point));
        if (state.signal === null) {
          trace.forEach(point => put(point));
          return;
        }
        const head = Math.min(1, (at - state.signal) / 960) * length;
        trace.forEach(point => {
          const lit = point.distance <= head && point.distance > head - 0.62;
          put(point, lit ? 6 : 2, undefined, lit ? '@' : undefined);
        });
      },
    };
  }

  function piano() {
    const points = box(0, -0.56, -0.055, 4.8, 0.45, 1.72, 2);
    for (let i = 0; i < 10; i++) {
      points.push(...box((i - 4.5) * 0.44, -0.24, 0.19, 0.36, 0.19, 1.42, 1));
    }
    for (const i of [0, 1, 3, 4, 5, 7, 8]) {
      points.push(...box((i - 4) * 0.44, -0.145, -0.21, 0.24, 0.15, 0.76, 5));
    }
    return {
      yaw: -0.18, pitch: 0.76, size: 5.95,
      flow: (x, state) => {
        const swing = state.pattern === 'steady' ? 0 : Math.sin(x * 8) * 0.6;
        const wave = Math.sin(x * 7.5 + swing);
        return [0.24 + wave * 0.12, 0.49 + Math.sin(x * 8 + 1 + swing) * 0.14, 0.71 - wave * 0.11];
      },
      paint(put, at, state) {
        points.forEach(point => put(point));
        const pulse = (state.ambient / 1450) % 1;
        for (let i = 0; i <= 170; i++) {
          const u = i / 170;
          const x = 4.5 * (u - 0.5);
          const beat = state.pattern === 'steady' ? u * 4 : u * 4 + Math.sin(u * Math.PI * 4) * 0.35;
          const carrier = Math.sin(2 * Math.PI * (u * 13 - pulse));
          const envelope = Math.pow(Math.max(0, Math.cos(2 * Math.PI * beat)), 2);
          const y = 0.78 + carrier * (0.095 + envelope * 0.47);
          put({ pos: [x, 0.78, -0.57], tone: 0 });
          put({ pos: [x, y, -0.57], tone: 3 + envelope * 2 }, undefined, undefined, envelope > 0.55 ? '+' : undefined);
        }
      },
    };
  }

  const rotateY = ([x, y, z], sin, cos) => [x * cos + z * sin, y, z * cos - x * sin];

  function puzzle() {
    const fixed = [], layer = [];
    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          const center = [x, y, z];
          if (center.every(value => value === 0)) continue;
          const chunk = box(x, y, z, 0.85, 0.85, 0.85, (axis, sign) => {
            if (center[axis] !== sign) return 0;
            return [[3, 4], [1, 5], [2, 6]][axis][sign === 1 ? 1 : 0];
          }, 0.095);
          (y === 1 ? layer : fixed).push(...chunk);
        }
      }
    }
    return {
      yaw: -0.53, pitch: 0.44, size: 6.3,
      flow: x => [0.2 + 0.24 * Math.sin(Math.PI * x),
        0.49 + 0.22 * Math.sin(Math.PI * (x - 0.35)), 0.69 + 0.16 * Math.sin(Math.PI * (x + 0.35))],
      paint(put, at, state) {
        fixed.forEach(point => put(point));
        const turn = state.turn;
        const progress = turn ? clamp((at - turn.start) / 410, 0, 1) : 0;
        const angle = QUARTER * (state.turns + (turn ? progress * progress * (3 - 2 * progress) : 0));
        const sin = Math.sin(angle), cos = Math.cos(angle);
        layer.forEach(point => put(point, undefined, { sin, cos }));
      },
    };
  }

  const factories = { technology: circuit, music: piano, cubing: puzzle };
  const styles = getComputedStyle(document.documentElement);
  const font = styles.getPropertyValue('--font-outlier').trim();
  const palette = ['--color-glyph-1', '--color-glyph-2', '--color-glyph-3', '--color-glyph-4',
    '--color-accent', '--color-accent-deep', '--color-ink'].map(name => styles.getPropertyValue(name).trim());
  const trailFaint = styles.getPropertyValue('--color-model-trail').trim();

  function renderer(canvas, ctx, model) {
    const cellWidth = 8, cellHeight = 16;
    let cols, rows, width, height, depth, tones, glyphs, lit;

    function resize() {
      const rect = canvas.getBoundingClientRect();
      width = Math.round(rect.width);
      height = Math.round(rect.height);
      const scale = Math.min(devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * scale);
      canvas.height = Math.round(height * scale);
      ctx.setTransform(scale, 0, 0, scale, 0, 0);
      cols = Math.ceil(width / cellWidth);
      rows = Math.ceil(height / cellHeight);
      depth = new Float32Array(cols * rows);
      tones = new Uint8Array(cols * rows);
      glyphs = new Array(cols * rows);
      lit = new Uint8Array(cols * rows);
    }

    function draw(time, state) {
      if (!width || !height) return;
      ctx.clearRect(0, 0, width, height);
      depth.fill(-Infinity);
      const yawSin = Math.sin(state.yaw), yawCos = Math.cos(state.yaw);
      const pitchSin = Math.sin(state.pitch), pitchCos = Math.cos(state.pitch);
      const scale = Math.min(width, height * 1.2) / model.size;
      const ox = (width - cols * cellWidth) / 2;
      const oy = (height - rows * cellHeight) / 2;
      ctx.font = `13px ${font || 'monospace'}`;
      ctx.textBaseline = 'middle';

      function put(point, requestedTone = point.tone, turn, glyph) {
        const [x, y, z] = turn ? rotateY(point.pos, turn.sin, turn.cos) : point.pos;
        const rx = x * yawCos + z * yawSin;
        const rz = z * yawCos - x * yawSin;
        const ry = y * pitchCos - rz * pitchSin;
        const front = y * pitchSin + rz * pitchCos;
        let light = 0;
        if (point.normal) {
          const [nx, ny, nz] = turn ? rotateY(point.normal, turn.sin, turn.cos) : point.normal;
          const nzYaw = nz * yawCos - nx * yawSin;
          const normalDepth = ny * pitchSin + nzYaw * pitchCos;
          if (normalDepth < 0.025) return;
          light = normalDepth > 0.55 ? 1 : 0;
        }
        const perspective = 8 / (8 - front);
        const col = Math.floor((width / 2 + rx * scale * perspective - ox) / cellWidth);
        const row = Math.floor((height / 2 - ry * scale * perspective - oy) / cellHeight);
        if (col < 0 || col >= cols || row < 0 || row >= rows) return;
        const index = row * cols + col;
        const shade = clamp(Math.round(requestedTone) + light, 0, 6);
        if (front < depth[index] - 0.028 || (front <= depth[index] + 0.028 && tones[index] > shade)) return;
        depth[index] = Math.max(front, depth[index]);
        tones[index] = shade;
        lit[index] = Number(glyph === '@');
        const paletteRamp = themes[light ? 0 : 1];
        const pulse = state.ambient > 0 && Math.sin(state.ambient / 410 - col * 0.22 + row * 0.1) > 0.84 ? 1 : 0;
        glyphs[index] = glyph || RAMP[Math.min(6, paletteRamp[shade] + pulse)];
      }

      model.paint(put, time, state);
      // Each path trails off as lighter glyphs. Leave painted model cells clear.
      const travel = state.ambient / 360;
      for (let col = 0; col < cols; col++) {
        const x = col / (cols - 1);
        model.flow(x, state).forEach((y, path) => {
          const offset = path * 0.27;
          const crest = Math.pow(0.5 + 0.5 * Math.sin(x * 18 - travel + offset * 14), 2);
          const taper = Math.sin(Math.PI * (0.06 + 0.88 * x));
          const center = y + 0.012 * Math.sin(x * 18 - travel + path);
          const mainRow = Math.round(center * (rows - 1));
          for (const band of [-1, 0, 1]) {
            const row = mainRow + band;
            if (row < 0 || row >= rows || Number.isFinite(depth[row * cols + col])) continue;
            const density = (0.20 + 0.80 * crest) * taper;
            if (band && density < 0.57 + (col % 3) * 0.09) continue;
            if (!band && density < 0.16 && col % 3 === 1) continue;
            const glyph = ['.', ':', '+', '*'][Math.min(3, Math.floor((band ? density * 0.58 : density) * 4))];
            ctx.fillStyle = band || density < 0.25 ? trailFaint : palette[density > 0.68 ? 1 : 0];
            ctx.fillText(glyph, ox + col * cellWidth, oy + (row + 0.5) * cellHeight);
          }
        });
      }
      for (let index = 0; index < depth.length; index++) {
        if (!Number.isFinite(depth[index])) continue;
        const col = index % cols, row = Math.floor(index / cols);
        ctx.fillStyle = palette[lit[index] ? 4 : tones[index]];
        ctx.fillText(glyphs[index], ox + col * cellWidth, oy + (row + 0.5) * cellHeight);
      }
    }
    return { resize, draw };
  }

  const instances = [];
  let frame = 0;
  let last = 0;
  function tick(now) {
    frame = 0;
    const step = !last ? 0 : Math.min(now - last, 40);
    if (!last || now - last >= 1000 / 30) {
      last = now;
      instances.forEach(instance => instance.update(now, step));
    }
    schedule();
  }
  function schedule() {
    if (!frame && !document.hidden && instances.some(instance => instance.running())) {
      frame = requestAnimationFrame(tick);
    }
    if (!frame) last = 0;
  }

  function initialize(figure) {
    const canvas = figure.querySelector('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const model = factories[figure.dataset.model]();
    const stage = figure.querySelector('.model-stage');
    const buttons = [...figure.querySelectorAll('[data-action]')];
    const status = figure.querySelector('[role="status"]');
    const play = figure.querySelector('[data-action="motion"]');
    const view = renderer(canvas, ctx, model);
    const state = {
      yaw: model.yaw, pitch: model.pitch, ambient: 0, pattern: 'steady',
      signal: null, signalDone: false, turns: 0, turn: null,
    };
    let inView = false;
    let paused = false;
    let drag = null;
    let announceFrame = 0;
    const announce = message => {
      cancelAnimationFrame(announceFrame);
      status.textContent = '';
      announceFrame = requestAnimationFrame(() => { status.textContent = message; });
    };
    const canAnimate = () => !motion.matches && !paused && inView && !document.hidden;
    const running = () => canAnimate() && (state.ambient < AMBIENT_LIMIT || state.turn || state.signal !== null && !state.signalDone);
    const syncMotionKey = () => {
      play.hidden = motion.matches;
      const label = paused || state.ambient >= AMBIENT_LIMIT ? play.dataset.play : play.dataset.pause;
      if (play.textContent !== label) play.textContent = label;
    };
    const finishTurn = () => {
      if (!state.turn) return;
      state.turns = (state.turns + 1) % 4;
      announce(state.turn.message);
      state.turn = null;
    };
    const finishSignal = () => {
      if (state.signal === null || state.signalDone) return;
      state.signalDone = true;
      announce(figure.querySelector('[data-action="signal"]').dataset.complete);
    };
    const draw = now => view.draw(now, state);
    const settle = () => {
      finishTurn();
      if (state.signal !== null) {
        state.signal = performance.now() - 960;
        finishSignal();
      }
      draw(performance.now());
    };

    function update(now, step) {
      if (!running()) return;
      state.ambient = Math.min(AMBIENT_LIMIT, state.ambient + step);
      if (state.turn && now - state.turn.start >= 410) finishTurn();
      if (state.signal !== null && now - state.signal >= 960) finishSignal();
      draw(now);
      syncMotionKey();
    }

    function move(dx, dy) {
      state.yaw = (state.yaw + dx) % (2 * Math.PI);
      state.pitch = clamp(state.pitch + dy, -Math.PI, Math.PI);
      draw(performance.now());
    }

    function activate(button) {
      const now = performance.now();
      switch (button.dataset.action) {
        case 'left': move(-0.24, 0); return;
        case 'right': move(0.24, 0); return;
        case 'up': move(0, 0.24); return;
        case 'down': move(0, -0.24); return;
        case 'view':
          state.yaw = model.yaw;
          state.pitch = model.pitch;
          break;
        case 'motion':
          if (paused || state.ambient >= AMBIENT_LIMIT) {
            paused = false;
            state.ambient = 0;
          } else {
            paused = true;
            settle();
          }
          syncMotionKey();
          break;
        case 'signal':
          state.signal = now;
          state.signalDone = false;
          if (!canAnimate()) settle();
          break;
        case 'steady':
        case 'syncopated':
          state.pattern = button.dataset.action;
          buttons.filter(key => key.hasAttribute('aria-pressed')).forEach(key => {
            key.setAttribute('aria-pressed', String(key === button));
          });
          break;
        case 'turn':
          finishTurn();
          state.turn = { start: now, message: button.dataset.complete };
          if (!canAnimate()) finishTurn();
          break;
        case 'cube':
          state.turn = null;
          state.turns = 0;
          announce(button.dataset.complete);
          break;
      }
      draw(now);
      schedule();
    }

    stage.addEventListener('pointerdown', event => {
      if (!event.isPrimary || event.button !== 0) return;
      drag = { id: event.pointerId, x: event.clientX, y: event.clientY };
      stage.setPointerCapture(event.pointerId);
      stage.classList.add('is-dragging');
    });
    stage.addEventListener('pointermove', event => {
      if (!drag || event.pointerId !== drag.id) return;
      const dx = event.clientX - drag.x;
      const dy = event.pointerType === 'touch' ? 0 : event.clientY - drag.y;
      move(dx * 0.012, dy * 0.012);
      drag.x = event.clientX;
      drag.y = event.clientY;
    });
    function endDrag(event) {
      if (event.pointerId !== drag?.id) return;
      drag = null;
      stage.classList.remove('is-dragging');
    }
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(type => stage.addEventListener(type, endDrag));
    buttons.forEach(button => button.addEventListener('click', () => activate(button)));

    canvas.hidden = false;
    figure.querySelector('.model-fallback').hidden = true;
    figure.querySelector('.model-controls').hidden = false;
    figure.querySelector('.model-hint').hidden = false;
    stage.classList.add('is-interactive');
    const resize = () => { view.resize(); draw(performance.now()); };
    resize();
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
    else window.addEventListener('resize', resize, { passive: true });
    document.fonts?.ready.then(resize);
    const motionChanged = () => {
      if (!canAnimate()) settle();
      syncMotionKey();
      schedule();
    };
    if (motion.addEventListener) motion.addEventListener('change', motionChanged);
    else motion.addListener(motionChanged);
    document.addEventListener('visibilitychange', motionChanged);
    syncMotionKey();

    const instance = {
      running, update,
      show(visible) {
        inView = visible;
        if (!visible) settle();
        schedule();
      },
    };
    instances.push(instance);
    return instance;
  }

  const figures = [...document.querySelectorAll('[data-model]')];
  const rendered = new Map();
  for (const figure of figures) {
    const instance = initialize(figure);
    if (instance) rendered.set(figure.querySelector('canvas'), instance);
  }
  if ('IntersectionObserver' in window && rendered.size) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => rendered.get(entry.target).show(entry.isIntersecting && entry.intersectionRatio >= 0.2));
    }, { threshold: 0.2 });
    rendered.forEach((_, canvas) => observer.observe(canvas));
  } else {
    // Explicit actions still work when viewport observation is unavailable.
    rendered.forEach(instance => instance.show(false));
  }
})();
