#!/usr/bin/env python

import argparse
import base64
import sys
import zlib
from PIL import Image

from .aries import parseDocument, getChild
from .util import ensure_dir_path_exists

def main():
    parser = argparse.ArgumentParser(description='Convert ika sprite file')
    parser.add_argument('source_path')
    parser.add_argument('dest_path')
    args = parser.parse_args()

    export_sprite(args.source_path, args.dest_path)

def export_sprite(source_path, dest_path):
    ensure_dir_path_exists(dest_path)
    sprite = readSprite(source_path)
    writeSpriteImage(sprite, dest_path)

def readSprite(path):
    with open(path, 'rt') as f:
        data = f.read()
    doc = parseDocument(data)
    if doc[0] != 'ika-sprite':
        raise Exception("expected document type ika-sprite")
    version = getChild(doc, 'version')[1]
    if version != '1.0':
        raise Exception("Version '%s' not supported" % version)
    # TODO: infomation?
    # TODO: header?
    # TODO: scripts?
    frames = getChild(doc, 'frames')
    frame_count = int(getChild(frames, 'count')[1])

    dimensions = getChild(frames, 'dimensions')
    width = int(getChild(dimensions, 'width')[1])
    height = int(getChild(dimensions, 'height')[1])

    hotspot = getChild(frames, 'hotspot')
    hotspotX = int(getChild(hotspot, 'x')[1])
    hotspotY = int(getChild(hotspot, 'y')[1])
    hotspotWidth = int(getChild(hotspot, 'width')[1])
    hotspotHeight = int(getChild(hotspot, 'height')[1])

    data = getChild(frames, 'data')
    format = getChild(data, 'format')[1]
    if format != 'zlib':
        raise Exception("Format '%s' not supported" % format)

    # Note: Ika source has two implementations of base64, and it says the old
    # one (used in version 1.0) is wrong.  Not sure exactly what is wrong...
    # Hopefully the Python base64 still works on it.
    compressed_base64 = ''.join(data[2:])
    compressed_data = base64.b64decode(compressed_base64)
    frame_data_size = width * height * 4
    pix_data_size = frame_data_size * frame_count
    decompressor = zlib.decompressobj()
    pix_data = decompressor.decompress(compressed_data, pix_data_size)
    frames = []
    for i in range(frame_count):
        frames.append(pix_data[i * frame_data_size:(i+1) * frame_data_size])

    sprite = Sprite(
        width=width,
        height=height,
        frames=frames,
        hotspotX=hotspotX,
        hotspotY=hotspotY,
        hotspotWidth=hotspotWidth,
        hotspotHeight=hotspotHeight,
    )
    return sprite

def writeSpriteImage(sprite, path):
    num_cols = 8
    num_rows = (len(sprite.frames) + num_cols - 1) // num_cols
    im_width = sprite.width * num_cols
    im_height = sprite.height * num_rows
    sprite_im = Image.new("RGBA", (im_width, im_height))
    for i, frame_data in enumerate(sprite.frames):
        im = Image.frombytes("RGBA", (sprite.width, sprite.height), frame_data)
        x = (i % num_cols) * sprite.width
        y = (i // num_cols) * sprite.height
        sprite_im.paste(im, (x, y))
    sprite_im.save(path)

class Sprite(object):
    def __init__(
        self,
        width,
        height,
        frames,
        hotspotX,
        hotspotY,
        hotspotWidth,
        hotspotHeight,
    ):
        self.width = width
        self.height = height
        self.frames = frames
        self.hotspotX = hotspotX
        self.hotspotY = hotspotY
        self.hotspotWidth = hotspotWidth
        self.hotspotHeight = hotspotHeight

if __name__ == '__main__':
    main()
