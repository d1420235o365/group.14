/**
 * main.js — 前端互動邏輯
 * 書籍查詢系統
 */

/* ── Flash 訊息自動消失 ─────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });
});

/* ── 搜尋表單：Enter 鍵提交 ─────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('search-input') || document.getElementById('hero-search-input');
  if (input) {
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.target.closest('form').submit();
      }
    });
  }
});

/* ── 下拉篩選自動送出 ───────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  ['filter-category', 'filter-status', 'hero-category', 'hero-status'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', () => el.closest('form').submit());
    }
  });
});
