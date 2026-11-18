(() => {
  const scene = document.querySelector('[data-social-orbit]');
  if (!scene) return;

  const svg = scene.querySelector('.social-orbit__svg');
  const rail = svg?.querySelector('.social-orbit__rail');
  const nodes = [...scene.querySelectorAll('.social-orbit__node')];
  if (!svg || !rail || !nodes.length) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 600px)');
  const message = scene.querySelector('.social-orbit__message');
  const desktopPath = 'M90 470 A410 410 0 0 1 910 470';
  const mobilePath = 'M18 232 A162 162 0 0 1 342 232';
  let length = 0;
  let raf = 0;
  let visible = true;
  let lastTime = 0;

  if (message && !reducedMotion.matches) {
    message.classList.add('orbit-ready');
    const messageObserver = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      message.classList.add('is-visible');
      messageObserver.disconnect();
    }, { threshold: 0.35 });
    messageObserver.observe(message);
  }

  const setGeometry = () => {
    const isMobile = mobile.matches;
    const width = isMobile ? 360 : 1000;
    const height = isMobile ? 260 : 520;
    const path = isMobile ? mobilePath : desktopPath;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    rail.setAttribute('d', path);
    svg.querySelector('.social-orbit__rail-shadow')?.setAttribute('d', path);
    length = rail.getTotalLength();
    place(0);
  };

  const place = (time) => {
    const duration = 26000;
    const progress = reducedMotion.matches ? 0.08 : (time % duration) / duration;
    const count = nodes.length;
    nodes.forEach((node, index) => {
      // Each mark moves the same measured distance per frame and remains upright.
      const p = (progress + index / count) % 1;
      const point = rail.getPointAtLength(p * length);
      const depth = 0.76 + 0.25 * Math.sin(Math.PI * p);
      const edge = Math.min(p, 1 - p);
      const opacity = reducedMotion.matches ? 1 : Math.min(1, edge / 0.075);
      node.style.left = `${(point.x / (mobile.matches ? 360 : 1000)) * 100}%`;
      node.style.top = `${(point.y / (mobile.matches ? 260 : 520)) * 100}%`;
      node.style.setProperty('--depth', depth.toFixed(3));
      node.style.setProperty('--orbit-opacity', opacity.toFixed(3));
      node.style.zIndex = String(Math.round(depth * 10));
    });
  };

  const tick = (now) => {
    raf = 0;
    if (!visible || document.hidden || reducedMotion.matches) return;
    if (!lastTime) lastTime = now;
    place(now % 26000);
    raf = requestAnimationFrame(tick);
  };

  const start = () => {
    if (!visible || document.hidden || reducedMotion.matches || raf) return;
    raf = requestAnimationFrame(tick);
  };
  const stop = () => {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    lastTime = 0;
  };
  const onMotionChange = () => {
    if (reducedMotion.matches) {
      stop();
      place(0);
    } else start();
  };

  setGeometry();
  const observer = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    visible ? start() : stop();
  }, { threshold: 0 });
  observer.observe(scene);
  window.addEventListener('resize', setGeometry, { passive: true });
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
  reducedMotion.addEventListener?.('change', onMotionChange);
  if (reducedMotion.matches) place(0);
})();
