# For Dad — 55 years of you

A mobile-first birthday album with 55 unique family photographs. Swipe vertically through chapters and horizontally through photos. Buttons, chapter navigation, photo counters, and keyboard navigation are also available.

Live site: https://rah-1.github.io/dad-bday/

## Photo curation

Groups follow the original alphabetical filename sequence provided by the family:

| Chapter | Original group | Included |
| --- | --- | --- |
| Formative years & family | First 10 | 10 |
| Life at Asha Kiran | Next 19 | 16 |
| College life | Next 7 | 7 |
| US ready | Next 5 | 5 |
| Thatha | Next 5 | 5 |
| Our family | Last 13 | 12 |
| Total | 59 | 55 |

Within groups, photos are arranged for narrative flow, without claiming exact dates. Thatha's chapter uses present, affectionate language. Omitted originals remain untouched: IMG_8321.jpg, IMG_8325.jpg, and IMG_8329.jpg overlap with other Asha Kiran portraits/gatherings; IMG_8366.jpg is a softer family snapshot overlapping with the other sibling photos.

scripts/prepare_photos.py records the selection, order, captions, alt text, and rotation corrections. Run it with Python and Pillow to regenerate memories.js and photos/web/. Web copies are upright, resized to a maximum 1600 pixels, and saved without EXIF metadata. Original JPGs in photos/ stay local and are ignored by Git. Only the selected 55 web copies are published. The two cover photos reuse selections from the album.

## Preview and updates

Run node server.js and visit http://localhost:5173. The site is static; pushing main updates GitHub Pages. When changing assets, update version query strings in index.html to refresh cached CSS and scripts.

Gallery photos use object-fit: contain to preserve the full photograph. Google Fonts enhance typography online, with system fallbacks offline. No analytics, uploads, accounts, or backend are required.
