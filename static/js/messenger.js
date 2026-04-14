let fabAc = null;
function initMessengerFab() {
  fabAc?.abort();
  fabAc = null;

  const fab = document.getElementById("messenger-fab");
  if (!fab) return;

  const trigger = fab.querySelector("[data-fab-toggle]");
  if (!trigger) return;

  fabAc = new AbortController();
  const { signal } = fabAc;

  const toggle = () => {
    const isOpen = fab.classList.toggle("is-open");
    trigger.setAttribute("aria-expanded", String(isOpen));
  };

  const close = () => {
    fab.classList.remove("is-open");
    trigger.setAttribute("aria-expanded", "false");
  };

  trigger.addEventListener("click", toggle, { signal });

  document.addEventListener("click", (e) => {
    if (!fab.contains(e.target)) close();
  }, { signal });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  }, { signal });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initMessengerFab);
} else {
  initMessengerFab();
}

document.addEventListener("htmx:afterSwap", initMessengerFab);
document.addEventListener("htmx:historyRestore", initMessengerFab);
