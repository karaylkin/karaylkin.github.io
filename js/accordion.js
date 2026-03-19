document.querySelectorAll('.subject-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
    btn.nextElementSibling.style.display = expanded ? 'none' : 'block';
  });
});

// Auto-open first subject on load
const firstToggle = document.querySelector('.subject-toggle');
if (firstToggle && firstToggle.getAttribute('aria-expanded') !== 'true') {
  firstToggle.setAttribute('aria-expanded', 'true');
  firstToggle.nextElementSibling.style.display = 'block';
}
