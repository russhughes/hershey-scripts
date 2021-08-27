#!/usr/bin/env python3

"""
Convert Hershey data with hmp file to create DrawBot python module file
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

def map_to_py(map_file_name, font_file_name):
    """
    Convert Hershey data with hmp file to create python module file
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

    # Write the font_data to the file
    with open(font_file_name, "wt") as outfile:

        # number of glyphs in font
        print(f'def glyphs():\n\treturn {glyph_counter}\n', file=outfile)

        font_data = bytes()
        # vectors for each glyph in the font
        for glyph in font_vectors:
            print("cnt:", font_count[glyph], "vect:", font_vectors[glyph])
            print("")

            f_c = bytearray(font_count[glyph].to_bytes(1, byteorder='little'))
            f_v = bytearray(font_vectors[glyph], 'utf-8')
            font_data += f_c + f_v
            print("f_c:", f_c, "f_v", f_v)

        print("_font =\\", file=outfile)
        print("b'", file=outfile, sep='', end='')
        count = 0
        for byte in (font_data):
            print(f'\\x{byte:02x}', file=outfile, sep='', end='', )
            count += 1
            if count == 15:
                print("'\\\nb'", file=outfile, sep='', end='')
                count = 0

        print("'", file=outfile)

        # 16 bit integer table to the start of the vector data for each glyph in the font
        index_data = bytes()
        for offset in offsets:
            print("for offset:", offsets[offset])
            index_data += bytearray(pack('H', offsets[offset]))

        print("\n_index =\\", file=outfile)
        print("b'", file=outfile, sep='', end='')
        count = 0
        for byte in (index_data):
            print(f'\\x{byte:02x}', file=outfile, sep='', end='', )
            count += 1
            if count == 15:
                print("'\\\nb'", file=outfile, sep='', end='')
                count = 0

        print("'", file=outfile)
        count = 0

        print ("""
_mvfont = memoryview(_font)

def _chr_addr(ordch):
    offset = 2 * (ordch - 32)
    return int.from_bytes(_index[offset:offset + 2], 'little')

def get_ch(ordch):
    offset = _chr_addr(ordch if 32 <= ordch <= 127 else ord('?'))
    count = _font[offset]
    return _mvfont[offset:offset+(count+2)*2-1]

""", file=outfile)

hershey_load("hershey/hersh-fixed.oc")

map_to_py("hershey/astrol.hmp", "pyfont/astrol.py")
map_to_py("hershey/cyrilc.hmp", "pyfont/cyrilc.py")
map_to_py("hershey/gotheng.hmp", "pyfont/gotheng.py")
map_to_py("hershey/gothger.hmp", "pyfont/gothger.py")
map_to_py("hershey/gothita.hmp", "pyfont/gothita.py")
map_to_py("hershey/greekc.hmp", "pyfont/greekc.py")
map_to_py("hershey/greekcs.hmp", "pyfont/greekcs.py")
map_to_py("hershey/greeks.hmp", "pyfont/greeks.py")
map_to_py("hershey/greekp.hmp", "pyfont/greekp.py")
map_to_py("hershey/italicc.hmp", "pyfont/italicc.py")
map_to_py("hershey/italiccs.hmp", "pyfont/italiccs.py")
map_to_py("hershey/italict.hmp", "pyfont/italict.py")
map_to_py("hershey/lowmat.hmp", "pyfont/lowmat.py")
map_to_py("hershey/marker.hmp", "pyfont/marker.py")
map_to_py("hershey/meteo.hmp", "pyfont/meteo.py")
map_to_py("hershey/music.hmp", "pyfont/music.py")
map_to_py("hershey/romanc.hmp", "pyfont/romanc.py")
map_to_py("hershey/romancs.hmp", "pyfont/romancs.py")
map_to_py("hershey/romand.hmp", "pyfont/romand.py")
map_to_py("hershey/romans.hmp", "pyfont/romans.py")
map_to_py("hershey/romant.hmp", "pyfont/romant.py")
map_to_py("hershey/scriptc.hmp", "pyfont/scriptc.py")
map_to_py("hershey/scripts.hmp", "pyfont/scripts.py")
map_to_py("hershey/symbol.hmp", "pyfont/symbol.py")
map_to_py("hershey/uppmat.hmp", "pyfont/uppmat.py")
map_to_py("hershey/romanp.hmp", "pyfont/romanp.py")

with open("hershey/misc.hmp", "w") as file:
    for glyph in vectors_used:
        if not vectors_used[glyph]:
            print(f'{glyph} 0', file=file)

map_to_py("hershey/misc.hmp", "pyfont/misc.py")

print('glyph map:')
character = 0
for glyph in vectors_used:
    if not vectors_used[glyph]:
        print(f'{character:X} {glyph}')
        character += 1

hershey_load("hershey/hersh.or")
map_to_py("hershey/japan.hmp", "pyfont/japan.py")
