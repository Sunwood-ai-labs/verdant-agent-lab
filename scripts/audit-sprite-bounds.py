#!/usr/bin/env python3
"""Flag runtime PNGs whose non-transparent pixels touch the source canvas edge."""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent.parent
MANIFESTS = [
    ROOT / "assets/manifests/furniture.v1.json",
    ROOT / "assets/manifests/technology.v1.json",
    ROOT / "assets/manifests/props.v1.json",
]


def touches_edge(alpha):
    width, height = alpha.size
    pixels = alpha.load()
    edges = {
        "top": any(pixels[x, 0] > 0 for x in range(width)),
        "right": any(pixels[width - 1, y] > 0 for y in range(height)),
        "bottom": any(pixels[x, height - 1] > 0 for x in range(width)),
        "left": any(pixels[0, y] > 0 for y in range(height)),
    }
    return edges, [edge for edge, hit in edges.items() if hit]


def main():
    results = []
    for manifest_path in MANIFESTS:
        manifest = json.loads(manifest_path.read_text())
        for item in manifest["items"]:
            sprite = ROOT / "assets" / item["sprite"].replace("../", "")
            alpha = Image.open(sprite).convert("RGBA").getchannel("A")
            edges, hit_edges = touches_edge(alpha)
            results.append({
                "id": item["id"],
                "sprite": item["sprite"],
                "size": list(alpha.size),
                "alphaBBox": list(alpha.getbbox() or (0, 0, 0, 0)),
                "touchesCanvasEdge": bool(hit_edges),
                "edges": edges,
                "hitEdges": hit_edges,
            })
    report = {
        "schemaVersion": 1,
        "policy": "An edge touch is a visible-crop risk, not a pass. It requires source inspection before an asset can be called cleanly isolated.",
        "runtimeAssetCount": len(results),
        "edgeTouchCount": sum(item["touchesCanvasEdge"] for item in results),
        "assets": results,
    }
    output = ROOT / "proof/runtime-asset-bounds-v1.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"runtimeAssetCount": report["runtimeAssetCount"], "edgeTouchCount": report["edgeTouchCount"]}))


if __name__ == "__main__":
    main()
