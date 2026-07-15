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

    def test_splits_three_columns_and_two_rows_in_row_major_order(self):
        source = Image.new("RGB", (19, 20), "#ff00ff")
        draw = ImageDraw.Draw(source)
        cells = [{"id": f"asset-{index}"} for index in range(1, 7)]
        xs, ys = MODULE.proportional_boundaries(19, 3), MODULE.proportional_boundaries(20, 2)
        for index in range(6):
            column, row = index % 3, index // 3
            draw.rectangle((xs[column] + 1, ys[row] + 1, xs[column] + 2, ys[row] + 2), fill=(index + 1, 30, 40))
        with tempfile.TemporaryDirectory() as directory:
            _, report = MODULE.split_sheet(source, cells, Path(directory), columns=3, rows=2)
            self.assertEqual([entry["id"] for entry in report], [f"asset-{index}" for index in range(1, 7)])
            self.assertTrue(all(entry["opaquePixels"] == 4 for entry in report))

    def test_uses_row_specific_vertical_gutters(self):
        source = Image.new("RGB", (30, 20), "#ff00ff")
        draw = ImageDraw.Draw(source)
        cells = [{"id": f"asset-{index}"} for index in range(1, 7)]
        # Top row's second/third boundary is at x=22; bottom row's is x=18.
        for rectangle, colour in [((1, 1, 7, 8), (1, 1, 1)), ((10, 1, 18, 8), (2, 2, 2)), ((24, 1, 28, 8), (3, 3, 3)), ((1, 12, 5, 18), (4, 4, 4)), ((8, 12, 14, 18), (5, 5, 5)), ((20, 12, 28, 18), (6, 6, 6))]:
            draw.rectangle(rectangle, fill=colour)
        with tempfile.TemporaryDirectory() as directory:
            _, report = MODULE.split_sheet(source, cells, Path(directory), columns=3, rows=2)
            self.assertTrue(all(not any(entry["edgeFlags"].values()) for entry in report))

    def test_preserves_existing_soft_alpha_for_gutter_detection(self):
        source = Image.new("RGBA", (30, 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(source)
        cells = [{"id": f"asset-{index}"} for index in range(1, 7)]
        for rectangle in [
            (1, 1, 7, 8), (10, 1, 18, 8), (24, 1, 28, 8),
            (1, 12, 5, 18), (8, 12, 14, 18), (20, 12, 28, 18),
        ]:
            draw.rectangle(rectangle, fill=(0, 0, 0, 220))
        source.putpixel((1, 1), (16, 16, 16, 64))
        with tempfile.TemporaryDirectory() as directory:
            alpha, report = MODULE.split_sheet(source, cells, Path(directory), columns=3, rows=2)
            self.assertEqual(alpha.getpixel((1, 1)), (16, 16, 16, 64))
            self.assertTrue(all(not any(entry["edgeFlags"].values()) for entry in report))


if __name__ == "__main__":
    unittest.main()
