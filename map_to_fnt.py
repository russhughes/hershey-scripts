#!/usr/bin/env python3

"""
Convert Hershey data using hmp files to create DrawBot fnt files
"""

from struct import pack
import re
from parse import parse

vectors = {}
vectors_count = {}
vectors_used = {}

def hershey_load(glyph_file_name):
    """
    Load Hershey glyphs
    """
    global vectors, vectors_count, vectors_used

    vectors = {}
    vectors_count = {}
    vectors_used = {}

    print(glyph_file_name)

    # Read the glyphs file handling the continuation line
    with open(glyph_file_name, "r") as file:
        for raw_line in file:
            match = re.match('^([0-9 ]{4}[0-9]{1})([0-9 ]{2}[0-9]{1})(.*)$', raw_line.rstrip())
            if match:
                glyph_num = int(match.group(1))
                glyph_len = int(match.group(2))
                vectors[glyph_num] = match.group(3)
                vectors_count[glyph_num] = glyph_len -1
                vectors_used[glyph_num] = False
            else:
                line = raw_line.rstrip()
                vectors[glyph_num] += line

def map_to_fnt(map_file_name, font_file_name):
    """
    Convert Hershey data with hmp file to create DrawBot fnt file
    """

    global vectors, vectors_count, vectors_used

    offsets = {}
    offset = 0

    font_vectors = {}
    font_count = {}

    print(map_file_name, font_file_name)
    # Read the map file and build FONT[]
    with open(map_file_name, "r") as file:
        glyph_counter = 0
        for raw_line in file:
            hmp_entry = parse("{:d} {:d}", raw_line)
            if hmp_entry:
                if hmp_entry[1] is not 0:
                    for glyph in range(hmp_entry[0], hmp_entry[1]+1):
                        if vectors[glyph] is not None:
                            vectors_used[glyph] = True
                            font_vectors[glyph_counter] = vectors.get(glyph)
                            font_count[glyph_counter] = vectors_count.get(glyph)
                            offsets[glyph_counter] = offset
                            offset += len(font_vectors[glyph_counter])+1
                            glyph_counter += 1
                        else:
                            raise Exception("glyph {glyph} referenced but not found.")
                else:
                    glyph = hmp_entry[0]
                    vectors_used[glyph] = True
                    font_vectors[glyph_counter] = vectors.get(glyph)
                    font_count[glyph_counter] = vectors_count.get(glyph)

                    offsets[glyph_counter] = offset
                    offset += len(font_vectors[glyph_counter])+1

                    glyph_counter += 1

    # Write the FONT[] to the fnt file
    with open(font_file_name, "wb") as file:
        # 16 bit integer in little endian order with number of glyphs in FONT[]
        file.write(pack('<h', glyph_counter))
        #print("glyphs in font ", font_file_name, glyph_counter)

        # 16 bit integer table to the beginning of the vector data for each glyph in the FONT[]
        for offset in offsets:
            file.write(pack('<h', offsets[offset]+glyph_counter*2+2))
            #print("offset", offset, "location: ", offsets[offset]+glyph_counter*2+2)
        # vectors for each glyph in the FONT[]
        for glyph in font_vectors:
            #print(f'is glyph {glyph}')
            file.write(pack("B", font_count[glyph]))
            file.write(bytes(font_vectors[glyph], 'utf-8'))
            #print("Vectors for", glyph, "length", font_count[glyph], font_vectors[glyph])

hershey_load("hershey/hersh-fixed.oc")

map_to_fnt("hershey/astrol.hmp", "fonts/astrol.fnt")
map_to_fnt("hershey/cyrilc.hmp", "fonts/cyrilc.fnt")
map_to_fnt("hershey/gotheng.hmp", "fonts/gotheng.fnt")
map_to_fnt("hershey/gothger.hmp", "fonts/gothger.fnt")
map_to_fnt("hershey/gothita.hmp", "fonts/gothita.fnt")
map_to_fnt("hershey/greekc.hmp", "fonts/greekc.fnt")
map_to_fnt("hershey/greekcs.hmp", "fonts/greekcs.fnt")
map_to_fnt("hershey/greeks.hmp", "fonts/greeks.fnt")
map_to_fnt("hershey/greekp.hmp", "fonts/greekp.fnt")
map_to_fnt("hershey/italicc.hmp", "fonts/italicc.fnt")
map_to_fnt("hershey/italiccs.hmp", "fonts/italiccs.fnt")
map_to_fnt("hershey/italict.hmp", "fonts/italict.fnt")
map_to_fnt("hershey/lowmat.hmp", "fonts/lowmat.fnt")
map_to_fnt("hershey/marker.hmp", "fonts/marker.fnt")
map_to_fnt("hershey/meteo.hmp", "fonts/meteo.fnt")
map_to_fnt("hershey/music.hmp", "fonts/music.fnt")
map_to_fnt("hershey/romanc.hmp", "fonts/romanc.fnt")
map_to_fnt("hershey/romancs.hmp", "fonts/romancs.fnt")
map_to_fnt("hershey/romand.hmp", "fonts/romand.fnt")
map_to_fnt("hershey/romans.hmp", "fonts/romans.fnt")
map_to_fnt("hershey/romant.hmp", "fonts/romant.fnt")
map_to_fnt("hershey/scriptc.hmp", "fonts/scriptc.fnt")
map_to_fnt("hershey/scripts.hmp", "fonts/scripts.fnt")
map_to_fnt("hershey/symbol.hmp", "fonts/symbol.fnt")
map_to_fnt("hershey/uppmat.hmp", "fonts/uppmat.fnt")
map_to_fnt("hershey/romanp.hmp", "fonts/romanp.fnt")

with open("hershey/misc.hmp", "w") as file:
    for glyph in vectors_used:
        if not vectors_used[glyph]:
            print(f'{glyph} 0', file=file)

map_to_fnt("hershey/misc.hmp", "fonts/misc.fnt")

print('glyph map:')
character = 0
for glyph in vectors_used:
    if not vectors_used[glyph]:
        print(f'{character:X} {glyph}')
        character += 1

hershey_load("hershey/hersh.or")
map_to_fnt("hershey/japan.hmp", "fonts/japan.fnt")
