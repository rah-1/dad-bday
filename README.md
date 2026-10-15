# For Dad — 55 years of you

A mobile-first birthday album with 55 unique family photographs. Swipe vertically through chapters and horizontally through photos. Buttons, chapter navigation, photo counters, and keyboard navigation are also available.

Live site: https://rah-1.github.io/dad-bday/

## Current chapter order

| Chapter | Photos |
| --- | --- |
| My Roots | 15 |
| Life at Asha Kiran | 12 |
| US ready | 5 |
| College life | 7 |
| Our family | 13 |
| Thatha | 3 |
| Total | 55 |

See PHOTO-EDITS.md for Mom's original photo numbers, resolved moves, replacement choices, and captions. All 12 newly supplied images are included. The black-and-white family portrait opens the cover and My Roots. NASCAR ends Our family, immediately before the final Thatha chapter. The cover note reads “our roots.”

scripts/prepare_photos.py records the selection, order, captions, alt text, and rotation corrections. Run it with Python and Pillow to regenerate memories.js and photos/web/. Web copies are upright, resized to a maximum 1600 pixels, and saved without EXIF metadata. Original photos stay local and are ignored by Git. Originals are never modified or deleted.

## Preview and updates

Run node server.js and visit http://localhost:5173. Pushing main updates GitHub Pages. When changing assets, update version query strings in index.html to refresh cached CSS and scripts.

Gallery photos preserve the full frame. Google Fonts enhance typography online, with system fallbacks offline. No analytics, uploads, accounts, or backend are required.

The site is silent, with no music player or audio playback.
