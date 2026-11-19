/* BEINTOX — site runtime. Progressive enhancement only; every page works without JS. */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* Mobile nav */
  const nav = $(".nav"), toggle = $(".nav__toggle");
  if (nav && toggle) {
    const set = (open) => { nav.classList.toggle("is-open", open); toggle.setAttribute("aria-expanded", String(open)); };
    toggle.addEventListener("click", () => set(!nav.classList.contains("is-open")));
    addEventListener("keydown", (e) => e.key === "Escape" && set(false));
    $$(".nav__links a").forEach((a) => a.addEventListener("click", () => set(false)));
  }

  /* Match the header wordmark to the page surface behind the transparent nav. */
  const navLogo = nav && $(".logo__adaptive", nav);
  if (navLogo) {
    const rgbLuminance = (value) => {
      const match = value.match(/rgba?\(([^)]+)\)/i);
      if (!match) return null;
      const values = match[1].split(/[,/\s]+/).filter(Boolean).map(Number);
      if (values.length < 3 || values.slice(0, 3).some(Number.isNaN)) return null;
      const channels = values.slice(0, 3).map((v) => {
        v /= 255;
        return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
      });
      return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2];
    };
    const surfaceLuminance = (element) => {
      for (let node = element; node && node !== document.documentElement; node = node.parentElement) {
        const style = getComputedStyle(node);
        const color = style.backgroundColor.match(/rgba?\(([^)]+)\)/i);
        if (color) {
          const parts = color[1].split(/[,/\s]+/).filter(Boolean).map(Number);
          const alpha = parts.length > 3 && Number.isFinite(parts[3]) ? parts[3] : 1;
          if (alpha > .1) {
            const luminance = rgbLuminance(style.backgroundColor);
            if (luminance !== null) return luminance;
          }
        }
        if (style.backgroundImage && style.backgroundImage !== "none") {
          const colors = style.backgroundImage.match(/rgba?\([^)]+\)|#[\da-f]{3,8}\b/gi) || [];
          const values = colors.map((c) => {
            if (c.startsWith("#")) {
              let h = c.slice(1);
              if (h.length === 3 || h.length === 4) h = [...h].map((x) => x + x).join("");
              return rgbLuminance(`rgb(${parseInt(h.slice(0, 2), 16)}, ${parseInt(h.slice(2, 4), 16)}, ${parseInt(h.slice(4, 6), 16)})`);
            }
            return rgbLuminance(c);
          }).filter((n) => n !== null);
          if (values.length) return values.reduce((sum, n) => sum + n, 0) / values.length;
        }
      }
      return 1;
    };
    let contrastFrame = 0;
    const updateLogoContrast = () => {
      cancelAnimationFrame(contrastFrame);
      contrastFrame = requestAnimationFrame(() => {
        const rect = navLogo.getBoundingClientRect();
        const oldVisibility = nav.style.visibility;
        nav.style.visibility = "hidden";
        let underlay;
        try { underlay = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2); }
        finally { nav.style.visibility = oldVisibility; }
        nav.classList.toggle("nav--light-underlay", surfaceLuminance(underlay) > .52);
      });
    };
    addEventListener("scroll", updateLogoContrast, { passive: true });
    addEventListener("resize", updateLogoContrast);
    addEventListener("load", updateLogoContrast, { once: true });
    updateLogoContrast();
  }

  /* Lightbox: any [data-lb] link inside a [data-lb-group] container */
  const lb = $("#lb");
  if (lb && typeof lb.showModal === "function") {
    const img = $("img", lb), cap = $("span", lb);
    let list = [], i = 0;
    const show = (n) => {
      i = (n + list.length) % list.length;
      const a = list[i], thumb = $("img", a);
      img.src = a.href; img.alt = thumb ? thumb.alt : "";
      cap.textContent = `${a.dataset.lb || img.alt}  ·  ${i + 1} / ${list.length}`;
    };
    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[data-lb]");
      if (!a || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      list = $$("a[data-lb]", a.closest("[data-lb-group]") || document);
      show(list.indexOf(a)); lb.showModal();
    });
    $("[data-prev]", lb).addEventListener("click", () => show(i - 1));
    $("[data-next]", lb).addEventListener("click", () => show(i + 1));
    $("[data-close]", lb).addEventListener("click", () => lb.close());
    lb.addEventListener("click", (e) => e.target === lb && lb.close());
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
    lb.addEventListener("close", () => img.removeAttribute("src"));
  }

  /* Contact form → WhatsApp or email with the brief pre-filled (no backend required) */
  const form = $("#brief");
  if (form) {
    const compose = () => {
      const d = new FormData(form);
      const services = d.getAll("services").join(", ") || "Not sure yet";
      return [
        `Hi BEINTOX, I'd like to discuss a project.`, ``,
        `Name: ${d.get("name")}`,
        `Business: ${d.get("business") || "-"}`,
        `Contact: ${d.get("contact")}`,
        `Interested in: ${services}`,
        `Timeline: ${d.get("timeline")}`, ``,
        `${d.get("message") || ""}`,
      ].join("\n").trim();
    };
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const via = e.submitter && e.submitter.value === "email" ? "email" : "whatsapp";
      const text = compose();
      const url = via === "email"
        ? `mailto:${form.dataset.email}?subject=${encodeURIComponent("Project enquiry — " + (new FormData(form).get("business") || new FormData(form).get("name")))}&body=${encodeURIComponent(text)}`
        : `https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(text)}`;
      if (via === "email") location.href = url; else window.open(url, "_blank", "noopener");
    });
  }

  /* Newsletter requests open a prefilled email to the BEINTOX inbox. */
  const subscribeForm = $(".subscribe-form");
  if (subscribeForm) {
    subscribeForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!subscribeForm.reportValidity()) return;
      const email = new FormData(subscribeForm).get("email");
      const subject = encodeURIComponent("BEINTOX newsletter subscription");
      const body = encodeURIComponent(`Please add ${email} to the BEINTOX newsletter.`);
      location.href = `mailto:${subscribeForm.dataset.email}?subject=${subject}&body=${body}`;
    });
  }

  /* Home page work reel: pause, step through cards and open a full-screen player. */
  const workReel = $("[data-work-reel]");
  if (workReel) {
    const track = $(".reel__track", workReel);
    const viewport = $(".reel--work", workReel);
    const toggle = $("[data-work-toggle]", workReel);
    const dialog = $(".work-lightbox", workReel);
    const player = $("video", dialog);
    let wasPausedBeforeDialog = false;

    const setPaused = (paused) => {
      track.classList.toggle("is-paused", paused);
      toggle.classList.toggle("is-paused", paused);
      toggle.setAttribute("aria-label", paused ? "Play video slider" : "Pause video slider");
      toggle.setAttribute("aria-pressed", String(paused));
    };

    toggle.addEventListener("click", () => setPaused(!track.classList.contains("is-paused")));
    const step = (direction) => {
      const animation = track.getAnimations().find((item) => item.animationName === "marquee");
      const firstCard = $("[data-work-video]", track);
      if (!animation || !firstCard) {
        const distance = firstCard ? firstCard.getBoundingClientRect().width + 16 : 300;
        viewport.scrollBy({ left: direction * distance, behavior: still ? "auto" : "smooth" });
        return;
      }
      const duration = Number(animation.effect.getTiming().duration);
      const cycleWidth = track.scrollWidth / 2;
      const stride = firstCard.getBoundingClientRect().width + (parseFloat(getComputedStyle(track).columnGap) || 16);
      const offset = duration * stride / cycleWidth;
      const current = Number(animation.currentTime) || 0;
      animation.currentTime = (current + direction * offset + duration) % duration;
    };
    $("[data-work-prev]", workReel).addEventListener("click", () => step(-1));
    $("[data-work-next]", workReel).addEventListener("click", () => step(1));

    $$('[data-work-video]', workReel).forEach((card) => card.addEventListener("click", () => {
      wasPausedBeforeDialog = track.classList.contains("is-paused");
      setPaused(true);
      player.src = card.dataset.workVideo;
      player.poster = card.dataset.workPoster;
      dialog.showModal();
      player.play().catch(() => {});
    }));
    $("[data-work-close]", dialog).addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener("close", () => {
      player.pause();
      player.removeAttribute("src");
      player.removeAttribute("poster");
      player.load();
      if (!wasPausedBeforeDialog) setPaused(false);
    });
  }

  /* Reveal cards once as they scroll in, and count numbers up from 0 */
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const reveals = $$(".rv"), counters = $$("[data-count]");
  const count = (el) => {
    const end = +el.dataset.count, t0 = performance.now(), dur = 1800;
    const tick = (now) => {
      const p = Math.min((now - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if (still || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("in"));
  } else {
    counters.forEach((el) => (el.textContent = "0"));
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      if (e.target.matches("[data-count]")) count(e.target); else e.target.classList.add("in");
    }), { threshold: 0.2 });
    reveals.forEach((el) => io.observe(el));
    counters.forEach((el) => io.observe(el));
  }

  /* On phones only, reveal the home process cards from alternating sides as they enter view. */
  const mobileProcess = matchMedia("(max-width: 767px)");
  const processCards = $$(".home-process .process-card");
  if (mobileProcess.matches && processCards.length && !still && "IntersectionObserver" in window) {
    document.documentElement.classList.add("mobile-process-motion");
    const processObserver = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-mobile-entered");
      processObserver.unobserve(entry.target);
    }), { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    processCards.forEach((card) => processObserver.observe(card));
  } else if (mobileProcess.matches) {
    processCards.forEach((card) => card.classList.add("is-mobile-entered"));
  }

  /* Services-only mobile testimonial carousel: one equal-size card stays centered. */
  const servicesClientCarousel = $("body.page-services .client-videos");
  const servicesClientMobile = matchMedia("(max-width: 767px)");
  if (servicesClientCarousel && servicesClientMobile.matches) {
    const viewport = $(".client-videos__viewport", servicesClientCarousel);
    const track = $(".client-videos__track", servicesClientCarousel);
    const cards = $$(".client-videos__set:not(.client-videos__set--clone) .client-video", servicesClientCarousel);
    let activeIndex = 0;
    let timer = 0;
    let resetTimer = 0;

    const getStep = () => {
      const card = cards[0];
      const set = $(".client-videos__set", track);
      if (!card || !set) return 0;
      return card.getBoundingClientRect().width + parseFloat(getComputedStyle(set).columnGap || "0");
    };
    const placeCard = (index, instant = false) => {
      track.classList.toggle("is-resetting", instant);
      track.style.transform = `translate3d(${-getStep() * index}px, 0, 0)`;
      if (instant) requestAnimationFrame(() => requestAnimationFrame(() => track.classList.remove("is-resetting")));
    };
    const stop = () => {
      window.clearInterval(timer);
      window.clearTimeout(resetTimer);
      timer = 0;
    };
    const start = () => {
      stop();
      if (document.hidden || still || !servicesClientMobile.matches) return;
      timer = window.setInterval(() => {
        activeIndex += 1;
        placeCard(activeIndex);
        if (activeIndex === cards.length) {
          activeIndex = 0;
          resetTimer = window.setTimeout(() => placeCard(0, true), 720);
        }
      }, 4200);
    };

    placeCard(0, true);
    start();
    addEventListener("resize", () => placeCard(activeIndex, true), { passive: true });
    document.addEventListener("visibilitychange", () => document.hidden ? stop() : start());
    servicesClientMobile.addEventListener?.("change", (event) => {
      if (event.matches) { placeCard(activeIndex, true); start(); }
      else stop();
    });
    let touchStartX = 0;
    viewport.addEventListener("touchstart", (event) => { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
    viewport.addEventListener("touchend", (event) => {
      const delta = event.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) < 45) return;
      activeIndex = (activeIndex + (delta < 0 ? 1 : cards.length - 1)) % cards.length;
      placeCard(activeIndex, activeIndex === 0);
      start();
    }, { passive: true });
  }

  /* 3D tilt + moving light on [data-tilt] (founder portrait) */
  if (!still && matchMedia("(hover: hover)").matches) {
    $$("[data-tilt]").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.classList.add("is-tilting");
        el.style.setProperty("--ry", `${(x - 0.5) * 12}deg`);
        el.style.setProperty("--rx", `${(0.5 - y) * 12}deg`);
        el.style.setProperty("--mx", `${x * 100}%`);
        el.style.setProperty("--my", `${y * 100}%`);
      });
      el.addEventListener("pointerleave", () => {
        el.classList.remove("is-tilting");
        el.style.setProperty("--rx", "0deg"); el.style.setProperty("--ry", "0deg");
      });
    });
  }

  const y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
