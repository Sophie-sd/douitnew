const STORAGE_KEY = 'ru_modal_shown';
const RU_PREFIX = '/ru/';

const getUkUrl = () => {
  const path = window.location.pathname.replace(/^\/ru(\/|$)/, '/');
  return (path || '/') + window.location.search + window.location.hash;
};

const initLangModal = () => {
  if (!window.location.pathname.startsWith(RU_PREFIX)) return;
  if (sessionStorage.getItem(STORAGE_KEY)) return;

  const modal = document.getElementById('lang-switch-modal');
  if (!modal) return;

  const switchBtn = document.getElementById('lang-modal-switch');
  const stayBtn = document.getElementById('lang-modal-stay');

  switchBtn?.setAttribute('href', getUkUrl());

  stayBtn?.addEventListener('click', () => {
    modal.close();
    sessionStorage.setItem(STORAGE_KEY, '1');
  });

  modal.addEventListener('cancel', () => {
    sessionStorage.setItem(STORAGE_KEY, '1');
  });

  setTimeout(() => modal.showModal(), 2000);
};

document.addEventListener('DOMContentLoaded', initLangModal);

// Re-run after HTMX navigation (hx-boost replaces content but fires this event)
document.addEventListener('htmx:afterSettle', () => {
  const modal = document.getElementById('lang-switch-modal');
  if (modal?.open) return;

  const switchBtn = document.getElementById('lang-modal-switch');
  switchBtn?.setAttribute('href', getUkUrl());

  if (!window.location.pathname.startsWith(RU_PREFIX)) return;
  if (sessionStorage.getItem(STORAGE_KEY)) return;

  modal && setTimeout(() => modal.showModal(), 2000);
});
