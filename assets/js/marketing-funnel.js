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
  let frame = 0;
  let currentStage = -1;

  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));

  function update() {
    frame = 0;
    const sticky = section.querySelector(".marketing-funnel__sticky");
    const travel = Math.max(1, section.offsetHeight - sticky.offsetHeight);
    const progress = clamp(-section.getBoundingClientRect().top / travel);

    section.classList.toggle("is-progressing", progress > 0.005);
    const activeStage = progress <= 0.005 ? 0 : Math.min(3, Math.ceil(progress * 4));
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

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate, { passive: true });
  requestUpdate();
})();
