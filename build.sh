#!/bin/bash
ESC_RED='\033[0;31m'
ESC_GRN='\033[0;32m'
ESC_NC='\033[0m'

mkdir -p frames/overlays

function BLK {
	>&2 printf "${ESC_RED}=* Black circle *=*${ESC_NC}\n"
	./black_circle.py > Black.xpm && convert Black.xpm Black.png
}

function MUL {
	>&2 printf "${ESC_RED}=* Multicolored circle *=*${ESC_NC}\n"
	./multicolor_circle.py > Multicolor.xpm && convert Multicolor.xpm Multicolor.png
}

function smallcirc {
	SCALE=12
	# small_circle.py:16
	SIZE=$(( (((23*2)+3)*$SCALE)+1 ))

	# Scale up
	convert "$1" -scale $(($SCALE*100))% Smaller.png
	# Add grid (slightly edited https://stackoverflow.com/a/49722177)
	# By GeeMack, CC-BY-SA 4.0
	convert Smaller.png \( xc:none[11x11] -background \#c20000 -splice 1x1 -roll +0+0 \) \
	   -set option:distort:viewport "%[fx:u.w]x%[fx:u.h]" -virtual-pixel tile -distort SRT 0 \
	   -compose over -composite Smaller2.png
	# Add one red pixel edge to right-side and bottom
	convert Smaller2.png -background \#c20000 -extent ${SIZE}x${SIZE} Smaller3.png

	rm Small{er,er2}.png
	mv Smaller3.png "$2"
}

function SML {
	>&2 printf "${ESC_RED}=* Small circle with overlayed grid *=*${ESC_NC}\n"
	./small_circle.py > Small.xpm && convert Small.xpm Small.png
	smallcirc Small.png Small.png
}

function GIF {
	>&2 printf "${ESC_RED}=* GIF: draw circle, record data *=*${ESC_NC}\n"
	./recorded_gif.py
	>&2 printf "${ESC_RED}=* GIF: Increase size 10x (Magick) *=*${ESC_NC}\n"
	for f in frames/*.xpm; do smallcirc "$f" "$f".png; done
	>&2 printf "${ESC_RED}=* GIF: Make overlays *=*${ESC_NC}\n"
	./make_overlays.py
	>&2 printf "${ESC_RED}=* GIF: Paint overlay (Magick) *=*${ESC_NC}\n"
	TEMPFILE=`mktemp`
	for f in frames/overlays/*; do convert "frames/${f##*/}" "$f" -flatten $TEMPFILE.png && mv $TEMPFILE.png "frames/F${f##*/}"; done
	>&2 printf "${ESC_RED}=* GIF: Final GIF (Magick) *=*${ESC_NC}\n"
	# We repeat last frame three times to make a little delay.
	cd frames
	LS=`ls F*`
	LAST=${LS##*$'\n'}
	convert -delay 40 F*.png $LAST $LAST -loop 0 -layers Optimize '../Animation.gif'
}

if test $# -eq 0; then
	BLK
	SML
	MUL
	GIF
fi

while test $# -gt 0
do
    case "$1" in
        BLK) BLK
            ;;
        SML) SML
            ;;
        MUL) MUL
            ;;
        GIF) GIF
            ;;
    esac
    shift
done

>&2 printf "${ESC_GRN}Done${ESC_NC}\n"
