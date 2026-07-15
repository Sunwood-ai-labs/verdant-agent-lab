#!/usr/bin/env python3
"""Score a same-view office reconstruction against the private original."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

TARGET_SIZE = (1280, 960)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_image(path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"Could not read image: {path}")
    return cv2.resize(image, TARGET_SIZE, interpolation=cv2.INTER_AREA)


def mask_from_file(path):
    data = json.loads(Path(path).read_text())
    mask = np.full((TARGET_SIZE[1], TARGET_SIZE[0]), 255, dtype=np.uint8)
    for region in data["regions"]:
        x1, y1, x2, y2 = region["bbox"]
        mask[y1:y2, x1:x2] = 0
    return data, mask


def ssim_map(a, b):
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mu_a = cv2.GaussianBlur(a, (11, 11), 1.5)
    mu_b = cv2.GaussianBlur(b, (11, 11), 1.5)
    sigma_a = cv2.GaussianBlur(a * a, (11, 11), 1.5) - mu_a * mu_a
    sigma_b = cv2.GaussianBlur(b * b, (11, 11), 1.5) - mu_b * mu_b
    sigma_ab = cv2.GaussianBlur(a * b, (11, 11), 1.5) - mu_a * mu_b
    return ((2 * mu_a * mu_b + c1) * (2 * sigma_ab + c2)) / ((mu_a * mu_a + mu_b * mu_b + c1) * (sigma_a + sigma_b + c2))


def masked_mean(values, mask):
    valid = mask > 0
    return float(np.mean(values[valid])) if np.any(valid) else 0.0


def edge_f1(a_gray, b_gray, mask):
    a = cv2.Canny(a_gray, 70, 140)
    b = cv2.Canny(b_gray, 70, 140)
    kernel = np.ones((3, 3), np.uint8)
    a_dilated = cv2.dilate(a, kernel)
    b_dilated = cv2.dilate(b, kernel)
    valid = mask > 0
    a_edges = (a > 0) & valid
    b_edges = (b > 0) & valid
    precision = float(np.sum(b_edges & (a_dilated > 0)) / max(1, np.sum(b_edges)))
    recall = float(np.sum(a_edges & (b_dilated > 0)) / max(1, np.sum(a_edges)))
    return 2 * precision * recall / max(1e-9, precision + recall)


def lab_histogram_similarity(a, b, mask):
    a_lab = cv2.cvtColor(a, cv2.COLOR_BGR2LAB)
    b_lab = cv2.cvtColor(b, cv2.COLOR_BGR2LAB)
    scores = []
    for channel in range(3):
        hist_a = cv2.calcHist([a_lab], [channel], mask, [64], [0, 256])
        hist_b = cv2.calcHist([b_lab], [channel], mask, [64], [0, 256])
        cv2.normalize(hist_a, hist_a)
        cv2.normalize(hist_b, hist_b)
        scores.append(max(0.0, cv2.compareHist(hist_a, hist_b, cv2.HISTCMP_CORREL)))
    return float(np.mean(scores))


def region_mask(base_mask, bbox):
    mask = np.zeros_like(base_mask)
    x1, y1, x2, y2 = bbox
    mask[y1:y2, x1:x2] = base_mask[y1:y2, x1:x2]
    return mask


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--mask", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--diff", required=True)
    parser.add_argument("--label", default="modular-reconstruction")
    args = parser.parse_args()

    target = load_image(args.target)
    candidate = load_image(args.candidate)
    mask_data, mask = mask_from_file(args.mask)
    ledger = json.loads(Path(args.ledger).read_text())
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    candidate_gray = cv2.cvtColor(candidate, cv2.COLOR_BGR2GRAY)
    similarity = ssim_map(target_gray, candidate_gray)
    raw_ssim = float(np.mean(similarity))
    masked_ssim = masked_mean(similarity, mask)
    edges = edge_f1(target_gray, candidate_gray, mask)
    histogram = lab_histogram_similarity(target, candidate, mask)
    # These blended values are diagnostics only.  They may help locate a
    # silhouette or palette issue, but must never substitute for a requested
    # direct screenshot-similarity target.
    pixel_composite = 0.70 * masked_ssim + 0.20 * edges + 0.10 * histogram
    layout_content = 0.35 * masked_ssim + 0.40 * edges + 0.25 * histogram
    ledger_verified = ledger.get("status") == "complete" and all(
        instance.get("status") == "verified" for instance in ledger["instances"]
    )
    direct_masked_ssim_pass = masked_ssim >= 0.60
    objective_pass = direct_masked_ssim_pass and ledger_verified

    zones = []
    for instance in ledger["instances"]:
        zone_mask = region_mask(mask, instance["bbox"])
        zones.append({
            "id": instance["id"],
            "semantic": instance["semantic"],
            "orientation": instance["orientation"],
            "ledgerStatus": instance["status"],
            "ssimPercent": round(masked_mean(similarity, zone_mask) * 100, 2),
        })

    report = {
        "schemaVersion": 2,
        "method": "office-similarity-v2-direct-ssim",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "label": args.label,
        "normalization": {"width": 1280, "height": 960, "sameViewRequired": True, "referenceOverlayForbidden": True},
        "diagnosticWeights": {
            "pixelComposite": {"maskedGrayscaleSsim": 0.70, "edgeF1": 0.20, "labHistogram": 0.10},
            "layoutContentSimilarity": {"maskedGrayscaleSsim": 0.35, "edgeF1": 0.40, "labHistogram": 0.25},
        },
        "thresholds": {"authoritativeDirectMaskedSsimPercent": 60},
        "scores": {
            "rawSsimPercent": round(raw_ssim * 100, 2),
            "maskedSsimPercent": round(masked_ssim * 100, 2),
            "edgeF1Percent": round(edges * 100, 2),
            "labHistogramPercent": round(histogram * 100, 2),
            "pixelCompositePercent": round(pixel_composite * 100, 2),
            "layoutContentSimilarityPercent": round(layout_content * 100, 2),
        },
        "ledgerVerified": ledger_verified,
        "directMaskedSsimPass": direct_masked_ssim_pass,
        "diagnosticOnly": ["edgeF1Percent", "labHistogramPercent", "pixelCompositePercent", "layoutContentSimilarityPercent"],
        "pass": objective_pass,
        "inputs": {
            "target": {"name": Path(args.target).name, "sha256": sha256(args.target)},
            "candidate": {"name": Path(args.candidate).name, "sha256": sha256(args.candidate)},
            "mask": {"name": Path(args.mask).name, "version": mask_data["version"], "sha256": sha256(args.mask)},
            "ledger": {"name": Path(args.ledger).name, "version": ledger["version"], "sha256": sha256(args.ledger)},
        },
        "zones": zones,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    heat = np.clip((1.0 - similarity) * 255, 0, 255).astype(np.uint8)
    heat[mask == 0] = 0
    heat = cv2.applyColorMap(heat, cv2.COLORMAP_INFERNO)
    cv2.imwrite(args.diff, heat)
    print(json.dumps(report["scores"], ensure_ascii=False))
    print("PASS" if report["pass"] else "FAIL")


if __name__ == "__main__":
    main()
