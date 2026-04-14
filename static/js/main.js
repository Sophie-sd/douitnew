const SELECTORS = {
  menuToggle: "[data-menu-toggle]",
  menuClose: "[data-menu-close]",
  mobileMenu: "#mobile-menu",
  stickyCta: "#sticky-cta",
  hero: ".hero, .service-hero",
  reveal: ".reveal, .reveal--slide-left, .reveal--scale",
  faqToggle: "[data-faq-toggle]",
  utmFields: "[data-utm]",
  openModal: "[data-open-modal]",
  closeModal: "[data-close-modal]",
  leadModal: "#lead-modal",
  openContact: "[data-open-contact]",
  contactModal: "#contact-modal",
  phoneUa: "[data-phone-ua]",
};

let menuAc = null;
function initMobileMenu() {
  menuAc?.abort();
  menuAc = new AbortController();
  const { signal } = menuAc;

  const toggle = document.querySelector(SELECTORS.menuToggle);
  const menu = document.querySelector(SELECTORS.mobileMenu);
  if (!toggle || !menu) return;

  const open = () => {
    menu.classList.add("is-open");
    menu.setAttribute("aria-hidden", "false");
    toggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  };

  const close = () => {
    menu.classList.remove("is-open");
    menu.setAttribute("aria-hidden", "true");
    toggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };

  toggle.addEventListener("click", open, { signal });

  menu.querySelectorAll(SELECTORS.menuClose).forEach((el) => {
    el.addEventListener("click", close, { signal });
  });

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", close, { signal });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.classList.contains("is-open")) close();
  }, { signal });
}

let stickyObserver = null;
function initStickyCta() {
  stickyObserver?.disconnect();
  stickyObserver = null;

  const stickyCta = document.querySelector(SELECTORS.stickyCta);
  const hero = document.querySelector(SELECTORS.hero);
  if (!stickyCta || !hero) return;

  stickyObserver = new IntersectionObserver(
    ([entry]) => {
      const show = !entry.isIntersecting;
      stickyCta.classList.toggle("is-visible", show);
      stickyCta.setAttribute("aria-hidden", String(!show));
    },
    { threshold: 0 }
  );
  stickyObserver.observe(hero);
}

function assignStaggerIndices() {
  const groups = new Map();
  document.querySelectorAll(SELECTORS.reveal).forEach((el) => {
    const parent = el.parentElement;
    if (!parent) return;
    if (!groups.has(parent)) groups.set(parent, []);
    groups.get(parent).push(el);
  });
  groups.forEach((children) => {
    children.forEach((el, i) => {
      el.style.setProperty("--reveal-i", String(i));
    });
  });
}

function initReveal() {
  const els = document.querySelectorAll(SELECTORS.reveal);
  if (!els.length) return;

  assignStaggerIndices();

  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  if (prefersReduced) {
    els.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const revealed = new Set();

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const parent = el.parentElement;

        if (parent && !revealed.has(parent)) {
          revealed.add(parent);
          const siblings = parent.querySelectorAll(
            ":scope > .reveal, :scope > .reveal--slide-left, :scope > .reveal--scale"
          );
          siblings.forEach((sib) => {
            sib.classList.add("is-visible");
            observer.unobserve(sib);
          });
        } else {
          el.classList.add("is-visible");
          observer.unobserve(el);
        }
      });
    },
    { threshold: 0.08, rootMargin: "0px 0px -30px 0px" }
  );
  els.forEach((el) => observer.observe(el));
}

function initFaqAccordion() {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(SELECTORS.faqToggle);
    if (!btn) return;
    const item = btn.closest(".faq-item");
    if (!item) return;
    const isOpen = item.classList.toggle("is-open");
    btn.setAttribute("aria-expanded", String(isOpen));
  });
}

function initUtmCapture() {
  const params = new URLSearchParams(window.location.search);
  const utmKeys = ["utm_source", "utm_medium", "utm_campaign"];

  utmKeys.forEach((key) => {
    const val = params.get(key);
    if (val) {
      try {
        sessionStorage.setItem(key, val);
      } catch {
        /* storage unavailable */
      }
    }
  });

  fillUtmFields();
}

function fillUtmFields() {
  document.querySelectorAll(SELECTORS.utmFields).forEach((input) => {
    const key = input.dataset.utm;
    if (key === "url") {
      input.value = window.location.href;
      return;
    }
    try {
      input.value = sessionStorage.getItem(`utm_${key}`) ?? "";
    } catch {
      /* noop */
    }
  });
}

