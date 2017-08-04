#!/usr/bin/env python

import argparse
import struct
import sys
import zlib
from PIL import Image

from .util import ensure_dir_path_exists

def main():
    parser = argparse.ArgumentParser(description='Convert ika tile file')
    parser.add_argument('source_path')
    parser.add_argument('dest_path')
    args = parser.parse_args()

    export_tile_lib(args.source_path, args.dest_path)

def export_tile_lib(source_path, dest_path):
    tileLib = readTileLib(source_path)
    writeTileLibImage(tileLib, dest_path)

def readTileLib(path):
    with open(path, 'rb') as f:
        data = [f.read()]
    def read(fmt, data=data):
        size = struct.calcsize(fmt)
        d = struct.unpack(fmt, data[0][:size])
        data[0] = data[0][size:]
        return d
    (version,) = read('<H')
    # Only open ika-specific 32-bpp zlib compressed tiles
    if version != 6:
        raise Exception("Unrecognized tile format")
    (bpp,) = read('<B')
    if bpp != 4:
        raise Exception("Unrecognized tile format")
    (width, height, num_tiles, desc) = read('<HHI64s')
    pix_data_size = width * height * num_tiles * bpp
    z_pix_data_size = read('<I')
    (z_pix_data,) = read('<%ds' % z_pix_data_size)
    decompressor = zlib.decompressobj()
    pix_data = decompressor.decompress(z_pix_data, pix_data_size)
    data[0] = pix_data
    tiles = []
    for i in range(num_tiles):
        (tile_data,) = read("<%ds" % (bpp * width * height))
        tiles.append(tile_data)
    return TileLib(width, height, bpp, desc, tiles)

def writeTileLibImage(tileLib, path):
    num_cols = 16
    num_rows = (len(tileLib.tiles) + num_cols - 1) // num_cols
    tile_im_width = num_cols * tileLib.width
    tile_im_height = num_rows * tileLib.height
    tile_im = Image.new("RGBA", (tile_im_width, tile_im_height))
    for i, tile_data in enumerate(tileLib.tiles):
        im = Image.frombytes("RGBA", (tileLib.width, tileLib.height), tile_data)
        x = (i % num_cols) * tileLib.width
        y = (i // num_cols) * tileLib.height
        tile_im.paste(im, (x, y))
    tile_im.save(path)

class TileLib(object):
    def __init__(self, width, height, bpp, desc, tiles):
        self.width = width
        self.height = height
        self.bpp = bpp
        self.desc = desc
        self.tiles = tiles

if __name__ == '__main__':
    main()
