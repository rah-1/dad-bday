'use strict';
const album = document.querySelector('#album');
const menu = document.querySelector('#chapter-menu');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const motion = () => reduceMotion.matches ? 'instant' : 'smooth';
const make = (tag, className, content) => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (content !== undefined) element.textContent = content;
  return element;
};
const galleries = [];
// Small ink marks for his interests, independent of the photos or their dates.
const hobbyIds = ['golf', 'cooking', 'f1'];
function hobbyIcon(hobby) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.classList.add('hobby-icon');
  svg.setAttribute('aria-hidden', 'true');
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', `#hobby-${hobby}`);
  svg.append(use);
  return svg;
}
window.MEMORIES.forEach((memory, chapterIndex) => {
  const section = make('section', 'chapter memory');
  section.id = memory.id;
  section.setAttribute('aria-labelledby', `${memory.id}-title`);
  const inner = make('div', 'memory-inner');
  const copy = make('div', 'memory-copy');
  const number = make('span', 'chapter-number', String(chapterIndex + 1).padStart(2, '0'));
  number.setAttribute('aria-hidden', 'true');
  const heading = make('h2', '', memory.title);
  heading.id = `${memory.id}-title`;
  heading.append(make('br'), make('em', '', memory.emphasis));
  copy.append(number, make('p', 'eyebrow', `Ages ${memory.age} · ${memory.label}`), heading, make('p', 'message', memory.message), make('p', 'handwritten', memory.note));
  const gallery = make('div', 'photo-album');
  const track = make('div', 'photo-track');
  track.tabIndex = 0;
  track.id = `${memory.id}-photos`;
  track.setAttribute('role', 'region');
  track.setAttribute('aria-roledescription', 'carousel');
  track.setAttribute('aria-label', `${memory.label} photos. Swipe left or right, or use the arrow keys.`);
  const dots = make('div', 'photo-dots');
  memory.photos.forEach((photo, index) => {
    const slide = make('div', 'photo-slide');
    slide.setAttribute('role', 'group');
    slide.setAttribute('aria-label', `Photo ${index + 1} of ${memory.photos.length}`);
    const figure = make('figure', 'photo-frame');
    figure.style.margin = '0';
    const placeholder = () => {
      const scene = make('div', 'photo-placeholder');
      scene.setAttribute('role', 'img');
      scene.setAttribute('aria-label', `Photo placeholder: ${photo.caption}`);
      scene.append(make('span', 'placeholder-sun'), make('span', 'placeholder-icon', '♡'), make('span', 'placeholder-text', 'A memory belongs here'));
      return scene;
    };
    if (photo.src) {
      const img = make('img', 'memory-photo');
      img.src = photo.src; img.alt = photo.alt || photo.caption;
      img.loading = 'lazy'; img.decoding = 'async';
      img.addEventListener('error', () => img.replaceWith(placeholder()), { once: true });
      figure.append(img);
    } else figure.append(placeholder());
    figure.append(make('figcaption', '', photo.caption));
    const detail = make('p', 'photo-detail');
    detail.append(hobbyIcon(hobbyIds[index % hobbyIds.length]), make('span', '', photo.detail));
    slide.append(figure, detail);
    track.append(slide);
    const dot = make('button');
    dot.setAttribute('aria-label', `Go to photo ${index + 1}: ${photo.caption}`);
    dot.addEventListener('click', () => goPhoto(index));
    dots.append(dot);
  });
  let current = 0;
  const goPhoto = (index) => {
    const target = track.children[Math.max(0, Math.min(index, track.children.length - 1))];
    if (target) track.scrollTo({ left: target.offsetLeft - track.children[0].offsetLeft, behavior: motion() });
  };
  const controls = make('div', 'photo-controls');
  const prev = make('button', '', '←');
  const next = make('button', '', '→');
  prev.setAttribute('aria-label', 'Previous photo'); next.setAttribute('aria-label', 'Next photo');
  prev.setAttribute('aria-controls', track.id); next.setAttribute('aria-controls', track.id);
  prev.onclick = () => goPhoto(current - 1); next.onclick = () => goPhoto(current + 1);
  const update = () => {
    const start = track.children[0]?.offsetLeft || 0;
    let distance = Infinity;
    [...track.children].forEach((slide, index) => {
      const delta = Math.abs(slide.offsetLeft - start - track.scrollLeft);
      if (delta < distance) { distance = delta; current = index; }
    });
    [...dots.children].forEach((dot, index) => dot.setAttribute('aria-current', String(index === current)));
    prev.disabled = current === 0; next.disabled = current === track.children.length - 1;
  };
  track.addEventListener('scroll', update, { passive: true });
  track.addEventListener('keydown', event => {
    if (['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      event.preventDefault(); event.stopPropagation(); goPhoto(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  controls.append(prev, dots, next); gallery.append(track, controls);
  inner.append(copy, gallery);
  const footer = make('div', 'memory-footer');
  const onward = make('button', '', chapterIndex === window.MEMORIES.length - 1 ? 'One more page ↓' : 'Next chapter ↓');
  onward.dataset.go = chapterIndex + 2;
  footer.append(make('span', '', `${String(chapterIndex + 1).padStart(2, '0')} / ${String(window.MEMORIES.length).padStart(2, '0')}`), onward, make('span', '', 'Swipe ↔ for photos'));
  section.append(inner, footer);
  document.querySelector('#memory-chapters').append(section);
  galleries.push({ track, update }); update();
});
const chapters = [...document.querySelectorAll('.chapter')];
const labels = ['Happy 55th', ...window.MEMORIES.map(memory => memory.label), 'With love'];
let activeChapter = 0;
function goChapter(index, focus = false) {
  const target = chapters[index];
  if (!target) return;
  album.scrollTo({ top: target.offsetTop, behavior: motion() });
  if (focus) { target.tabIndex = -1; target.focus({ preventScroll: true }); }
}
chapters.forEach((chapter, index) => {
  const dot = make('button', 'rail-dot');
  dot.setAttribute('aria-label', labels[index]); dot.append(make('span', '', labels[index]));
  dot.onclick = () => goChapter(index, true);
  document.querySelector('.chapter-rail').append(dot);
  const link = make('button');
  link.append(make('span', '', index === 0 ? '♡' : index === chapters.length - 1 ? '✳' : window.MEMORIES[index - 1].age), document.createTextNode(labels[index]));
  link.onclick = () => { menu.close(); goChapter(index, true); };
  document.querySelector('#chapter-links').append(link);
});
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    entry.target.classList.toggle('active', entry.isIntersecting);
    if (entry.isIntersecting) {
      activeChapter = chapters.indexOf(entry.target);
      document.querySelectorAll('.rail-dot').forEach((dot, index) => dot.setAttribute('aria-current', String(index === activeChapter)));
      document.querySelector('#announcement').textContent = labels[activeChapter];
    }
  });
}, { root: album, threshold: .55 });
chapters.forEach(chapter => observer.observe(chapter));
document.addEventListener('click', event => {
  const button = event.target.closest('[data-go]');
  if (button) goChapter(Number(button.dataset.go), true);
});
document.querySelector('.masthead a').onclick = event => { event.preventDefault(); goChapter(0, true); };
document.querySelector('#open-chapters').onclick = () => menu.showModal();
document.querySelector('#close-chapters').onclick = () => menu.close();
menu.addEventListener('click', event => {
  const bounds = menu.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) menu.close();
});
document.addEventListener('keydown', event => {
  if (menu.open || event.altKey || event.ctrlKey || event.metaKey) return;
  if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Home', 'End'].includes(event.key)) {
    event.preventDefault();
    let index = activeChapter + (['ArrowDown', 'PageDown'].includes(event.key) ? 1 : -1);
    if (event.key === 'Home') index = 0;
    if (event.key === 'End') index = chapters.length - 1;
    goChapter(Math.max(0, Math.min(index, chapters.length - 1)), true);
  }
});
window.addEventListener('resize', () => galleries.forEach(({ update }) => update()));