function initModalDelegation() {
  document.addEventListener("click", (e) => {
    const openModalTrigger = e.target.closest(SELECTORS.openModal);
    if (openModalTrigger) {
      e.preventDefault();
      const dialog = document.querySelector(SELECTORS.leadModal);
      if (!dialog) return;
      resetQuiz(dialog);
      dialog.showModal();
      fillUtmFields();
      return;
    }

    const openContactTrigger = e.target.closest(SELECTORS.openContact);
    if (openContactTrigger) {
      e.preventDefault();
      const dialog = document.querySelector(SELECTORS.contactModal);
      if (!dialog) return;
      dialog.showModal();
      fillUtmFields();
      initPhoneMask();
      return;
    }

    if (e.target.closest(SELECTORS.closeModal)) {
      e.target.closest("dialog")?.close();
      return;
    }

    if (e.target.tagName === "DIALOG" && e.target.open) {
      e.target.close();
    }
  });
}

function resetQuiz(container) {
  const quiz = container?.querySelector("[data-quiz]") ?? container;
  if (!quiz) return;
  quizAnswers.clear();
  quiz.querySelectorAll(".quiz__step").forEach((step, i) => {
    step.classList.toggle("is-active", i === 0);
  });
  quiz.querySelectorAll(".quiz__option").forEach((opt) => {
    opt.classList.remove("is-selected");
  });
  quiz.querySelectorAll("[data-quiz-next]").forEach((btn) => {
    const step = btn.closest(".quiz__step");
    const mode = step?.querySelector("[data-quiz-mode]")?.dataset.quizMode;
    btn.disabled = mode !== "checkbox";
  });
  updateQuizProgress(quiz);
}

const quizAnswers = new Map();
const TOTAL_STEPS = 6;

function updateQuizProgress(quiz) {
  const activeStep = quiz.querySelector(".quiz__step.is-active");
  const stepNum = parseInt(activeStep?.dataset.quizStep ?? "1", 10);
  const bar = quiz.querySelector("[data-quiz-progress]");
  const text = quiz.querySelector("[data-quiz-progress-text]");
  if (bar) bar.style.width = `${(stepNum / TOTAL_STEPS) * 100}%`;
  if (text) text.textContent = `Крок ${stepNum} з ${TOTAL_STEPS}`;
}

function goToStep(quiz, stepNum) {
  quiz.querySelectorAll(".quiz__step").forEach((s) => {
    s.classList.toggle("is-active", parseInt(s.dataset.quizStep, 10) === stepNum);
  });
  updateQuizProgress(quiz);
  if (stepNum === TOTAL_STEPS) {
    writeQuizHiddenFields(quiz);
    initPhoneMask();
    fillUtmFields();
  }
}

function writeQuizHiddenFields(quiz) {
  quiz.querySelectorAll("[data-quiz-hidden]").forEach((input) => {
    const field = input.dataset.quizHidden;
    const val = quizAnswers.get(field);
    input.value = Array.isArray(val) ? val.join(", ") : (val ?? "");
  });
}

function initQuiz() {
  document.addEventListener("click", (e) => {
    const optBtn = e.target.closest(".quiz__option");
    if (optBtn) {
      handleQuizOptionClick(optBtn);
      return;
    }
    const nextBtn = e.target.closest("[data-quiz-next]");
    if (nextBtn && !nextBtn.disabled) {
      const quiz = nextBtn.closest("[data-quiz]");
      const step = nextBtn.closest(".quiz__step");
      const current = parseInt(step.dataset.quizStep, 10);
      if (current < TOTAL_STEPS) goToStep(quiz, current + 1);
      return;
    }
    const prevBtn = e.target.closest("[data-quiz-prev]");
    if (prevBtn) {
      const quiz = prevBtn.closest("[data-quiz]");
      const step = prevBtn.closest(".quiz__step");
      const current = parseInt(step.dataset.quizStep, 10);
      if (current > 1) goToStep(quiz, current - 1);
      return;
    }
    const skipBtn = e.target.closest("[data-quiz-skip]");
    if (skipBtn) {
      const quiz = skipBtn.closest("[data-quiz]");
      const step = skipBtn.closest(".quiz__step");
      const current = parseInt(step.dataset.quizStep, 10);
      if (current < TOTAL_STEPS) goToStep(quiz, current + 1);
    }
  });

  document.querySelectorAll("[data-quiz]").forEach((quiz) => {
    updateQuizProgress(quiz);
  });
}

