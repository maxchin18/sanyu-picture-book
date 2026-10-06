(() => {
  const BOOK = window.BOOK, STARTS = window.STARTS;
  const SRC = "video/master.m3u8";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- gold leaf flecks ---------- */
  const cv = document.getElementById("flecks"), cx = cv.getContext("2d");
  let W, H, dpr, flecks = [];
  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = cv.width = innerWidth * dpr; H = cv.height = innerHeight * dpr;
    const n = Math.round(Math.min(90, innerWidth / 14));
    flecks = Array.from({ length: n }, () => newFleck(true));
  }
  function newFleck(anywhere) {
    return {
      x: Math.random() * W, y: anywhere ? Math.random() * H : H + 10,
      r: (Math.random() ** 2 * 2.6 + .5) * dpr, vy: -(Math.random() * .25 + .06) * dpr,
      vx: (Math.random() - .5) * .12 * dpr, a: Math.random() * .6 + .25, tw: Math.random() * Math.PI * 2,
      hue: Math.random() < .8 ? "236,200,120" : "246,226,166"
    };
  }
  function draw(move) {
    cx.clearRect(0, 0, W, H);
    for (const f of flecks) {
      if (move) {
        f.y += f.vy; f.x += f.vx; f.tw += .02;
        if (f.y < -10) Object.assign(f, newFleck(false));
      }
      const a = f.a * (.65 + .35 * Math.sin(f.tw));
      cx.beginPath(); cx.arc(f.x, f.y, f.r, 0, 6.283);
      cx.fillStyle = `rgba(${f.hue},${a})`; cx.shadowColor = `rgba(${f.hue},${a})`; cx.shadowBlur = f.r * 3;
      cx.fill();
    }
  }
  function tick() { if (!document.hidden) draw(true); requestAnimationFrame(tick); }
  size();
  addEventListener("resize", () => { size(); if (reduce) draw(false); });
  if (reduce) draw(false); else requestAnimationFrame(tick);

  /* ---------- top bar + reveal ---------- */
  const bar = document.querySelector(".topbar");
  addEventListener("scroll", () => bar.classList.toggle("solid", scrollY > 60), { passive: true });
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  /* ---------- video ---------- */
  const video = document.getElementById("video"), bigPlay = document.getElementById("bigPlay");
  const chips = [...document.querySelectorAll(".chip")];
  const nowNo = document.getElementById("nowNo"), nowTitle = document.getElementById("nowTitle");
  let ready = null;
  function load() {
    if (ready) return ready;
    ready = new Promise(res => {
      if (video.canPlayType("application/vnd.apple.mpegurl")) {
        video.src = SRC; video.addEventListener("loadedmetadata", res, { once: true }); video.load();
      } else if (window.Hls && Hls.isSupported()) {
        const hls = new Hls({ capLevelToPlayerSize: true, startLevel: -1 });
        hls.loadSource(SRC); hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, () => res());
      } else { video.src = SRC; res(); }
    });
    return ready;
  }
  async function playAt(t) {
    await load();
    if (t != null) video.currentTime = t;
    try { await video.play(); } catch (_) {}
  }
  bigPlay.addEventListener("click", () => playAt(null));
  video.addEventListener("play", () => bigPlay.classList.add("hide"));
  video.addEventListener("pointerdown", () => load(), { once: true });
  function pageAt(t) { let p = 0; for (let i = 0; i < STARTS.length; i++) if (t >= STARTS[i] - .2) p = i; return p; }
  let lastP = -1;
  video.addEventListener("timeupdate", () => {
    const p = pageAt(video.currentTime);
    if (p === lastP) return; lastP = p;
    chips.forEach(c => c.classList.toggle("on", +c.dataset.page === p));
    nowNo.textContent = p ? "No. " + String(p).padStart(2, "0") : "Prologue";
    nowTitle.textContent = p ? BOOK[p - 1].t : "三魚海味探索繪本";
  });
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-t]");
    if (!b) return;
    closeReader();
    document.getElementById("film").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    playAt(parseFloat(b.dataset.t));
  });

  /* ---------- reader ---------- */
  const reader = document.getElementById("reader"), rImg = document.getElementById("rImg"),
        rNo = document.getElementById("rNo"), rCount = document.getElementById("rCount"),
        rTitle = document.getElementById("rTitle"), rBody = document.getElementById("rBody"),
        rPrev = document.getElementById("rPrev"), rNext = document.getElementById("rNext");
  let cur = 1, lastFocus = null;
  function show(n) {
    cur = Math.max(1, Math.min(16, n));
    const pg = BOOK[cur - 1], id = String(cur).padStart(2, "0");
    rImg.src = `img/p${id}.webp`; rImg.alt = `第 ${cur} 頁插圖：${pg.t}`;
    rNo.textContent = "No. " + id; rCount.textContent = `${cur} / 16`;
    rTitle.textContent = pg.t; rBody.innerHTML = "";
    pg.p.forEach(s => { const p = document.createElement("p"); p.textContent = s; rBody.appendChild(p); });
    rPrev.disabled = cur === 1; rNext.disabled = cur === 16;
    const nxt = new Image(); if (cur < 16) nxt.src = `img/p${String(cur + 1).padStart(2, "0")}.webp`;
  }
  function openReader(n) { lastFocus = document.activeElement; show(n); reader.hidden = false; document.body.style.overflow = "hidden"; document.getElementById("rClose").focus(); }
  function closeReader() {
    if (reader.hidden) return;
    reader.hidden = true; document.body.style.overflow = "";
    const el = document.getElementById("p" + String(cur).padStart(2, "0"));
    if (el) el.scrollIntoView({ block: "center" });
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }
  document.querySelectorAll("[data-open]").forEach(b => b.addEventListener("click", () => openReader(+b.dataset.open)));
  document.getElementById("rClose").addEventListener("click", closeReader);
  rPrev.addEventListener("click", () => show(cur - 1));
  rNext.addEventListener("click", () => show(cur + 1));
  reader.addEventListener("click", e => { if (e.target === reader) closeReader(); });
  addEventListener("keydown", e => {
    if (reader.hidden) return;
    if (e.key === "Escape") closeReader();
    else if (e.key === "ArrowLeft") show(cur - 1);
    else if (e.key === "ArrowRight") show(cur + 1);
  });
  let sx = null;
  reader.addEventListener("touchstart", e => { sx = e.touches[0].clientX; }, { passive: true });
  reader.addEventListener("touchend", e => {
    if (sx == null) return; const dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
  });
})();
