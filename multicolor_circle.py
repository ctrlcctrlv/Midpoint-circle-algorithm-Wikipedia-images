#!/usr/bin/env python3
# © 2020 Fredrick R. Brennan (User:Psiĥedelisto) (For Wikipedia)

# Permission is granted to copy, distribute and/or modify this document
# under the terms of the GNU Free Documentation License, Version 1.2
# or any later version published by the Free Software Foundation;
# with no Invariant Sections, no Front-Cover Texts, and no Back-Cover
# Texts.  A copy of the license is included in the section entitled "GNU
# Free Documentation License".

import math

from rcbitmap import Bitmap
from rcbitmap import BLACK, WHITE, RED, GREEN, BLUE, TRANSPARENT

WIDTH = HEIGHT = 301

bitmap = Bitmap(WIDTH, HEIGHT, background=TRANSPARENT)

colours = list()

for i in range(0,25):
    colours.append(BLACK if i%2 else RED)

for i in range(0,25):
    colours.append(BLACK if math.ceil(i/2)%2 else RED)

for i in range(0,5):
    colours.append(RED)

for i in range(0,5):
    colours.append(BLACK)

for i in range(0,150-len(colours)):
    colours.append(BLUE if math.floor(i/18)%2 else RED)

assert len(colours) == 150, "Not enough colours"

for i in range(1, 151):
    bitmap.circle(x0=(WIDTH//2), y0=(HEIGHT//2), radius=i, colour=colours[i-1])

bitmap.xpm()
