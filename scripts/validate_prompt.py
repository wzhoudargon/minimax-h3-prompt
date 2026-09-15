#!/usr/bin/env python3
"""Read-only checks for the source-verified H3 text/keyframe prompt structure."""
import argparse
import json
import math
import re
from pathlib import Path

FIELDS = ('integrated_multimodal_description', 'overall_soundscape', 'non_diegetic_music')
I2VA = ('For the target video, at 0.00 seconds into the target video, '
        '<Picture 1> (from [Shot 1]) is fully referenced.')
PREFIX = 'How the reference pictures align with the target video — '
COUNTS = {'T2VA': 0, 'I2VA': 1, 'FL2VA': 2, 'L2VA': 1}


def validate(text, mode, duration, image_count=None, max_chars=None):
    errors = []
    if mode not in COUNTS:
        return ['Unsupported mode; omni-reference syntax is not validated.']
    if not math.isfinite(duration) or duration <= 0:
        return ['Duration must be finite and positive.']
    if image_count is not None and image_count != COUNTS[mode]:
        errors.append(f'{mode} requires {COUNTS[mode]} keyframe images, got {image_count}.')
    if max_chars is not None:
        if max_chars <= 0:
            errors.append('Character limit must be positive.')
        elif len(text) > max_chars:
            errors.append(f'Prompt exceeds configured {max_chars}-character limit.')
    text = text.strip()
    matches = list(re.finditer(r'(?m)^(' + '|'.join(FIELDS) + r'):[ \t]*', text))
    if [m.group(1) for m in matches] != list(FIELDS):
        errors.append('Use each of the three fields once, in order, at line starts.')
        return errors
    values = [text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip()
              for i, m in enumerate(matches)]
    for name, value in zip(FIELDS, values):
        if not value:
            errors.append(f'{name} must have content.')
    # Only integrated description contains actual shot labels. Header references
    # and prose references to earlier shots must not determine the final shot.
    shots = [int(n) for n in re.findall(r'\[Shot (\d+)\]', values[0])]
    unique = list(dict.fromkeys(shots))
    if not unique or unique != list(range(1, max(unique, default=0)+1)):
        errors.append('Actual shot labels must begin at 1 and proceed without gaps.')
    final = max(unique, default=1)
    expected = {
        'T2VA': '',
        'I2VA': I2VA,
        'FL2VA': (PREFIX + 'Picture 1 (from Shot 1) aligns with the 0.00-second mark '
                  'of the target video; Picture 2 (from Shot ' + str(final) + ') aligns '
                  f'with the {duration:.2f}-second mark of the target video.'),
        'L2VA': (PREFIX + f'<Picture 1> (from [Shot {final}]) aligns with the '
                 f'{duration:.2f}-second mark of the target video.'),
    }[mode]
    before = text[:matches[0].start()]
    if mode == 'T2VA':
        if before:
            errors.append('T2VA must start with integrated_multimodal_description, without an instruction.')
    elif before != expected + '\n\n':
        errors.append('Expected the canonical mode instruction as the first line, followed by one blank line.')
    if mode in {'I2VA', 'L2VA'}:
        if re.search(r'\bPicture\s+(?!1\b)\d+', values[0]):
            errors.append('Single-keyframe mode references an unavailable picture number.')
    elif mode == 'T2VA' and re.search(r'\bPicture\s+\d+', values[0]):
        errors.append('T2VA unexpectedly references a keyframe picture.')
    elif mode == 'FL2VA' and re.search(r'\bPicture\s+(?!(?:1|2)\b)\d+', values[0]):
        errors.append('FL2VA references a picture other than 1 or 2.')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prompt', type=Path)
    parser.add_argument('--mode', required=True, choices=tuple(COUNTS))
    parser.add_argument('--duration', required=True, type=float)
    parser.add_argument('--image-count', type=int)
    parser.add_argument('--max-chars', type=int, help='Optional current deployment limit; no universal default.')
    args = parser.parse_args()
    try:
        text = args.prompt.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f'Cannot read prompt: {exc}\n')
    errors = validate(text, args.mode, args.duration, args.image_count, args.max_chars)
    print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'mode': args.mode,
                      'errors': errors, 'scope': 'structure_only',
                      'not_checked': ['semantic_correctness', 'dialogue_accuracy',
                                      'media_validity', 'generation_support', 'generated_audio']},
                     ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
