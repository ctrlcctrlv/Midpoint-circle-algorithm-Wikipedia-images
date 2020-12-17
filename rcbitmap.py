# © 2009 David McCarthy (User:Paddy3118) (RosettaCode.org: Bitmap, Bitmap →
# Midpoint circle algorithm)
#
# © 2010–2020 RosettaCode.org contributors (to the pages Bitmap, Bitmap →
# Midpoint circle algorithm, Bitmap → Python)
#
# © 2020 Fredrick R. Brennan (User:Psiĥedelisto) (For Wikipedia: Bitmap.xpm,
# various hacky changes to make an animation of circle drawing)

# Permission is granted to copy, distribute and/or modify this document under
# the terms of the GNU Free Documentation License, Version 1.2 or any later
# version published by the Free Software Foundation; with no Invariant
# Sections, no Front-Cover Texts, and no Back-Cover Texts.  A copy of the
# license is included in the section entitled "GNU Free Documentation License".

from collections import namedtuple, OrderedDict
from copy import copy
from io import StringIO
import sys
 
Colour = namedtuple('Colour','r,g,b')
Colour.copy = lambda self: copy(self)

# Colour ranges are not enforced.
TRANSPARENT = Colour(None,None,None)
BLACK = Colour(0,0,0)
WHITE = Colour(255,255,255)
RED = Colour(255,0,0)
ORANGE = Colour(255,128,0)
YELLOW = Colour(255,255,0)
GREEN = Colour(0,255,0)
BLUE = Colour(0,0,255)
PURPLE = Colour(128,0,255)
PINK = Colour(255,0,255)
GREY = Colour(128,128,128)
 
class Bitmap():
    def __init__(self, width = 40, height = 40, background=WHITE):
        assert width > 0 and height > 0 and type(background) == Colour
        self.width = width
        self.height = height
        self.background = background
        self.map = [[background.copy() for w in range(width)] for h in range(height)]

        # Number of set operations
        self.n_sets = 0

        # Record sets?
        self.record = False
 
    def fillrect(self, x, y, width, height, colour=BLACK):
        assert x >= 0 and y >= 0 and width > 0 and height > 0 and type(colour) == Colour
        for h in range(height):
            for w in range(width):
                self.map[y+h][x+w] = colour.copy()
 
    # This function wasn't part of the RosettaCode code, I wrote it.
    def xpm(self, buf=False):
        stdout = sys.stdout
        if buf: outbuf = sys.stdout = StringIO()
        print("/* XPM */")
        colors = OrderedDict()
        colors_d = dict()
        for x in self.map:
            for y in x:
                colors[y] = None
        start = ord("a")
        end = start + len(colors)
        print("static char * WIKIPEDIA_xpm[] = {")
        print('"{} {} {} {}",'.format(len(self.map[0]), len(self.map), len(colors), '1'))
        for i, color in enumerate(colors):
            if color.r is None or color.g is None or color.b is None:
                print('" \tc None",'.format(chr(start+i)))
                # Using a space just improves the appearance to human eyes of the XPM file. Not required part of standard.
                colors_d[color] = " "
            else:
                print('"{}\tc #{:02x}{:02x}{:02x}",'.format(chr(start+i), color.r, color.g, color.b))
                colors_d[color] = chr(start+i)
        for x in self.map:
            print('"', end='')
            for y in x:
                print(colors_d[y], end='')
            print('",')
        print("};")
        sys.stdout = stdout
        if buf: return outbuf
 
    def set(self, x, y, colour=BLACK, only_if=None):
        assert type(colour) == Colour
        if not type(only_if) == Colour or self.get(x, y) == only_if:
            self.map[y][x]=colour
        if self.record:
            with open('frames/{:04d}.xpm'.format(self.n_sets), 'w+') as f:
                f.write(self.xpm(buf=True).getvalue())
 
    def get(self, x, y):
	    return self.map[y][x]
 
    def circle(self, x0, y0, radius, colour=BLACK, explain=False):
        only_if = WHITE if explain else None
        fil = open("frames/record.tsv", "w+")
        if self.record:
            fil.write("frame\tx\ty\tf\n")
        write_frame = lambda frame, x, y, f: fil.write("{frame}\t{x}\t{y}\t{f}\n".format(frame=frame, x=x, y=y, f=f)) if self.record else 0

        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.n_sets += 1
        if explain:
            self.set(x0, y0) # middle dot
        self.set(x0, y0 + radius, GREY if explain else colour, only_if=only_if)
        self.set(x0, y0 - radius, GREY if explain else colour, only_if=only_if)
        self.set(x0 + radius, y0, GREY if explain else colour, only_if=only_if)
        self.set(x0 - radius, y0, GREY if explain else colour, only_if=only_if)
        write_frame(self.n_sets, x, y, f)

        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            self.n_sets += 1
            write_frame(self.n_sets, x, y, f)
            self.set(x0 + x, y0 + y, RED if explain else colour, only_if=only_if)
            self.set(x0 + y, y0 + x, ORANGE if explain else colour, only_if=only_if)
            self.set(x0 + y, y0 - x, YELLOW if explain else colour, only_if=only_if)
            self.set(x0 + x, y0 - y, GREEN if explain else colour, only_if=only_if)
            self.set(x0 - x, y0 - y, BLUE if explain else colour, only_if=only_if)
            self.set(x0 - y, y0 - x, PURPLE if explain else colour, only_if=only_if)
            self.set(x0 - y, y0 + x, PINK if explain else colour, only_if=only_if)
            self.set(x0 - x, y0 + y, BLACK if explain else colour, only_if=only_if)
        fil.close()


