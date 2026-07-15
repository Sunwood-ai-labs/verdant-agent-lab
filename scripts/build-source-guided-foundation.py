#!/usr/bin/env python3
"""Build a fixed-architecture layer by replacing only declared movable zones."""

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--empty-candidate", required=True)
    parser.add_argument("--mask", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source = cv2.imread(args.source, cv2.IMREAD_COLOR)
    candidate = cv2.imread(args.empty_candidate, cv2.IMREAD_COLOR)
    if source is None or candidate is None:
        raise SystemExit("Could not read source or candidate")
    height, width = source.shape[:2]
    candidate = cv2.resize(candidate, (width, height), interpolation=cv2.INTER_LANCZOS4)
    spec = json.loads(Path(args.mask).read_text())
    canvas = spec.get("canvas", {"width": width, "height": height})
    scale_x = width / canvas["width"]
    scale_y = height / canvas["height"]
    alpha = np.zeros((height, width), dtype=np.float32)
    for region in spec["regions"]:
        x1, y1, x2, y2 = region["bbox"]
        x1, x2 = round(x1 * scale_x), round(x2 * scale_x)
        y1, y2 = round(y1 * scale_y), round(y2 * scale_y)
        alpha[y1:y2, x1:x2] = 1.0
    alpha = cv2.GaussianBlur(alpha, (0, 0), 5.0)
    alpha = np.clip(alpha[..., None], 0.0, 1.0)
    result = source.astype(np.float32) * (1.0 - alpha) + candidate.astype(np.float32) * alpha
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.out, np.clip(result, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    main()
