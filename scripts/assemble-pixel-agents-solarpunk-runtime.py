#!/usr/bin/env python3
"""Assemble a separate Pixel Agents runtime with the Verdant preset overlaid.

The reference checkout is read-only. The generated runtime and deterministic
zip are written under this repository's ignored ``build/`` directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = Path("/Users/admin/Prj/pixel-agents")
DEFAULT_OUTPUT = ROOT / "build" / "pixel-agents-solarpunk-default-runtime"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pixel-agents", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_exact_dir(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def deterministic_zip(source: Path, archive: Path) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            relative = path.relative_to(source.parent)
            info = zipfile.ZipInfo(str(relative), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = path.stat().st_mode
            info.external_attr = (stat.S_IMODE(mode) & 0xFFFF) << 16
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> None:
    args = parse_args()
    reference = args.pixel_agents.resolve()
    dist = reference / "dist"
    output = args.output.resolve()
    build_root = (ROOT / "build").resolve()
    if build_root not in output.parents:
        raise SystemExit(f"output must stay under {build_root}")
    if not (dist / "cli.js").is_file():
        raise SystemExit(f"Pixel Agents dist is missing: {dist}")

    subprocess.run(
        ["python3", str(ROOT / "scripts/build-pixel-agents-solarpunk-default-preset.py")],
        check=True,
        cwd=ROOT,
    )
    staging = output.with_name(output.name + ".staging")
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(dist, staging)
    # The repository root is ESM, while Pixel Agents' bundled CLI is CommonJS.
    # Give the assembled runtime an explicit module boundary so it can launch
    # from build/ without inheriting the parent package.json.
    (staging / "package.json").write_text(
        json.dumps({"private": True, "type": "commonjs"}, indent=2) + "\n"
    )

    assets = staging / "assets"
    copy_exact_dir(ROOT / "pixel-agents-pack/assets/furniture", assets / "furniture")
    copy_exact_dir(ROOT / "pixel-agents-theme-v2/assets/floors", assets / "floors")
    copy_exact_dir(ROOT / "pixel-agents-theme-v2/assets/walls", assets / "walls")
    layout = ROOT / "pixel-agents-solarpunk-default/layout.json"
    shutil.copy2(layout, assets / "default-layout-1.json")
    shutil.copy2(layout, assets / "default-layout-2.json")

    license_dir = staging / "THIRD_PARTY_LICENSES"
    license_dir.mkdir(exist_ok=True)
    shutil.copy2(reference / "LICENSE", license_dir / "pixel-agents-MIT.txt")

    source_commit = subprocess.check_output(
        ["git", "-C", str(reference), "rev-parse", "HEAD"], text=True
    ).strip()
    receipt = {
        "name": "Verdant Solarpunk Default Office runtime overlay",
        "pixelAgentsReference": str(reference),
        "pixelAgentsCommit": source_commit,
        "referenceCheckoutModified": False,
        "layout": {"grid": "21x22", "placements": 36, "path": "assets/default-layout-1.json"},
        "assets": {"furnitureManifests": 53, "physicalFurnitureSprites": 64, "floors": 9, "wallAtlases": 1},
        "launch": f"NODE_PATH={reference / 'node_modules'} node {output / 'cli.js'} --port 3101",
    }
    (staging / "VERDANT_PRESET.json").write_text(json.dumps(receipt, indent=2) + "\n")
    (staging / "README-VERDANT.md").write_text(
        "# Verdant Solarpunk Default Office runtime\n\n"
        "This is an assembled development overlay. The original Pixel Agents checkout was not modified.\n\n"
        "Launch from an unrelated working directory so project agents are not shown:\n\n"
        f"```bash\ncd /tmp\nNODE_PATH={reference / 'node_modules'} node {output / 'cli.js'} --port 3101\n```\n"
    )

    if output.exists():
        shutil.rmtree(output)
    staging.rename(output)
    archive = output.with_suffix(".zip")
    if archive.exists():
        archive.unlink()
    deterministic_zip(output, archive)

    checks = {
        "layout1MatchesPreset": sha256(output / "assets/default-layout-1.json") == sha256(layout),
        "layout2MatchesPreset": sha256(output / "assets/default-layout-2.json") == sha256(layout),
        "floorCountIs9": len(list((output / "assets/floors").glob("floor_*.png"))) == 9,
        "wallAtlasCountIs1": len(list((output / "assets/walls").glob("wall_*.png"))) == 1,
        "referenceStillExists": (reference / ".git").is_dir(),
        "archiveCreated": archive.is_file(),
    }
    if not all(checks.values()):
        raise SystemExit(f"assembled runtime validation failed: {checks}")
    print(json.dumps({
        "status": "passed",
        "output": str(output),
        "archive": str(archive),
        "archiveSha256": sha256(archive),
        "pixelAgentsCommit": source_commit,
        "checks": checks,
    }, indent=2))


if __name__ == "__main__":
    main()
