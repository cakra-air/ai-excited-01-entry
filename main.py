import os
import zlib
import struct
import math
import random

WIDTH = 768
HEIGHT = 768
SEED = 20261116


def generate_pixels():
    rng = random.Random(SEED)
    noise = [rng.random() for _ in range(256)]
    buf = bytearray()
    for y in range(HEIGHT):
        yy = y / HEIGHT
        for x in range(WIDTH):
            xx = x / WIDTH
            a = math.sin(xx * 8.0 + yy * 4.0 + SEED * 0.001)
            b = math.sin((xx * xx + yy * yy) * 20.0)
            c = math.sin(xx * 12.0) * math.cos(yy * 12.0)
            n = noise[int((x + y * 7) % 256)]
            v = (a + b + c + n) / 4.0
            v = (v + 1.0) / 2.0
            v = max(0.0, min(1.0, v))
            h = v * 0.8 + 0.6
            r = math.sin(math.pi * h) ** 2
            g = math.sin(math.pi * (h + 1.0 / 3.0)) ** 2
            b = math.sin(math.pi * (h + 2.0 / 3.0)) ** 2
            r = min(255, int(r * 255 * 1.2 + 30))
            g = min(255, int(g * 255 * 1.1 + 20))
            b = min(255, int(b * 255 * 1.3 + 40))
            buf += bytes((r, g, b))
    return bytes(buf)


def write_png(path, width, height, raw):
    def chunk(chunk_type, data):
        c = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", c)

    scanlines = bytearray()
    row_len = width * 3
    for i in range(0, len(raw), row_len):
        scanlines.append(0)
        scanlines += raw[i:i + row_len]

    compressed = zlib.compress(bytes(scanlines), 9)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    raw = generate_pixels()
    write_png(path, WIDTH, HEIGHT, raw)
    print("Wrote " + path)


if __name__ == "__main__":
    main()