"""Build the curated 55-photo album. Requires Pillow; originals stay untouched."""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ROTATE_LEFT = {8305,8306,8307,8308,8310,8311,8313,8316,8317,8320,8322,8324,8328,8330,8331,8332,8333,8334,8335,8336,8337,8338,8339,8342,8343}
ROTATE_RIGHT = {8340,8345,8349,8351,8356,8363}
# Group boundaries follow the supplied file-name order: 10 / 19 / 7 / 5 / 5 / 13.
# Omitted: 8321 (overlapping family portrait), 8325 (softer overlapping portrait),
# 8329 (overlapping gathering), 8366 (softer sideways snapshot).
GROUPS = [
    dict(id='formative-years', label='Formative years & family', title='Where it all', emphasis='began.', message='The first pages of your story, and the family woven through them. So much life, held in these little photographs.', note='The people at the beginning.', photos=[
        (8307,'The early pages','An older man seated with two children.'),
        (8308,'A moment outdoors','Two young people sitting together outdoors.'),
        (8305,'Family traditions','A family gathered around a traditional ceremony.'),
        (8310,'Everyone together','A large family group posing together indoors.'),
        (8306,'A little music','A woman seated on the floor playing a stringed instrument.'),
        (8312,'Across generations','Two men standing behind a seated older woman.'),
        (8311,'Faces we hold close','Four older women sitting together.'),
        (8313,'A portrait to keep','A seated older woman wearing a sari.'),
        (8314,'From the family album','A studio portrait of a young woman.'),
        (8309,'Together, outdoors','Three family members standing together outdoors.')]),
    dict(id='asha-kiran', label='Life at Asha Kiran', title='A place called', emphasis='home.', message='Asha Kiran, Bengaluru. Familiar faces, shared celebrations, and all the little moments that make a place part of your story.', note='A whole chapter of belonging.', photos=[
        (8334,'The Asha Kiran days','A group of family and friends gathered among plants outdoors.'),
        (8317,'An afternoon together','Three young men sitting and talking outdoors.'),
        (8318,'Time for a game','A young man holding a paddle beside a table-tennis table.'),
        (8316,'Something to celebrate','A group raising their glasses around a table.'),
        (8328,'A little fun in the sun','Two young men posing playfully outdoors.'),
        (8322,'Just the two of you','A man and woman standing together outside a doorway.'),
        (8320,'A familiar embrace','Three people posing together indoors.'),
        (8330,'Smiles from home','Two women smiling together beside a bookshelf.'),
        (8323,'Four-legged family, too','A couple seated indoors with a black dog.'),
        (8327,'A very good companion','A black dog sitting on a tiled floor.'),
        (8315,'Dressed for the occasion','A young person in traditional dance costume posing outdoors.'),
        (8326,'A moment of pride','Two people standing together, one wearing traditional dance costume.'),
        (8331,'A sunny day together','Four people sitting together beneath palm leaves.'),
        (8332,'Traditions to carry with you','A young man wearing glasses during a traditional ceremony.'),
        (8333,'A family gathering','Family members taking part in a traditional ceremony.'),
        (8324,'The people who made it home','Four family members standing together outdoors.')]),
    dict(id='college-life', label='College life', title='Friends, and a world', emphasis='of possibility.', message='The college chapter. Faces, places, and moments to come back to, one photograph at a time.', note='Some chapters stay with you.', photos=[
        (8336,'The college crew','A large group posing outside a college building.'),
        (8335,'All in one frame','A group of young men posing together outdoors.'),
        (8337,'Out and about','A group gathered around a motorcycle outdoors.'),
        (8338,'Those days, those smiles','A smiling group of friends posing outdoors.'),
        (8340,'A little music along the way','A young man playing an acoustic guitar.'),
        (8339,'A gathering to remember','People gathered around a seated young man during a ceremony.'),
        (8341,'A moment worth keeping','Two people embracing in a doorway.')]),
    dict(id='us-ready', label='US ready', title='Ready for the', emphasis='next chapter.', message='The US-ready years. A new chapter ahead, with the people you love always part of the story.', note='New beginnings, familiar love.', photos=[
        (8342,'Before the next adventure','A family group posing around a seated man indoors.'),
        (8343,'Around the table','Three men seated together at a dining table.'),
        (8345,'A world ahead','A man in a yellow jacket posing outdoors beside water.'),
        (8346,'Out into the evening','A man in a yellow jacket standing outdoors at night.'),
        (8347,'A moment along the way','Two people posing together outside a temple entrance.')]),
    dict(id='thatha', label='Thatha', title='So much love,', emphasis='in these pages.', message='A few moments with Thatha. Familiar expressions, family gatherings, and the love that connects these pages.', note='Close to our hearts.', photos=[
        (8352,'A portrait of Thatha','A portrait of an older man wearing a suit and tie.'),
        (8348,'A quiet moment outdoors','An older man standing in a leafy garden.'),
        (8349,'A moment at the table','An older man in a red shirt seated at a table with food.'),
        (8350,'Side by side','Two older men standing together outdoors in traditional clothing.'),
        (8351,'Together with family','Family members gathered during a flower-filled ceremony.')]),
    dict(id='our-family', label='Our family', title='Our favorite part:', emphasis='being together.', message='The family you’re part of. The big days, the small days, and so many reasons we’re grateful for you. We love you, Dad.', note='A whole family of love for you.', photos=[
        (8354,'A new little chapter','A family portrait with a baby and an older woman.'),
        (8353,'All the generations','A multigenerational family portrait with a baby.'),
        (8355,'The littlest smiles','A baby seated among soft toys.'),
        (8361,'A little everyday love','A father holding and kissing a baby.'),
        (8356,'Held close','Adults gathered around a smiling baby.'),
        (8363,'A lap full of love','A father seated with two young children.'),
        (8364,'Growing up together','A studio portrait of two small children.'),
        (8358,'That little smile','A young boy smiling in an outdoor portrait.'),
        (8359,'Side by side','Two boys in striped shirts posing outdoors.'),
        (8360,'A little older, still together','Two boys smiling together beside a wooden bench.'),
        (8365,'Out making memories','Two boys in striped shirts posing in a basketball arena.'),
        (8362,'And always, you','A smiling man in traditional white clothing standing indoors.')]),
]

