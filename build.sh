#!/bin/bash
ESC_RED='\033[0;31m'
ESC_GRN='\033[0;32m'
ESC_NC='\033[0m'

>&2 printf "${ESC_RED}=* Black circle *=*${ESC_NC}\n"
./black_circle.py > Black.xpm && convert Black.xpm Black.png

>&2 printf "${ESC_RED}=* Multicolored circle *=*${ESC_NC}\n"
./multicolor_circle.py > Multicolor.xpm && convert Multicolor.xpm Multicolor.png

>&2 printf "${ESC_RED}=* Small circle with overlayed grid *=*${ESC_NC}\n"
./small_circle.py > Small.xpm && convert Small.xpm Small.png

SCALE=12
# small_circle.py:16
SIZE=$(( (((23*2)+3)*$SCALE)+1 ))

# Scale up
convert Small.png -scale $(($SCALE*100))% Smaller.png
# Add grid (slightly edited https://stackoverflow.com/a/49722177)
# By GeeMack, CC-BY-SA 4.0
convert Smaller.png \( xc:none[11x11] -background \#c20000 -splice 1x1 -roll +0+0 \) \
   -set option:distort:viewport "%[fx:u.w]x%[fx:u.h]" -virtual-pixel tile -distort SRT 0 \
   -compose over -composite Smaller2.png
# Add one red pixel edge to right-side and bottom
convert Smaller2.png -background \#c20000 -extent ${SIZE}x${SIZE} Smaller3.png

>&2 printf "${ESC_RED}=* Cleanup *=*${ESC_NC}\n"
rm Small{,er,er2}.png
mv Smaller3.png Small.png

>&2 printf "${ESC_GRN}Done${ESC_NC}\n"
