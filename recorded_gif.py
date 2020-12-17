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
from rcbitmap import BLACK, WHITE

WIDTH = HEIGHT = (23*2)+3

bitmap = Bitmap(WIDTH, HEIGHT, background=WHITE)

bitmap.record = True

bitmap.circle(x0=(WIDTH//2), y0=(HEIGHT//2), radius=23, explain=True)