# Mom's editing notes refer to the original album positions, before these moves.
by_id = {group['id']: group for group in GROUPS}
roots, asha, college, us, thatha, family = [by_id[key] for key in (
    'formative-years', 'asha-kiran', 'college-life', 'us-ready', 'thatha', 'our-family')]

def relabel(group, number, caption):
    group['photos'] = [(key, caption if key == number else text, alt) for key, text, alt in group['photos']]

def move(source, destination, number):
    record = next(photo for photo in source['photos'] if photo[0] == number)
    source['photos'].remove(record)
    destination['photos'].append(record)

relabel(roots, 8309, 'Some of My Fav People')
relabel(asha, 8322, 'Friends')
relabel(asha, 8332, 'A Moment of Strength')
relabel(asha, 8324, 'Neighbors')
relabel(college, 8339, 'Thread Ceremony')
relabel(us, 8346, 'Landed in the US')
relabel(us, 8347, 'A Sacred Moment')
for number in (8334, 8333):  # Asha Kiran's old 01/16 and 15/16.
    move(asha, roots, number)
for number in (8350, 8351):  # Thatha's old 04/05 and 05/05.
    move(thatha, roots, number)
    relabel(roots, number, 'Side by side' if number == 8350 else 'A family celebration')
relabel(roots, 8334, 'Family, all together')

roots.update(label='My Roots', title='My', emphasis='roots.',
    message='The people who came before us. The faces, traditions, and everyday moments that made this family ours.',
    note='Our story starts with them.')
roots['photos'] = [
    ('f-and-L/2_Vittu_Raghu_Paddy_Seetha.jpg', 'Our roots', 'A black-and-white family portrait of two young men standing behind a seated man and woman.'),
    ('first-chap/IMG_7013.jpg', 'The people at the beginning', 'A black-and-white portrait of a man and woman wearing glasses.'),
    ('first-chap/IMG-20200417-WA0004.jpg', 'The early years, together', 'An older black-and-white family photograph outdoors.'),
    ('first-chap/IMG-20200418-WA0023.jpg', 'A little moment from home', 'A black-and-white photograph of an older woman standing with two children outdoors.'),
    ('first-chap/20140702_203217.jpg', 'A little music', 'An old family photograph of a woman playing a stringed instrument with a child beside her.'),
] + roots['photos']

