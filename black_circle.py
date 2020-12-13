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
from rcbitmap import BLACK, TRANSPARENT

WIDTH = HEIGHT = 301

bitmap = Bitmap(WIDTH, HEIGHT, background=TRANSPARENT)

for i in range(1, 151):
    bitmap.circle(x0=(WIDTH//2), y0=(HEIGHT//2), radius=i, colour=BLACK)

bitmap.xpm()
