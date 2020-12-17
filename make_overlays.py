#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

TRANSPARENT=(0,)*4
WHITE=(255,)*4
BLACK=(0,)*3+(255,)

IMSIZE = 589
FONTSIZE = 21
import csv

tsvf = open('frames/record.tsv')
reader = csv.DictReader(tsvf, delimiter='\t')

for row in reader:
    im = Image.new('RGBA', (IMSIZE, IMSIZE), color=TRANSPARENT)
    draw = ImageDraw.Draw(im)
    ifont = ImageFont.truetype("/usr/share/fonts/TTF/IBMPlexMono-Bold.ttf", FONTSIZE)

    x = int(row['x'])
    y = int(row['y'])
    f = int(row['f'])
    overlay = "x = {x:02d}, y = {y:02d}, iteration {iter:02d}\nf = {f:+02d}".format(x=x, y=y, iter=int(row['frame']), f=f)

    sizes = [ifont.getsize(l) for l in overlay.splitlines()]
    point = [IMSIZE//2-(sizes[0][0]//2), IMSIZE//2-(sizes[0][1]//2)-(FONTSIZE*2)]
    bpoint = point[:]
    # Text background
    for size in sizes:
        draw.rectangle([(bpoint[0]-2, bpoint[1]-2), (bpoint[0]+size[0]+2, bpoint[1]+size[1]+2)], fill=WHITE)
        bpoint[1] += size[1]+2
    draw.text(point, overlay, font=ifont, fill=BLACK)
    # Sweeper
    sweeper = Image.new('RGBA', (IMSIZE, IMSIZE), color=TRANSPARENT)
    sdraw = ImageDraw.Draw(sweeper)
    radius = 23 # recorded_gif.py
    x += 3 # Image has a padding
    tl = (radius*10+radius+(x*10)+(x*2), 0)
    br = (tl[0]+12, IMSIZE)
    sdraw.rectangle([tl, br], fill=(0, 0, 0, 128))

    im = Image.alpha_composite(sweeper, im)

    im.save('frames/overlays/{:04d}.xpm.png'.format(int(row['frame'])))

tsvf.close()
