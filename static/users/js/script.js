// After 2 seconds, hide intro and show CTA
setTimeout(() => {
    document.getElementById('intro').classList.add('hidden');
    document.getElementById('cta').classList.remove('hidden');
  }, 2000);
  