function handleQuizOptionClick(optBtn) {
  const group = optBtn.closest("[data-quiz-field]");
  if (!group) return;
  const field = group.dataset.quizField;
  const mode = group.dataset.quizMode;
  const value = optBtn.dataset.quizValue;

  if (mode === "checkbox") {
    optBtn.classList.toggle("is-selected");
    const selected = [...group.querySelectorAll(".quiz__option.is-selected")]
      .map((o) => o.dataset.quizValue);
    quizAnswers.set(field, selected);
  } else {
    group.querySelectorAll(".quiz__option").forEach((o) => o.classList.remove("is-selected"));
    optBtn.classList.add("is-selected");
    quizAnswers.set(field, value);
  }

  const step = group.closest(".quiz__step");
  const nextBtn = step?.querySelector("[data-quiz-next]");
  if (nextBtn && mode !== "checkbox") {
    nextBtn.disabled = false;
  }
}

function initPhoneMask() {
  document.querySelectorAll(SELECTORS.phoneUa).forEach((input) => {
    if (input.dataset.phoneMasked) return;
    input.dataset.phoneMasked = "true";

    const formatPhone = (raw) => {
      let digits = raw.replace(/\D/g, "");

      if (digits.startsWith("380")) digits = digits.slice(2);
      else if (digits.startsWith("38")) digits = digits.slice(2);
      else if (digits.startsWith("80")) digits = `0${digits.slice(2)}`;

      if (digits.length > 0 && digits[0] !== "0") {
        digits = `0${digits}`;
      }

      const userDigits = digits.slice(0, 10);
      let result = "+38(";
      if (userDigits.length > 0) result += userDigits.slice(0, 3);
      if (userDigits.length >= 3) result += ")";
      if (userDigits.length > 3) result += userDigits.slice(3, 6);
      if (userDigits.length > 6) result += `-${userDigits.slice(6, 8)}`;
      if (userDigits.length > 8) result += `-${userDigits.slice(8, 10)}`;
      return result;
    };

    input.addEventListener("input", () => {
      const pos = input.selectionStart;
      const before = input.value.length;
      input.value = formatPhone(input.value);
      const after = input.value.length;
      const newPos = Math.max(3, pos + (after - before));
      input.setSelectionRange(newPos, newPos);
    });

    input.addEventListener("focus", () => {
      if (!input.value) {
        input.value = "+38(";
      }
    });

    input.addEventListener("keydown", (e) => {
      const cursorPos = input.selectionStart ?? 0;
      if (e.key === "Backspace" && cursorPos <= 3) {
        e.preventDefault();
      }
      if (e.key === "Delete" && cursorPos < 3) {
        e.preventDefault();
      }
    });

    if (!input.value) {
      input.value = "+38(";
    } else {
      input.value = formatPhone(input.value);
    }
  });
}

let parallaxAc = null;
function initParallax() {
  parallaxAc?.abort();
  parallaxAc = null;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const items = document.querySelectorAll("[data-parallax]");
  if (!items.length) return;

  parallaxAc = new AbortController();
  const { signal } = parallaxAc;

  const update = () => {
    const y = window.scrollY;
    items.forEach((el) => {
      const speed = parseFloat(el.dataset.parallax ?? "0");
      el.style.setProperty("--py", `${y * speed}px`);
    });
  };

  update();

  let ticking = false;
  window.addEventListener(
    "scroll",
    () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        update();
        ticking = false;
      });
    },
    { passive: true, signal }
  );
}

function reinit() {
  initMobileMenu();
  initStickyCta();
  initReveal();
  initParallax();
  initPhoneMask();
  fillUtmFields();
  initUtmCapture();
}

function initHtmxEvents() {
  document.addEventListener("htmx:afterSwap", reinit);
  document.addEventListener("htmx:historyRestore", reinit);
}

function init() {
  document.body.classList.add("js-ready");
  initMobileMenu();
  initStickyCta();
  initReveal();
  initFaqAccordion();
  initUtmCapture();
  initParallax();
  initHtmxEvents();
  initModalDelegation();
  initPhoneMask();
  initQuiz();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
