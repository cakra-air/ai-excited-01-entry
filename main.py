#!/usr/bin/env python3
"""
ai-excited-01 entry: Generates a deterministic, exciting image of an exploding cosmic event.
A supernova birth - energy, motion, surprise, and awe in one frame.
Deterministic: same bytes every run, no network, stdlib only.
"""

import os
import sys
import struct
import zlib
import math
import random
from typing import List, Tuple

# Deterministic seeded RNG
SEED = 0xA1E7C17ED  # hex for "ai-excited-01" seed
rng = random.Random(SEED)

# Image constraints
WIDTH = 1024
HEIGHT = 1024
MAX_BYTES = 1048576  # 1 MiB


def seeded_float() -> float:
    """Return deterministic float in [0, 1)."""
    return rng.random()


def seeded_int(a: int, b: int) -> int:
    """Return deterministic int in [a, b]."""
    return rng.randint(a, b)


def write_png(path: str, pixels: List[List[Tuple[int, int, int, int]]]) -> None:
    """Write PNG using stdlib only (zlib + struct)."""
    height = len(pixels)
    width = len(pixels[0]) if height > 0 else 0

    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)

    # IDAT chunk: compress scanlines with filter type 0 (none)
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0
        for x in range(width):
            r, g, b, a = pixels[y][x]
            raw.append(r)
            raw.append(g)
            raw.append(b)
            raw.append(a)
    compressed = zlib.compress(raw, level=9)
    idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    png += struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)

    # IEND chunk
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    png += struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)

    with open(path, 'wb') as f:
        f.write(png)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """Convert HSV to RGB (0-255)."""
    h = h % 1.0
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return (int(r * 255), int(g * 255), int(b * 255))


