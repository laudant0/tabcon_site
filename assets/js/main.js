(function(){
  const row = document.querySelector('.partner-row');
  if(!row) return;
  row.innerHTML = row.innerHTML + row.innerHTML;
  let x = 0;
  function tick(){ x -= 0.6; row.style.transform = `translateX(${x}px)`; if (Math.abs(x) > row.scrollWidth/2) x = 0; requestAnimationFrame(tick); }
  requestAnimationFrame(tick);
})();