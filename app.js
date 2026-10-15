(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(pointer: fine)');
  const motionButton = $('.motion-toggle');
  let motionPaused = false;
  try { motionPaused = sessionStorage.getItem('ma-cakr-motion') === 'off'; } catch (_) {}
  const effectsAllowed = () => !motionPaused && !reduce.matches;
  const menuButton = $('.menu-toggle');
  const menu = $('#navigation');
  function closeMenu() { if (menuButton) { menuButton.setAttribute('aria-expanded','false'); menu.classList.remove('is-open'); } }
  menuButton?.addEventListener('click', () => {
    const open=menuButton.getAttribute('aria-expanded')!=='true';
    menuButton.setAttribute('aria-expanded',String(open));menu.classList.toggle('is-open',open);
  });
  $$('a',menu).forEach(link=>link.addEventListener('click',closeMenu));
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&menuButton?.getAttribute('aria-expanded')==='true'){closeMenu();menuButton.focus();}
  });
  document.addEventListener('click',event=>{if(!event.target.closest('.site-header'))closeMenu();});
  matchMedia('(min-width: 651px)').addEventListener('change',event=>{if(event.matches)closeMenu();});
  if('IntersectionObserver'in window){
    document.documentElement.classList.add('js-ready');
    const observer=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target);}});
    },{threshold:.07});
    $$('.reveal').forEach(el=>observer.observe(el));
  }
  const normalize=text=>text.toLocaleLowerCase(document.documentElement.lang||'en').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ı/g,'i');
  const search=$('#note-search');
  const noteCards=$$('.note-card');
  let activeTopic='all';
  function filterNotes(){
    const words=normalize(search.value.trim()).split(/\s+/).filter(Boolean);let count=0;
    noteCards.forEach(card=>{
      const matches=(activeTopic==='all'||card.dataset.topic===activeTopic)&&words.every(word=>normalize(card.dataset.search).includes(word));
      card.hidden=!matches;if(matches){card.classList.add('is-visible');count++;}
    });
    const unit=count===1&&document.documentElement.lang==='en'?'note':$('.result-count').dataset.unit;
    $('.result-count').textContent=`${count} ${unit}`;
    $('.no-results').hidden=count!==0;$('.clear-search').hidden=search.value.length===0;
  }
  if(search){
    search.addEventListener('input',filterNotes);
    $('.clear-search').addEventListener('click',()=>{search.value='';filterNotes();search.focus();});
    $$('.topic-filter').forEach(button=>button.addEventListener('click',()=>{
      activeTopic=button.dataset.topic;
      $$('.topic-filter').forEach(other=>{const active=other===button;other.classList.toggle('is-active',active);other.setAttribute('aria-pressed',String(active));});filterNotes();
    }));
  }
  $$('.magnetic').forEach(element=>{
    element.addEventListener('pointermove',event=>{
      if(!effectsAllowed()||!finePointer.matches)return;
      const b=element.getBoundingClientRect();
      const x=(event.clientX-b.left-b.width/2)*.07,y=(event.clientY-b.top-b.height/2)*.1;
      element.style.transform=`translate(${Math.max(-3,Math.min(3,x))}px,${Math.max(-3,Math.min(3,y))}px)`;
    });
    element.addEventListener('pointerleave',()=>{element.style.transform='';});
    element.addEventListener('blur',()=>{element.style.transform='';});
  });
  const canvas=$('#ambient-trail'),ctx=canvas?.getContext('2d');
  let trail=[],raf=null,lastPoint=null;
  function clearTrail(){if(raf!==null)cancelAnimationFrame(raf);raf=null;trail=[];lastPoint=null;if(ctx)ctx.clearRect(0,0,innerWidth,innerHeight);}
  function drawTrail(now){
    raf=null;if(!ctx||!effectsAllowed()||document.hidden){clearTrail();return;}
    ctx.clearRect(0,0,innerWidth,innerHeight);trail=trail.filter(p=>now-p.t<850);
    for(let i=0;i<trail.length;i++){
      const p=trail[i],life=1-(now-p.t)/850,size=2+life*3;
      ctx.strokeStyle=`rgba(165,84,52,${life*.27})`;ctx.lineWidth=.75;ctx.beginPath();
      ctx.moveTo(p.x-size,p.y);ctx.lineTo(p.x+size,p.y);ctx.moveTo(p.x,p.y-size);ctx.lineTo(p.x,p.y+size);ctx.stroke();
      if(i>0&&Math.hypot(p.x-trail[i-1].x,p.y-trail[i-1].y)<85){ctx.strokeStyle=`rgba(165,84,52,${life*.12})`;ctx.beginPath();ctx.moveTo(trail[i-1].x,trail[i-1].y);ctx.lineTo(p.x,p.y);ctx.stroke();}
    }
    if(trail.length)raf=requestAnimationFrame(drawTrail);
  }
  function resizeCanvas(){if(!ctx)return;const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(innerWidth*dpr);canvas.height=Math.round(innerHeight*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);clearTrail();}
  if(ctx){
    resizeCanvas();window.addEventListener('resize',resizeCanvas);
    document.addEventListener('pointermove',event=>{
      if(!effectsAllowed()||!finePointer.matches||document.hidden)return;
      if(lastPoint&&Math.hypot(event.clientX-lastPoint.x,event.clientY-lastPoint.y)<14)return;
      lastPoint={x:event.clientX,y:event.clientY};trail.push({...lastPoint,t:performance.now()});if(trail.length>24)trail.shift();if(raf===null)raf=requestAnimationFrame(drawTrail);
    },{passive:true});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)clearTrail();});
    document.addEventListener('pointerleave',()=>{lastPoint=null;});
  }
  function syncMotion(){
    const off=!effectsAllowed();document.body.classList.toggle('motion-paused',off);
    if(!motionButton)return;
    motionButton.setAttribute('aria-pressed',String(off));motionButton.disabled=reduce.matches;
    const label=reduce.matches?motionButton.dataset.reduced:off?motionButton.dataset.resume:motionButton.dataset.pause;
    $('span',motionButton).textContent=label;motionButton.setAttribute('aria-label',label);
    if(off){clearTrail();$$('.magnetic').forEach(el=>{el.style.transform='';});}
  }
  motionButton?.addEventListener('click',()=>{motionPaused=!motionPaused;try{sessionStorage.setItem('ma-cakr-motion',motionPaused?'off':'on');}catch(_){}syncMotion();});
  reduce.addEventListener('change',syncMotion);syncMotion();
})();
