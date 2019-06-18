#!/usr/bin/env python3

import msgpack
import json
import base64
import os
import sys

def parse_str(s, parent_dir="."):
    if not isinstance(s, str):
        return s

    if s.startswith("PATH: "):
        with open(os.path.join(parent_dir, s.split(": ", 1)[1]), "rb") as f:
            return f.read()
    elif s.startswith("B64: "):
        return base64.decodebytes(s.split(": ", 1)[1].encode())

    return s

def parse_dict(d, parent_dir="."):
    for key in d:
        if isinstance(d[key], dict):
            parse_dict(d[key], parent_dir)
        elif isinstance(d[key], list):
            for i in range(len(d[key])):
                d[key][i] = parse_str(d[key][i], parent_dir)
        else:
            d[key] = parse_str(d[key], parent_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print("Usage: creator.py <json file>")
        print("(this will actually pretty much just pack a json to a msgpack")
        print("but it'll replace `PATH: <path>` with the contents of that path")
        print("and `B64: <b64>` with the base64 decoded bytes)")
    else:
        with open(sys.argv[1]) as f:
            to_pack = json.loads(f.read())

        parse_dict(to_pack, os.path.dirname(sys.argv[1]))

        if len(sys.argv) > 2:
            filename = sys.argv[2]
        else:
            filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
            filename += ".msgpack"

        with open(filename, "wb") as f:
            f.write(msgpack.packb(to_pack, use_bin_type=True))
