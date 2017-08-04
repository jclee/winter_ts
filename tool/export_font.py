#!/usr/bin/env python

import argparse
import struct
import sys
import zlib
from PIL import Image

from .util import ensure_dir_path_exists

def main():
    parser = argparse.ArgumentParser(description='Convert ika font file')
    parser.add_argument('source_path')
    parser.add_argument('dest_path')
    args = parser.parse_args()

    export_font(args.source_path, args.dest_path)

def export_font(source_path, dest_path):
    ensure_dir_path_exists(dest_path)
    font = readFont(source_path)
    writeFontImage(font, dest_path)

def readFont(path):
    with open(path, 'rb') as f:
        data = [f.read()]
    def read(fmt, data=data):
        size = struct.calcsize(fmt)
        d = struct.unpack(fmt, data[0][:size])
        data[0] = data[0][size:]
        return d
    (magic, num_subsets, num_glyphs) = read("<6sBH")
    if magic != b"FONT27":
        raise Exception("Unrecognized font format")
    subsets = []
    for i in range(num_subsets):
        subset = read("<256H")
        subsets.append(subset)
    glyph_sizes = []
    pix_data_size = 0
    for i in range(num_glyphs):
        (w, h) = read("<HH")
        glyph_sizes.append((w, h))
        pix_data_size += (4 * w * h)
    z_pix_data_size = read("<I")
    (z_pix_data,) = read("<%ds" % z_pix_data_size)
    decompressor = zlib.decompressobj()
    pix_data = decompressor.decompress(z_pix_data, pix_data_size)
    data[0] = pix_data
    glyphs = []
    for i, (w, h) in enumerate(glyph_sizes):
        (glyph_data,) = read("<%ds" % (4 * w * h))
        glyphs.append((w, h, glyph_data))
    return Font(subsets, glyphs)

def writeFontImage(font, path):
    max_width = max([x[0] for x in font.glyphs])
    max_height = max([x[1] for x in font.glyphs])
    num_glyphs = len(font.glyphs)

    font_width = max_width * 16
    font_height = max_height * ((num_glyphs + 15) // 16)
    font_im = Image.new("RGBA", (font_width, font_height))
    for i, (w, h, glyph_data) in enumerate(font.glyphs):
        im = Image.frombytes("RGBA", (w, h), glyph_data)
        x = (i % 16) * max_width
        y = (i // 16) * max_height
        font_im.paste(im, (x, y))
    font_im.save(path)

class Font(object):
    def __init__(self, subsets, glyphs):
        self.subsets = subsets
        self.glyphs = glyphs

if __name__ == '__main__':
    main()
