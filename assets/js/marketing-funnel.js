(() => {
  const section = document.querySelector("[data-marketing-funnel]");
  if (!section) return;

  // Illustrative placeholders only. Replace with verified reporting when available.
  const metrics = [1_284_300, 48_120, 2_940, 312];
  const stageEls = [...section.querySelectorAll("[data-funnel-stage]")];
  const metricEls = [...section.querySelectorAll("[data-funnel-metric]")];
  const counters = [...section.querySelectorAll("[data-funnel-counter]")];
  const clips = [...section.querySelectorAll("[data-funnel-clip]")];
  const formatter = new Intl.NumberFormat("en-US");
  const mobileViewport = window.matchMedia("(max-width: 600px)");
  let frame = 0;
  let currentStage = -1;
  let mobileScrollBound = false;
  const scrollRoot = document.scrollingElement || document.documentElement;

  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));

  function update() {
    frame = 0;
    const sticky = section.querySelector(".marketing-funnel__sticky");
    const travel = Math.max(1, section.offsetHeight - sticky.offsetHeight);
    const stickyTop = mobileViewport.matches ? (parseFloat(getComputedStyle(sticky).top) || 0) : 0;
    const sectionTop = mobileViewport.matches
      ? section.getBoundingClientRect().top + scrollRoot.scrollTop
      : 0;
    const progress = mobileViewport.matches
      ? clamp((scrollRoot.scrollTop - sectionTop + stickyTop) / travel)
      : clamp(-section.getBoundingClientRect().top / travel);

    section.classList.toggle("is-progressing", progress > 0.005);
    const activeStage = mobileViewport.matches
      ? Math.min(3, Math.floor(progress * 4))
      : progress <= 0.005 ? 0 : Math.min(3, Math.ceil(progress * 4));
    if (activeStage !== currentStage) {
      currentStage = activeStage;
      stageEls.forEach((stage, i) => {
        stage.classList.toggle("is-active", i === activeStage);
        stage.setAttribute("aria-current", i === activeStage ? "step" : "false");
      });
    }

    clips.forEach((rect, i) => {
      const amount = clamp(progress * 4 - i);
      rect.setAttribute("height", String(132 * amount));
      counters[i].textContent = formatter.format(Math.round(metrics[i] * amount));
      metricEls[i].classList.toggle("is-active", amount > 0);
    });
  }

  function requestUpdate() {
    if (!frame) frame = requestAnimationFrame(update);
  }

  function bindMobileScroll() {
    if (mobileViewport.matches === mobileScrollBound) return;
    mobileScrollBound = mobileViewport.matches;
    if (mobileScrollBound) {
      document.addEventListener("scroll", requestUpdate, { passive: true, capture: true });
      scrollRoot.addEventListener("scroll", requestUpdate, { passive: true });
      document.addEventListener("touchmove", requestUpdate, { passive: true, capture: true });
      window.visualViewport?.addEventListener("scroll", requestUpdate, { passive: true });
      window.visualViewport?.addEventListener("resize", requestUpdate, { passive: true });
      window.addEventListener("pageshow", requestUpdate, { passive: true });
      window.addEventListener("orientationchange", requestUpdate, { passive: true });
    } else {
      document.removeEventListener("scroll", requestUpdate, true);
      scrollRoot.removeEventListener("scroll", requestUpdate);
      document.removeEventListener("touchmove", requestUpdate, true);
      window.visualViewport?.removeEventListener("scroll", requestUpdate);
      window.visualViewport?.removeEventListener("resize", requestUpdate);
      window.removeEventListener("pageshow", requestUpdate);
      window.removeEventListener("orientationchange", requestUpdate);
    }
    requestUpdate();
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", () => {
    bindMobileScroll();
    requestUpdate();
  }, { passive: true });
  mobileViewport.addEventListener?.("change", bindMobileScroll);
  if ("ResizeObserver" in window) {
    const resizeObserver = new ResizeObserver(requestUpdate);
    resizeObserver.observe(section);
    resizeObserver.observe(section.querySelector(".marketing-funnel__sticky"));
  }
  bindMobileScroll();
  requestUpdate();
})();