# Keep the newly supplied images and all explicitly moved/relabelled photos.
# Replace older overlapping music/portrait shots and similar childhood pictures.
OMITTED_FOR_REPLACEMENTS = {8306, 8311, 8312, 8314, 8315, 8327, 8354, 8355, 8358, 8359, 8364}
for group in GROUPS:
    group['photos'] = [photo for photo in group['photos'] if photo[0] not in OMITTED_FOR_REPLACEMENTS]
dog = next(photo for photo in asha['photos'] if photo[0] == 8323)
asha['photos'].remove(dog)
asha['photos'].insert(0, dog)

# Replace the old final family photo (8362) with the new family group photograph.
family['photos'] = [photo for photo in family['photos'] if photo[0] != 8362]
family['photos'] += [
    ('last-but-one/upe5191.jpg', 'Three generations, one frame', 'A woman and child seated beside an older woman.'),
    ('last-but-one/paati-rahul-4.jpg', 'Held with love', 'An older woman holding a small child.'),
    ('last-but-one/05.jpg', 'All the generations', 'Women and children gathered together on a sofa.'),
    ('last-but-one/23.jpg', 'A lap full of memories', 'Two older women smiling together with three children.'),
    ('last-but-one/test.jpg', 'A little birthday love', 'Two grandparents holding a small child in front of a birthday banner.'),
    ('last-but-one/DSC05655.JPG', 'Our family, together', 'A family group smiling together indoors.'),
    ('f-and-L/IMG_3974.JPG', 'One more lap, one more memory', 'A person in a racing suit standing beside a blue number 2 NASCAR car at a racetrack.'),
]
thatha.update(title='Our roots.', emphasis='Our love.',
    message='Thatha, so much of our family’s story begins with you. These photographs hold moments we’re grateful to share, and love that brings us together. We’re thinking of you, wishing you comfort and strength, and holding you close in our hearts.',
    note='With all our love, Thatha.')
GROUPS = [roots, asha, us, college, family, thatha]

output = ROOT / 'photos' / 'web'
output.mkdir(exist_ok=True)
used = []
for group in GROUPS:
    photos = []
    for number, caption, alt in group['photos']:
        source_path = Path(f'IMG_{number}.jpg') if isinstance(number, int) else Path(number)
        filename = f'IMG_{number}.jpg' if isinstance(number, int) else source_path.parent.name + '-' + source_path.stem + '.jpg'
        with Image.open(ROOT / 'photos' / source_path) as source:
            image = ImageOps.exif_transpose(source).convert('RGB')
            if number in ROTATE_LEFT:
                image = image.rotate(90, expand=True)
            if number in ROTATE_RIGHT:
                image = image.rotate(-90, expand=True)
            image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            image.save(output / filename, quality=86, optimize=True, progressive=True)
        photos.append(dict(src=f'photos/web/{filename}', alt=alt, caption=caption, detail=group['label']))
        used.append(number)
    group['photos'] = photos
assert len(used) == len(set(used)) == 55, 'The album must contain 55 unique photos.'
selected_files = {Path(photo['src']).name for group in GROUPS for photo in group['photos']}
selected_files.add('cats-cover.jpg')  # Separate, user-supplied back-cover image.
# Prune only obsolete generated web copies; source folders are never touched.
for generated in output.glob('*.jpg'):
    if generated.name not in selected_files:
        generated.unlink()
(ROOT / 'memories.js').write_text('// 55 curated photos. Generated by scripts/prepare_photos.py.\nwindow.MEMORIES = ' + json.dumps(GROUPS, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
print('Prepared 55 photos:', ', '.join(f"{g['label']}: {len(g['photos'])}" for g in GROUPS))
print(f'Web images: {sum(p.stat().st_size for p in output.glob("*.jpg"))/1024/1024:.1f} MB. Originals unchanged.')
