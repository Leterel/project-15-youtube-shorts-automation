import unittest
from build_video import validate, fit_text, text_units


class ScriptTests(unittest.TestCase):
    def test_script_bounds_and_plain_text(self):
        scene={"heading":"Test", "caption":"100% eigener Text: kein Filtercode", "narration":"Ein eigener Satz."}
        self.assertEqual(validate({"version":1,"scenes":[scene]})[0],scene)
        for data in [None, {}, {"version":1,"scenes":[]}, {"version":1,"scenes":[{**scene,"heading":"x"*71}]}, {"version":1,"scenes":[{**scene,"narration":"\x00"}]}]:
            with self.assertRaises(ValueError):
                validate(data)

    def test_long_wide_text_stays_within_width_and_height_budgets(self):
        for text, width, height, maximum, minimum in [
            ("W"*70, 630, 330, 48, 28),
            ("W"*140, 590, 260, 34, 22),
            ("界"*60, 630, 330, 48, 28),
        ]:
            layout=fit_text(text, width, height, maximum, minimum)
            for line in layout["text"].splitlines():
                self.assertLessEqual(text_units(line)*layout["fontSize"], width)
            self.assertLessEqual(layout["lines"]*(int(layout["fontSize"]*1.5+.99)+8), height)

    def test_whitespace_is_normalized_and_unfit_text_is_rejected(self):
        result=fit_text("Hallo\r\n\r\n Welt\t heute",630,330,48,28)
        self.assertEqual(" ".join(result["text"].split()),"Hallo Welt heute")
        with self.assertRaises(ValueError):
            fit_text("W"*140,10,10,34,22)
        with self.assertRaises(ValueError):
            fit_text("界"*70,630,330,48,28)


if __name__ == "__main__":
    unittest.main()
