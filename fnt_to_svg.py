#!/usr/bin/env python3

import os
import math

def polyline(output, poly):
    """
    Create svg polyline from list of points
    """
    print('<polyline points="', sep='', end='', file=output)
    for point in poly:
        print(point[0], ',', point[1], sep='', end=' ', file=output)

    print('" stroke="black" stroke-width="1" fill="none" />', file=output)

def font2svg(font_file):
    """
    font2svg - Create SVG image of the entire font
    """
    min_x = min_y = max_x = max_y = 0

    spacing = 32
    height = 55

    pos_x = spacing * 2
    pos_y = height * 2 - spacing/2

    svg_file = "images/" + os.path.splitext(os.path.basename(font_file))[0] + ".svg"
    svg = open(svg_file, "w")

    with open(font_file, "rb", buffering=0) as file:
        characters = int.from_bytes(file.read(2), 'little')
        if (characters > 96):
            begin_at = 0
            end_at = math.ceil(characters / 16)
        else:
            begin_at = 2
            end_at = 8

        svg_height = (end_at-begin_at+2)*height

        print(f'<svg width="608" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">', file=svg)
        print('<style>.small { font: italic 13px sans-serif; }</style>', file=svg)
        print(f'<rect x="0" y="0" width="608" height="{svg_height-23}" fill="lightyellow" stroke-width="4" stroke="black" />', file=svg)
        print('<line x1="5" y1="55" x2="603" y2="55" stroke="lightgrey" stroke-width="1" />', file=svg)
        print(f'<line x1="55" y1="5" x2="55" y2="{svg_height-26}" stroke="lightgrey" stroke-width="1" />', file=svg)
        print(f'<text x="{spacing/2}" y="{height-24}" class="small">hex</text>', sep='', file=svg)

        for idx in range(begin_at, end_at):
            print(f'<text x="20" y="{(idx-begin_at+2)*height-8}" font-size="large">{idx:X}x</text>', sep='', file=svg)

        for idx in range(0, 16):
            print(f'<text x="{(idx+2)*spacing+8}" y="{height-20}" font-size="large">{idx:X}</text>', sep='', file=svg)

        for char in range(characters):
            vectors = []
            loc_offset = (char+1)*2
            file.seek(loc_offset)
            offset_loc = int.from_bytes(file.read(2), 'little')
            file.seek(offset_loc)
            length, left, right = file.read(3)

            left -= 0x52            # Position left side of the glyph
            right -= 0x52           # Position right side of the glyph

            if (char) % 16 == 0:
                pos_y += height
                pos_x = spacing * 2

            for _ in range(length):
                vector_x, vector_y = file.read(2)
                vector_x -= 0x52
                vector_y -= 0x52

                if vector_x > max_x:
                    max_x = vector_x
                if vector_y > max_y:
                    max_y = vector_y

                if vector_x < min_x:
                    min_x = vector_x
                if vector_y < min_y:
                    min_y = vector_y

                vector_y = height - vector_y

                if vector_x == -50:
                    polyline(svg, vectors)
                    vectors = []
                    continue

                vectors.append((pos_x + vector_x - left, pos_y - vector_y))

            polyline(svg, vectors)
            vectors = []

            pos_x += spacing

    print(f'<text x="370" y="{svg_height-height/1.6}" font-size="smaller">Max Height {max_y-min_y} Width {max_y-min_y}</text>', sep='', file=svg)

    print("</svg>", file=svg)
    svg.close()
    file.close()


font2svg("fonts/astrol.fnt")
font2svg("fonts/cyrilc.fnt")
font2svg("fonts/gotheng.fnt")
font2svg("fonts/gothger.fnt")
font2svg("fonts/gothita.fnt")
font2svg("fonts/greekc.fnt")
font2svg("fonts/greekcs.fnt")
font2svg("fonts/greeks.fnt")
font2svg("fonts/greekp.fnt")
font2svg("fonts/italicc.fnt")
font2svg("fonts/italiccs.fnt")
font2svg("fonts/italict.fnt")
font2svg("fonts/lowmat.fnt")
font2svg("fonts/marker.fnt")
font2svg("fonts/meteo.fnt")
font2svg("fonts/music.fnt")
font2svg("fonts/romanc.fnt")
font2svg("fonts/romancs.fnt")
font2svg("fonts/romand.fnt")
font2svg("fonts/romans.fnt")
font2svg("fonts/romant.fnt")
font2svg("fonts/romanp.fnt")
font2svg("fonts/scriptc.fnt")
font2svg("fonts/scripts.fnt")
font2svg("fonts/symbol.fnt")
font2svg("fonts/uppmat.fnt")
font2svg("fonts/misc.fnt")
font2svg("fonts/japan.fnt")
