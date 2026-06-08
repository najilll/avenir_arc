/**
 * avenir-projects.js
 * Optional standalone helper — all core logic is already inside index.html.
 * Use this file if you want to extend or override grid behaviour.
 */

/* Utility: debounce */
function debounce(fn, delay) {
  let t;
  return function (...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), delay);
  };
}

/* Utility: throttle */
function throttle(fn, limit) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
    if (now - last >= limit) { last = now; fn.apply(this, args); }
  };
}

/**
 * Example: extend project card with a "copy link" button
 * (uncomment and call after renderCards if needed)
 */
// function addCopyLinks() {
//   document.querySelectorAll('.pcard').forEach(card => {
//     const slug = card.dataset.slug;
//     const btn = document.createElement('button');
//     btn.textContent = '🔗';
//     btn.title = 'Copy link';
//     btn.style.cssText = 'position:absolute;top:10px;left:10px;background:rgba(255,255,255,.8);border:none;padding:2px 6px;font-size:.7rem;';
//     btn.onclick = e => {
//       e.stopPropagation();
//       navigator.clipboard.writeText(window.location.origin + '/api/projects/' + slug + '/');
//     };
//     card.querySelector('.pcard-cover').appendChild(btn);
//   });
// }
