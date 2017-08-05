#!/usr/bin/env python

import argparse
import base64
import json
import struct
import textwrap
import zlib

from .aries import parseDocument, getChild
from .util import ensure_dir_path_exists

def main():
    parser = argparse.ArgumentParser(description='Convert ika map file')
    parser.add_argument('source_path')
    parser.add_argument('dest_path')
    args = parser.parse_args()

    export_map(args.source_path, args.dest_path)

def export_map(source_path, dest_path):
    ensure_dir_path_exists(dest_path)
    obj = readMap(source_path)
    with open(dest_path, 'wt') as f:
        f.write(json.dumps(obj, separators=(',',':')))

def readMap(path):
    with open(path, 'rt') as f:
        data = f.read()
    doc = parseDocument(data)
    if doc[0] != 'ika-map':
        raise Exception("expected document type ika-map")
    version = getChild(doc, 'version')[1]
    # There are other map versions, but they are all 1.0 for this game.  Main
    # difference is in how base64 stuff is calculated?
    if version != '1.0':
        raise Exception("Version '%s' not supported" % version)
    # There are a bunch more fields, but their values are constant for this
    # game.
    specText = textwrap.dedent("""\
        information                         obj
            meta                            obj
                entityLayer                 string
                music                       string
        header                              obj
            dimensions                      obj
                width                       int
                height                      int
            tileset                         string
        layers                              array
            layer                           obj
                label                       string
                dimensions                  obj
                    width                   int
                    height                  int
                position                    obj
                    x                       int
                    y                       int
                parallax                    obj
                    mulx                    int
                    muly                    int
                    divx                    int
                    divy                    int
                data                        layerdata
                obstructions                obsdata
                entities                    array
                    entity                  obj
                        label               string
                        x                   int
                        y                   int
                        sprite              string
                zones                       array
                    zone                    obj
                        label               string
                        x                   int
                        y                   int
                        width               int
                        height              int
        zones                               array
            zone                            obj
                label                       string
                script                      string
    """).strip()
    def parseSpec(s):
        header = None
        childLines = []
        for line in s.splitlines():
            if line.startswith(' '):
                childLines.append(line)
            else:
                if header is not None:
                    if childLines:
                        yield (header.split(), list(parseSpec(textwrap.dedent('\n'.join(childLines)))))
                    else:
                        yield (header.split(), [])
                header = line
                childLines = []
        if childLines:
            yield (header.split(), list(parseSpec(textwrap.dedent('\n'.join(childLines)))))
        else:
            yield (header.split(), [])
    spec = list(parseSpec(specText))

    def parseInt(node, childSpecs, parent_wip):
        return int(node[1])

    def parseString(node, childSpecs, parent_wip):
        return ''.join(node[1:])

    def parseArray(node, childSpecs, parent_wip):
        vs = []
        [((name, type), subChildSpecs)] = childSpecs
        parser = parsers.get(type, parseDefault)
        for child in node[1:]:
            vs.append(parser(child, subChildSpecs, vs))
        return vs

    def parseLayerdata(node, childSpecs, parent_wip):
        if getChild(node, 'format')[1] != 'zlib':
            raise Exception("unrecognized layer format")
        compressed_base64 = ''.join(node[2:])
        compressed_data = base64.b64decode(compressed_base64)
        decompressor = zlib.decompressobj()
        dimensions = parent_wip['dimensions']
        width = dimensions['width']
        height = dimensions['height']
        value_count = width * height
        byte_data = decompressor.decompress(compressed_data, value_count * 4)
        return list(struct.unpack('<%dI' % value_count, byte_data))

    def parseObsdata(node, childSpecs, parent_wip):
        if getChild(node, 'format')[1] != 'tile':
            raise Exception("unrecognized obstruction format")
        compressed_base64 = ''.join(node[2:])
        compressed_data = base64.b64decode(compressed_base64)
        decompressor = zlib.decompressobj()
        dimensions = parent_wip['dimensions']
        width = dimensions['width']
        height = dimensions['height']
        value_count = width * height
        byte_data = decompressor.decompress(compressed_data, value_count)
        obs_data = list(struct.unpack('<%dB' % value_count, byte_data))
        if sum(obs_data) == 0:
            return []
        else:
            return obs_data

    parsers = {
        'array': parseArray,
        'int': parseInt,
        'layerdata': parseLayerdata,
        'obsdata': parseObsdata,
        'string': parseString,
    }

    def parseDefault(node, childSpecs, parent_wip):
        d = {}
        for ((name, type), subChildSpecs) in childSpecs:
            child = getChild(node, name)
            if child is None:
                d[name] = None
            else:
                parser = parsers.get(type, parseDefault)
                d[name] = parser(child, subChildSpecs, d)
        return d

    return parseDefault(doc, spec, None)

if __name__ == '__main__':
    main()

