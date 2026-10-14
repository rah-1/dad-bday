'use strict';
// The official artist recording. The player lives outside the scrollable album,
// so moving between chapters or photos never recreates or restarts the song.
(() => {
  const videoId = 'aR-kZUL9e6o';
  const panel = document.querySelector('#music-panel');
  const toggle = document.querySelector('#music-toggle');
  const container = document.querySelector('#music-player');
  let hasStarted = false;

  function openPlayer() {
    if (!panel.hidden) return;
    const chapter = document.querySelector('.chapter.active');
    panel.hidden = false;
    document.body.classList.add('music-playing');
    if (chapter) document.querySelector('#album').scrollTo({ top: chapter.offsetTop, behavior: 'instant' });
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Stop music and close player');
    const frame = document.createElement('iframe');
    const params = new URLSearchParams({
      autoplay: '1', playsinline: '1', loop: '1', playlist: videoId,
      controls: '1', rel: '0', origin: window.location.origin
    });
    frame.src = `https://www.youtube-nocookie.com/embed/${videoId}?${params}`;
    frame.title = 'My Old Man — Zac Brown Band, official YouTube recording';
    frame.width = '224'; frame.height = '200';
    frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    container.replaceChildren(frame);
    hasStarted = true;
  }

  function closePlayer() {
    // Removing the embed reliably stops playback, even if a third-party API is
    // blocked. The visible native player provides pause/resume without closing.
    container.replaceChildren();
    const chapter = document.querySelector('.chapter.active');
    panel.hidden = true;
    document.body.classList.remove('music-playing');
    if (chapter) document.querySelector('#album').scrollTo({ top: chapter.offsetTop, behavior: 'instant' });
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Play My Old Man by Zac Brown Band');
  }

  toggle.addEventListener('click', () => panel.hidden ? openPlayer() : closePlayer());
  document.querySelector('#music-close').addEventListener('click', () => {
    closePlayer(); toggle.focus();
  });
  document.querySelectorAll('#welcome [data-go="1"]').forEach(button => {
    button.addEventListener('click', () => { if (!hasStarted) openPlayer(); });
  });
})();
