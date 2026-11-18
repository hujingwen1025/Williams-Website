/* Viewport character streams and projection for the Cobalt models. */
(() => {
  'use strict';

  const RAMP = '.:+*#%@';
  const CELL_WIDTH = 8, CELL_HEIGHT = 16, GLYPH_SIZE = 13;
  const QUARTER = Math.PI / 2;
  const FULL_TURN = 4 * QUARTER;
  const INTRO_SPIN_DURATION = 3000;
  const INTRO_VISIBLE_FRACTION = 0.5;
  const ACTIVE_VISIBLE_FRACTION = 0.2;
  const AMBIENT_LIMIT = 3800;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const themes = [
    [0, 1, 2, 3, 4, 5, 6],
    [0, 0, 1, 2, 3, 4, 5],
  ];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const corners = (x, y, z) => x.flatMap(a => y.flatMap(b => z.map(c => [a, b, c])));

  function box(x, y, z, width, height, depth, material, inset = 0) {
    const center = [x, y, z];
    const lengths = [width, height, depth];
    const points = [];
    for (let axis = 0; axis < 3; axis++) {
      const across = (axis + 1) % 3;
      const up = (axis + 2) % 3;
      const cols = Math.ceil(lengths[across] / 0.048);
      const rows = Math.ceil(lengths[up] / 0.048);
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
      bounds: () => corners([-2.45, 2.45], [-0.35, 0.22], [-1.625, 1.625]),
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
      bounds: () => corners([-2.4, 2.4], [-0.8, 1.36], [-0.92, 0.9]),
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
    const cubeBase = corners([-1.425, 1.425], [-1.425, 0.425], [-1.425, 1.425]);
    const cubeTop = corners([-1.425, 1.425], [0.575, 1.425], [-1.425, 1.425]);
    const layerAngle = (at, state) => {
      const progress = state.turn ? clamp((at - state.turn.start) / 410, 0, 1) : 0;
      return QUARTER * (state.turns + progress * progress * (3 - 2 * progress));
    };
    return {
      yaw: -0.53, pitch: 0.44, size: 6.3,
      bounds(at, state) {
        const angle = layerAngle(at, state);
        const sin = Math.sin(angle), cos = Math.cos(angle);
        return cubeBase.concat(cubeTop.map(point => rotateY(point, sin, cos)));
      },
      paint(put, at, state) {
        fixed.forEach(point => put(point));
        const angle = layerAngle(at, state);
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

  function startPageField() {
    const canvas = document.querySelector('.page-field');
    const ctx = canvas?.getContext('2d');
    if (!ctx) return;

    const textBlocks = [...document.querySelectorAll('.intro-copy, .about-copy, .topic-copy, .section-heading, .feature-copy, .section-tail, .interests-grid, .org-grid, .directory-controls, .repo-grid, .contact-grid, .site-footer')];
    const graphite = document.querySelector('.organization-section');
    const paperTints = ['light', 'mid', 'deep'].map(tint => styles.getPropertyValue('--color-stream-' + tint).trim());
    const graphiteTints = [1, 2, 3].map(tint => styles.getPropertyValue('--color-graphite-glyph-' + tint).trim());
    const streamRamp = '.:+*#';
    const strandSpacing = 300;
    let width = 0, height = 0, frame = 0, lastDraw = -Infinity;
    let travel = 0;

    function paint(now) {
      frame = 0;
      if (document.hidden || !width || !height) return;
      if (now - lastDraw < 1000 / 30) { requestPaint(); return; }
      const animated = !motion.matches;
      if (animated && Number.isFinite(lastDraw)) {
        travel = (travel + Math.min(now - lastDraw, 80) / 1450) % (2 * Math.PI);
      }
      lastDraw = now;
      const top = window.scrollY;
      const phaseOffset = animated ? travel : 0;
      const dark = graphite?.getBoundingClientRect();
      const masks = textBlocks.map(block => block.getBoundingClientRect()).filter(rect => rect.bottom > 0 && rect.top < height);
      const cols = Math.ceil(width / CELL_WIDTH);
      ctx.clearRect(0, 0, width, height);
      ctx.font = `${GLYPH_SIZE}px ${font || 'monospace'}`;
      ctx.textBaseline = 'middle';

      for (let lane = Math.floor((top - 190) / strandSpacing); lane <= Math.ceil((top + height + 190) / strandSpacing); lane++) {
        for (let col = 0; col < cols; col++) {
          const x = col * CELL_WIDTH;
          const across = col / Math.max(1, cols - 1);
          const phase = lane * 1.37;
          const curve = lane * strandSpacing + 80 * Math.sin(across * 6.8 + phase) + 36 * Math.sin(across * 11 - phase);
          const crest = 0.5 + 0.5 * Math.sin(across * 15 - phaseOffset + phase * 2);
          const drift = animated ? 6 * Math.sin(across * 7 - phaseOffset + phase) : 0;
          for (const strand of [-1, 0, 1]) {
            const center = curve + strand * (19 + 18 * Math.sin(across * 4 + phase));
            const pageY = CELL_HEIGHT * Math.round(center / CELL_HEIGHT);
            const y = pageY - top + drift;
            if (pageY < 0 || y < -CELL_HEIGHT || y > height + CELL_HEIGHT) continue;
            const hash = (Math.imul(col + 1, 73856093) ^ Math.imul(lane + 96, 19349663) ^ Math.imul(strand + 4, 83492791)) >>> 0;
            const noise = (hash % 113) / 113;
            if (strand && noise > 0.42 + crest * 0.37) continue;
            const density = (0.27 + crest * 0.56 + noise * 0.17) * (strand ? 0.72 : 1);
            const shade = density > 0.76 ? 2 : density > 0.48 ? 1 : 0;
            const inGraphite = dark && y >= dark.top && y <= dark.bottom;
            const overText = masks.some(rect => x + CELL_WIDTH >= rect.left - 6 && x <= rect.right + 6 && y >= rect.top - 6 && y <= rect.bottom + 6);
            ctx.globalAlpha = overText ? 0.19 : 0.72;
            ctx.fillStyle = (inGraphite ? graphiteTints : paperTints)[shade];
            ctx.fillText(streamRamp[Math.min(4, Math.floor(density * 5))], x, y);
          }
        }
      }
      ctx.globalAlpha = 1;
      if (animated) requestPaint();
    }

    function requestPaint() {
      if (!frame && !document.hidden) frame = requestAnimationFrame(paint);
    }

    function resize() {
      width = canvas.clientWidth;
      height = canvas.clientHeight;
      const dpr = Math.min(devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      requestPaint();
    }

    canvas.hidden = false;
    window.addEventListener('scroll', requestPaint, { passive: true });
    window.addEventListener('resize', resize, { passive: true });
    function resumePaint() {
      lastDraw = -Infinity;
      requestPaint();
    }
    document.addEventListener('visibilitychange', resumePaint);
    if (motion.addEventListener) motion.addEventListener('change', resumePaint);
    else motion.addListener(resumePaint);
    document.fonts?.ready.then(requestPaint);
    resize();
  }

  startPageField();

  function renderer(canvas, ctx, model) {
    const cellWidth = CELL_WIDTH, cellHeight = CELL_HEIGHT;
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
      let scale = Math.min(width * 1.1, height * 1.25) / model.size;
      // Fit the rotated silhouette while keeping the glyphs themselves the same size.
      for (const [x, y, z] of model.bounds(time, state)) {
        const rx = x * yawCos + z * yawSin;
        const rz = z * yawCos - x * yawSin;
        const ry = y * pitchCos - rz * pitchSin;
        const perspective = 8 / (8 - y * pitchSin - rz * pitchCos);
        scale = Math.min(scale, (width / 2 - CELL_WIDTH) / Math.abs(rx * perspective),
          (height / 2 - CELL_HEIGHT) / Math.abs(ry * perspective));
      }
      const ox = (width - cols * cellWidth) / 2;
      const oy = (height - rows * cellHeight) / 2;
      ctx.font = `${GLYPH_SIZE}px ${font || 'monospace'}`;
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
    const status = figure.querySelector('[role="status"]');
    const view = renderer(canvas, ctx, model);
    const state = {
      yaw: model.yaw, pitch: model.pitch, ambient: 0, pattern: 'steady',
      signal: null, signalDone: false, turns: 0, turn: null,
    };
    let inView = false;
    let introInView = false;
    let introSpin = true;
    let introElapsed = 0;
    let drag = null;
    let announceFrame = 0;
    const announce = message => {
      cancelAnimationFrame(announceFrame);
      status.textContent = '';
      announceFrame = requestAnimationFrame(() => { status.textContent = message; });
    };
    const canAnimate = () => !motion.matches && inView && !document.hidden;
    const running = () => canAnimate() && (state.ambient < AMBIENT_LIMIT || introSpin && introInView
      || state.turn || state.signal !== null && !state.signalDone);
    const finishTurn = () => {
      if (!state.turn) return;
      state.turns = (state.turns + 1) % 4;
      announce(figure.dataset.complete);
      state.turn = null;
    };
    const finishSignal = () => {
      if (state.signal === null || state.signalDone) return;
      state.signalDone = true;
      announce(figure.dataset.complete);
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
      if (introSpin && introInView) {
        introElapsed += step;
        const progress = Math.min(1, introElapsed / INTRO_SPIN_DURATION);
        introSpin = progress < 1;
        const eased = progress - 0.85 * Math.sin(FULL_TURN * progress) / FULL_TURN;
        state.yaw = introSpin ? model.yaw + FULL_TURN * eased : model.yaw;
      }
      if (state.turn && now - state.turn.start >= 410) finishTurn();
      if (state.signal !== null && now - state.signal >= 960) finishSignal();
      draw(now);
    }

    function move(dx, dy) {
      introSpin = false;
      state.yaw = (state.yaw + dx) % FULL_TURN;
      state.pitch = clamp(state.pitch + dy, -Math.PI, Math.PI);
      draw(performance.now());
    }

    function activate() {
      introSpin = false;
      const now = performance.now();
      switch (figure.dataset.model) {
        case 'technology':
          state.signal = canAnimate() ? now : now - 960;
          state.signalDone = false;
          if (!canAnimate()) finishSignal();
          break;
        case 'music':
          state.pattern = state.pattern === 'steady' ? 'syncopated' : 'steady';
          announce(state.pattern === 'steady' ? figure.dataset.complete : figure.dataset.altComplete);
          break;
        case 'cubing':
          finishTurn();
          state.turn = { start: now };
          if (!canAnimate()) finishTurn();
          break;
      }
      draw(now);
      schedule();
    }

    stage.addEventListener('pointerdown', event => {
      if (!event.isPrimary || event.button !== 0) return;
      introSpin = false;
      drag = { id: event.pointerId, x: event.clientX, y: event.clientY, moved: false };
      stage.setPointerCapture(event.pointerId);
    });
    stage.addEventListener('pointermove', event => {
      if (!drag || event.pointerId !== drag.id) return;
      const dx = event.clientX - drag.x;
      const dy = event.clientY - drag.y;
      if (!drag.moved && Math.hypot(dx, dy) < 5) return;
      drag.moved = true;
      stage.classList.add('is-dragging');
      move(dx * 0.012, event.pointerType === 'touch' ? 0 : dy * 0.012);
      drag.x = event.clientX;
      drag.y = event.clientY;
    });
    function endDrag(event) {
      if (event.pointerId !== drag?.id) return;
      const tap = event.type === 'pointerup' && !drag.moved;
      drag = null;
      stage.classList.remove('is-dragging');
      if (tap) activate();
    }
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(type => stage.addEventListener(type, endDrag));
    stage.addEventListener('keydown', event => {
      if (event.altKey || event.metaKey || event.ctrlKey) return;
      switch (event.key) {
        case 'ArrowLeft': move(-0.24, 0); break;
        case 'ArrowRight': move(0.24, 0); break;
        case 'ArrowUp': move(0, 0.24); break;
        case 'ArrowDown': move(0, -0.24); break;
        case 'Home':
          introSpin = false;
          state.yaw = model.yaw;
          state.pitch = model.pitch;
          draw(performance.now());
          break;
        case 'Enter':
        case ' ':
          if (!event.repeat) activate();
          break;
        default: return;
      }
      event.preventDefault();
    });
    stage.addEventListener('click', event => {
      // An assistive activation has no pointer sequence.
      if (event.detail === 0) activate();
    });

    canvas.hidden = false;
    figure.querySelector('.model-fallback').hidden = true;
    const help = figure.querySelector('[id$="-model-help"]');
    help.hidden = false;
    stage.tabIndex = 0;
    stage.setAttribute('role', 'button');
    stage.setAttribute('aria-describedby', help.id);
    stage.classList.add('is-interactive');
    const resize = () => { view.resize(); draw(performance.now()); };
    resize();
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
    else window.addEventListener('resize', resize, { passive: true });
    document.fonts?.ready.then(resize);
    const motionChanged = () => {
      if (introInView && motion.matches) introSpin = false;
      if (!canAnimate()) settle();
      schedule();
    };
    if (motion.addEventListener) motion.addEventListener('change', motionChanged);
    else motion.addListener(motionChanged);
    document.addEventListener('visibilitychange', motionChanged);

    const instance = {
      running, update,
      show(fraction) {
        inView = fraction >= ACTIVE_VISIBLE_FRACTION;
        introInView = fraction >= INTRO_VISIBLE_FRACTION;
        if (introInView && motion.matches) introSpin = false;
        if (!inView) settle();
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
      entries.forEach(entry => rendered.get(entry.target).show(entry.isIntersecting ? entry.intersectionRatio : 0));
    }, { threshold: [ACTIVE_VISIBLE_FRACTION, INTRO_VISIBLE_FRACTION] });
    rendered.forEach((_, canvas) => observer.observe(canvas));
  } else {
    // Explicit actions still work when viewport observation is unavailable.
    rendered.forEach(instance => instance.show(0));
  }
})();
