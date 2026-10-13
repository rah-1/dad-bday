# For Dad — 55 years of you

A mobile-first birthday album, inspired by the full-screen scroll chapters in `../kirti-birthday`. Swipe up/down through the chapters and left/right through each chapter’s photos. Arrow buttons, the Chapters menu, and keyboard navigation are also available. The copy celebrates Dad and offers support without assuming an outcome for his father.

## Preview

From this folder, run `node server.js`, then visit http://localhost:5173. A phone on the same Wi-Fi can use your computer’s local IP address with port 5173, if your firewall allows it. The site is static and can also be opened directly via `index.html` or uploaded to static hosting.

## Add the family photos

1. Put your images in `photos/` (for example `photos/childhood-01.jpg`).
2. Open `memories.js`. Change a photo’s `src: ''` to `src: 'photos/childhood-01.jpg'`.
3. Write its `alt`, `caption`, and `detail`. The current captions are collection prompts, not factual memories.

Each chapter has three placeholders. Add/remove photo objects to change the count; controls update automatically. Change chapter titles, messages, and age ranges in the same file. Use `style.css` to adjust colors or layout. Photos use a cropped 4:3 frame (wider on short phones); crop beforehand or change `object-fit` if a particular picture needs its full frame.

Google Fonts enhance the typography when online; system fonts are used offline. No analytics, uploads, accounts, or backend are required.
