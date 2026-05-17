(function(){
  const row = document.querySelector('.partner-row');

  if(row){
    row.innerHTML = row.innerHTML + row.innerHTML;

    let x = 0;

    function tick(){
      x -= 0.6;
      row.style.transform = `translateX(${x}px)`;

      if(Math.abs(x) > row.scrollWidth / 2){
        x = 0;
      }

      requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  // ================= MOBILE NAVIGATION =================

  const hamburger = document.getElementById('hamburger');
  const nav = document.querySelector('.nav');

  if(hamburger && nav){

    hamburger.addEventListener('click', () => {
      nav.classList.toggle('show');
      hamburger.classList.toggle('active');
    });

    // close menu when a nav link is clicked
    document.querySelectorAll('.nav a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('show');
        hamburger.classList.remove('active');
      });
    });

    // close menu when clicking outside
    document.addEventListener('click', (e) => {
      const clickedInsideNav = nav.contains(e.target);
      const clickedHamburger = hamburger.contains(e.target);

      if(!clickedInsideNav && !clickedHamburger){
        nav.classList.remove('show');
        hamburger.classList.remove('active');
      }
    });
  }

})();
