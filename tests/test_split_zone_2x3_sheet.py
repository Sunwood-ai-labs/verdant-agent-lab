import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "split-zone-2x3-sheet.py"
SPEC = importlib.util.spec_from_file_location("split_zone", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SplitZone2x3SheetTests(unittest.TestCase):
    def test_splits_non_divisible_height_in_row_major_order(self):
        source = Image.new("RGB", (20, 19), "#ff00ff")
        draw = ImageDraw.Draw(source)
        cells = [{"id": f"asset-{index}"} for index in range(1, 7)]
        xs, ys = MODULE.proportional_boundaries(20, 2), MODULE.proportional_boundaries(19, 3)
        for index in range(6):
            column, row = index % 2, index // 2
            draw.rectangle((xs[column] + 1, ys[row] + 1, xs[column] + 2, ys[row] + 2), fill=(index + 1, 30, 40))
        with tempfile.TemporaryDirectory() as directory:
            alpha, report = MODULE.split_sheet(source, cells, Path(directory))
            self.assertEqual(alpha.size, (20, 19))
            self.assertEqual([entry["id"] for entry in report], [f"asset-{index}" for index in range(1, 7)])
            self.assertEqual(MODULE.proportional_boundaries(19, 3), [0, 6, 13, 19])
            self.assertEqual(MODULE.proportional_boundaries(20, 2), [0, 10, 20])
            self.assertTrue(all(Path(entry["output"]).exists() for entry in report))
            self.assertTrue(all(entry["opaquePixels"] == 4 for entry in report))


if __name__ == "__main__":
    unittest.main()
