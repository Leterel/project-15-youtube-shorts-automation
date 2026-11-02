import unittest
from build_video import validate


class ScriptTests(unittest.TestCase):
    def test_script_bounds_and_plain_text(self):
        scene={"heading":"Test", "caption":"100% eigener Text: kein Filtercode", "narration":"Ein eigener Satz."}
        self.assertEqual(validate({"version":1,"scenes":[scene]})[0],scene)
        for data in [None, {}, {"version":1,"scenes":[]}, {"version":1,"scenes":[{**scene,"heading":"x"*71}]}, {"version":1,"scenes":[{**scene,"narration":"\x00"}]}]:
            with self.assertRaises(ValueError):
                validate(data)


if __name__ == "__main__":
    unittest.main()
