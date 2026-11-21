#!/usr/bin/env python3
"""Typesetting helpers for the newsbot21 front page.

The earlier daily editions kept every measurement inside one script.
This page splits the reusable parts out: wrapping, fitting a headline
to its box, and column geometry live here, measured against the same
PIL draw context the page itself is drawn on, so a fit computed here
is a fit on the printed page.
"""

from PIL import ImageFont


def load(path, size):
    return ImageFont.truetype(path, size)


def wrapped(draw, text, font, width):
    """Greedy word wrap: the list of lines that fit inside `width`."""
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        elif line:
            out.append(line)
            line = word
        else:
            line = word
    if line:
        out.append(line)
    return out


def block_height(draw, text, font, width, leading):
    """Pixel height of `text` wrapped at `width`, `leading` per line."""
    return len(wrapped(draw, text, font, width)) * leading


def fit_size(draw, text, font_path, width, max_lines, start, floor=14):
    """Largest size at or below `start` whose wrap of `text` at `width`
    needs at most `max_lines` lines. Never goes below `floor`, so a
    headline that still overflows is visible instead of invisible."""
    size = start
    while size > floor:
        if len(wrapped(draw, text, load(font_path, size), width)) <= max_lines:
            break
        size -= 1
    return size


def columns(total, margin, gutter, count):
    """(x, width) pairs for `count` equal columns across `total`."""
    width = (total - 2 * margin - (count - 1) * gutter) // count
    return [(margin + i * (width + gutter), width) for i in range(count)]


def double_rule(draw, x0, x1, y, color, thick=3, thin=1, gap=3):
    """A newspaper masthead rule: one heavy line, a hairline below."""
    draw.line([(x0, y), (x1, y)], fill=color, width=thick)
    draw.line([(x0, y + thick + gap), (x1, y + thick + gap)],
              fill=color, width=thin)