def generate_explosion() -> List[List[Tuple[int, int, int, int]]]:
    """Generate a deterministic cosmic explosion image."""
    # Initialize canvas with deep space background
    pixels = [[(5, 3, 15, 255) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    cx, cy = WIDTH // 2, HEIGHT // 2
    max_r = min(WIDTH, HEIGHT) * 0.48

    # Layer 1: Background nebula clouds (fractal noise)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = (x - cx) / max_r
            dy = (y - cy) / max_r
            dist = math.sqrt(dx * dx + dy * dy)

            # Multi-octave noise for nebula
            noise_val = 0.0
            freq = 0.003
            amp = 1.0
            for _ in range(5):
                nx = x * freq + seeded_float() * 1000
                ny = y * freq + seeded_float() * 1000
                # Simple value noise
                ix, iy = int(nx), int(ny)
                fx, fy = nx - ix, ny - iy
                # Hash-based pseudo-random
                h1 = (ix * 73856093) ^ (iy * 19349663) ^ 83492791
                h2 = ((ix + 1) * 73856093) ^ (iy * 19349663) ^ 83492791
                h3 = (ix * 73856093) ^ ((iy + 1) * 19349663) ^ 83492791
                h4 = ((ix + 1) * 73856093) ^ ((iy + 1) * 19349663) ^ 83492791
                v1 = (h1 & 0xffff) / 65535.0
                v2 = (h2 & 0xffff) / 65535.0
                v3 = (h3 & 0xffff) / 65535.0
                v4 = (h4 & 0xffff) / 65535.0
                # Bilinear interpolation
                interp_x1 = v1 * (1 - fx) + v2 * fx
                interp_x2 = v3 * (1 - fx) + v4 * fx
                noise_val += (interp_x1 * (1 - fy) + interp_x2 * fy) * amp
                freq *= 2.0
                amp *= 0.5

            # Apply nebula with distance falloff
            nebula_strength = noise_val * (1.0 - dist * 0.8)
            if nebula_strength > 0.15:
                hue = 0.55 + nebula_strength * 0.15  # Blue-purple to magenta
                sat = 0.6 + nebula_strength * 0.3
                val = 0.15 + nebula_strength * 0.25
                r, g, b = hsv_to_rgb(hue, sat, val)
                # Blend with background
                br, bg, bb, _ = pixels[y][x]
                pixels[y][x] = (
                    min(255, br + int(r * 0.3)),
                    min(255, bg + int(g * 0.3)),
                    min(255, bb + int(b * 0.3)),
                    255
                )

    # Layer 2: Shockwave rings (expanding energy)
    num_rings = 12
    for ring in range(num_rings):
        ring_progress = (ring + seeded_float() * 0.3) / num_rings
        ring_radius = max_r * ring_progress
        ring_width = max(2, int(max_r * 0.02 * (1 - ring_progress * 0.5)))

        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                dist = math.sqrt(dx * dx + dy * dy)
                diff = abs(dist - ring_radius)

                if diff < ring_width:
                    intensity = 1.0 - (diff / ring_width)
                    intensity = intensity * intensity  # Quadratic falloff

                    # Color shifts from hot white to blue to purple
                    hue = 0.55 + (1.0 - ring_progress) * 0.15
                    sat = 0.3 + intensity * 0.5
                    val = 0.5 + intensity * 0.5
                    r, g, b = hsv_to_rgb(hue, sat, val)

                    br, bg, bb, _ = pixels[y][x]
                    blend = intensity * 0.8
                    pixels[y][x] = (
                        min(255, br + int(r * blend)),
                        min(255, bg + int(g * blend)),
                        min(255, bb + int(b * blend)),
                        255
                    )

    # Layer 3: Particle burst - thousands of glowing particles
    num_particles = 3000
    for _ in range(num_particles):
        # Random angle and distance from center
        angle = seeded_float() * 2 * math.pi
        # Biased toward outer regions for explosion feel
        dist_factor = seeded_float() ** 0.5  # sqrt for outward bias
        radius = max_r * (0.15 + dist_factor * 0.8)

        px = int(cx + radius * math.cos(angle))
        py = int(cy + radius * math.sin(angle))

        # Particle size (1-4 pixels)
        p_size = seeded_int(1, 3)

        # Particle color: hot core to cooler edges
        heat = 1.0 - (radius / max_r)
        hue = 0.05 + heat * 0.15  # Red-orange to yellow
        sat = 0.8 + heat * 0.2
        val = 0.9 + heat * 0.1
        r, g, b = hsv_to_rgb(hue, sat, val)

        # Draw particle as small glow
        for dy in range(-p_size, p_size + 1):
            for dx in range(-p_size, p_size + 1):
                x, y = px + dx, py + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    pdist = math.sqrt(dx * dx + dy * dy)
                    if pdist <= p_size:
                        intensity = 1.0 - (pdist / (p_size + 0.5))
                        br, bg, bb, _ = pixels[y][x]
                        blend = intensity * 0.9
                        pixels[y][x] = (
                            min(255, br + int(r * blend)),
                            min(255, bg + int(g * blend)),
                            min(255, bb + int(b * blend)),
                            255
                        )

    # Layer 4: Core flare - intense central burst
    core_radius = int(max_r * 0.12)
    for y in range(max(0, cy - core_radius), min(HEIGHT, cy + core_radius + 1)):
        for x in range(max(0, cx - core_radius), min(WIDTH, cx + core_radius + 1)):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < core_radius:
                intensity = 1.0 - (dist / core_radius)
                intensity = intensity ** 3  # Sharp core

                # Blinding white-hot center
                r = min(255, int(255 * (0.7 + intensity * 0.3)))
                g = min(255, int(255 * (0.8 + intensity * 0.2)))
                b = min(255, int(255 * (0.9 + intensity * 0.1)))

                br, bg, bb, _ = pixels[y][x]
                pixels[y][x] = (
                    min(255, br + int(r * intensity)),
                    min(255, bg + int(g * intensity)),
                    min(255, bb + int(b * intensity)),
                    255
                )

    # Layer 5: Radial light rays (god rays / volumetric light)
    num_rays = 32
    for ray in range(num_rays):
        base_angle = (ray / num_rays) * 2 * math.pi
        # Slight randomization per ray
        angle = base_angle + (seeded_float() - 0.5) * 0.05
        ray_width = 0.008 + seeded_float() * 0.012

        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - cx
                dy = y - cy
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > max_r * 0.2:
                    pixel_angle = math.atan2(dy, dx)
                    angle_diff = abs(pixel_angle - angle)
                    if angle_diff > math.pi:
                        angle_diff = 2 * math.pi - angle_diff

                    if angle_diff < ray_width * (1 + dist / max_r * 0.5):
                        intensity = (1.0 - angle_diff / (ray_width * (1 + dist / max_r * 0.5))) * 0.3
                        intensity *= (1.0 - dist / max_r)  # Fade with distance
                        if intensity > 0:
                            r = min(255, int(255 * (0.9 + intensity * 0.1)))
                            g = min(255, int(255 * (0.85 + intensity * 0.1)))
                            b = min(255, int(200 * (0.7 + intensity * 0.2)))

                            br, bg, bb, _ = pixels[y][x]
                            pixels[y][x] = (
                                min(255, br + int(r * intensity)),
                                min(255, bg + int(g * intensity)),
                                min(255, bb + int(b * intensity)),
                                255
                            )

    # Layer 6: Floating debris / asteroid fragments (surprise element)
    num_debris = 150
    for _ in range(num_debris):
        angle = seeded_float() * 2 * math.pi
        radius = max_r * (0.2 + seeded_float() * 0.9)
        px = int(cx + radius * math.cos(angle))
        py = int(cy + radius * math.sin(angle))
        size = seeded_int(3, 12)

        # Debris color: rocky, metallic
        hue = 0.05 + seeded_float() * 0.1
        sat = 0.2 + seeded_float() * 0.3
        val = 0.3 + seeded_float() * 0.4
        r, g, b = hsv_to_rgb(hue, sat, val)

        # Draw irregular debris shape
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                x, y = px + dx, py + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    pdist = math.sqrt(dx * dx + dy * dy)
                    # Irregular shape using noise
                    noise = (seeded_int(0, 1000) / 1000.0) * 0.3
                    if pdist < size * (0.7 + noise):
                        intensity = 1.0 - (pdist / (size * (0.7 + noise)))
                        br, bg, bb, _ = pixels[y][x]
                        blend = intensity * 0.7
                        pixels[y][x] = (
                            min(255, br + int(r * blend)),
                            min(255, bg + int(g * blend)),
                            min(255, bb + int(b * blend)),
                            255
                        )

    # Layer 7: Chromatic aberration / lens flare hints (craft detail)
    for _ in range(20):
        angle = seeded_float() * 2 * math.pi
        radius = max_r * (0.5 + seeded_float() * 0.4)
        px = int(cx + radius * math.cos(angle))
        py = int(cy + radius * math.sin(angle))
        size = seeded_int(8, 25)

        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                x, y = px + dx, py + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    pdist = math.sqrt(dx * dx + dy * dy)
                    if pdist < size:
                        intensity = (1.0 - pdist / size) * 0.15
                        # Chromatic shift
                        r_shift = int(50 * intensity * (seeded_float() - 0.5))
                        b_shift = int(50 * intensity * (seeded_float() - 0.5))
                        br, bg, bb, _ = pixels[y][x]
                        pixels[y][x] = (
                            min(255, max(0, br + r_shift)),
                            bg,
                            min(255, max(0, bb + b_shift)),
                            255
                        )

    return pixels


def main() -> None:
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'entry.png')

    print(f'Generating image: {WIDTH}x{HEIGHT}...')
    pixels = generate_explosion()

    print(f'Writing PNG to {out_path}...')
    write_png(out_path, pixels)

    # Verify file size
    size = os.path.getsize(out_path)
    print(f'Done. File size: {size} bytes ({size / 1024:.1f} KiB)')
    if size > MAX_BYTES:
        print(f'WARNING: Exceeds {MAX_BYTES} byte limit!', file=sys.stderr)
        sys.exit(1)
    print('Within size limit.')


if __name__ == '__main__':
    main()