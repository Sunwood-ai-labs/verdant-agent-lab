#!/usr/bin/env python3
"""Build the literal Pixel Agents default-office solarpunk reskin layout.

The furniture placement records and tile grid remain byte-for-byte identical
to the audited upstream default-layout-1.  The visual replacement happens only
through exact-ID assets in ``pixel-agents-pack/assets/furniture``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "research/pixel-agents/sources/pixel-agents/webview-ui/public/assets/default-layout-1.json"
)
OUTPUT = ROOT / "pixel-agents-pack/solarpunk-default-layout.json"
REQUIRED = ROOT / "pixel-agents-pack/default-layout-required-types.json"
CATALOG = ROOT / "pixel-agents-pack/catalog.json"
AUDIT = ROOT / "proofs/pixel-agents-default-reskin/layout-audit.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    layout = json.loads(source_bytes)
    required = set(json.loads(REQUIRED.read_text()))
    catalog = json.loads(CATALOG.read_text())
    used = {item["type"] for item in layout["furniture"]}

    checks = {
        "versionIs1": layout.get("version") == 1,
        "gridIs21x22": (layout.get("cols"), layout.get("rows")) == (21, 22),
        "tileCountIs462": len(layout.get("tiles", [])) == 21 * 22,
        "furnitureCountIs36": len(layout.get("furniture", [])) == 36,
        "requiredTypesMatchExactly": used == required,
        "allUsedTypesResolveInCatalog": used <= set(catalog),
        "allPlacementsUseIntegerGrid": all(
            isinstance(item.get("col"), int) and isinstance(item.get("row"), int)
            for item in layout["furniture"]
        ),
        "noCharactersOrPetsEmbedded": not layout.get("characters") and not layout.get("pets"),
    }
    if not all(checks.values()):
        raise SystemExit(f"default-reskin audit failed: {checks}")

    OUTPUT.write_bytes(source_bytes)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    audit = {
        "status": "passed",
        "source": str(SOURCE.relative_to(ROOT)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "sourceSha256": sha256(source_bytes),
        "outputSha256": sha256(OUTPUT.read_bytes()),
        "byteIdenticalToAuditedDefaultLayout": OUTPUT.read_bytes() == source_bytes,
        "grid": {"cols": layout["cols"], "rows": layout["rows"], "tileSizePx": 16},
        "furniturePlacements": len(layout["furniture"]),
        "uniqueFurnitureTypes": len(used),
        "resolvedFurnitureTypes": len(used & set(catalog)),
        "checks": checks,
    }
    AUDIT.write_text(json.dumps(audit, indent=2) + "\n")
    print(
        "PASS: upstream default layout preserved byte-for-byte; "
        f"{len(layout['furniture'])} placements / {len(used)} types / 21x22 grid"
    )


if __name__ == "__main__":
    main()
