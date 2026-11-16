import os
import zlib
import struct
import math
import random

WIDTH = 1024
HEIGHT = 1024
SEED = 20261116


def plasma(x, y, seed):
    r = random.Random(seed)
    a = math.sin(x / 37.0 + y / 71.0)
    b = math.sin((x * x + y * y) / 4000.0)
    c = math.sin(x / 19.0) * math.cos(y / 29.0)
    j = r.random()
    v = (a + b + c + j) / 4.0
    return v


def hue_to_rgb(h):
    r = math.sin(math.pi * (h + 0.0)) ** 2
    g = math.sin(math.pi * (h + 1.0 / 3.0)) ** 2
    b = math.sin(math.pi * (h + 2.0 / 3.0)) ** 2
    return int(r * 255), int(g * 255), int(b * 255)


def generate_pixels():
    pixels = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            v = plasma(x, y, SEED)
            v = (v + 1.0) / 2.0
            v = max(0.0, min(1.0, v))
            h = v * 0.8 + 0.6
            r, g, b = hue_to_rgb(h)
            r = min(255, int(r * 1.2 + 30))
            g = min(255, int(g * 1.1 + 20))
            b = min(255, int(b * 1.3 + 40))
            row.append((r, g, b))
        pixels.append(row)
    return pixels


def write_png(path, width, height, pixels):
    def chunk(chunk_type, data):
        c = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", c)

    raw = b""
    for row in pixels:
        raw += b"\x00"
        for r, g, b in row:
            raw += bytes((r, g, b))

    compressed = zlib.compress(raw, 6)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(png)


def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    pixels = generate_pixels()
    write_png(path, WIDTH, HEIGHT, pixels)
    print("Wrote " + path)


if __name__ == "__main__":
    main()
