# ruff: noqa: D101, D102

import json
import tempfile
import unittest
from pathlib import Path

from modules.util import stixhelpers


class StixTranslationOverlayTests(unittest.TestCase):
    def test_overlays_by_id_without_replacing_english_fields(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.json"
            translations_path = root / "translations.json"
            source_path.write_text(
                json.dumps(
                    {
                        "type": "bundle",
                        "objects": [
                            {"id": "attack-pattern--one", "name": "English", "description": "English body"},
                            {"id": "attack-pattern--two", "name": "Fallback"},
                        ],
                    }
                ),
                encoding="utf8",
            )
            translations_path.write_text(
                json.dumps(
                    {
                        "type": "bundle",
                        "objects": [
                            {
                                "id": "attack-pattern--one",
                                "name": "Do not use",
                                "description": "Do not use",
                                "name_fa": "فارسی",
                                "description_fa": "توضیح فارسی",
                            },
                            {"id": "attack-pattern--missing", "name_fa": "نادیده"},
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf8",
            )

            count = stixhelpers.overlay_stix_translations(source_path, str(translations_path))
            result = json.loads(source_path.read_text(encoding="utf8"))["objects"]

            self.assertEqual(count, 1)
            self.assertEqual(result[0]["name"], "English")
            self.assertEqual(result[0]["description"], "English body")
            self.assertEqual(result[0]["name_fa"], "فارسی")
            self.assertEqual(result[0]["description_fa"], "توضیح فارسی")
            self.assertNotIn("name_fa", result[1])

    def test_loads_single_object_bundles_recursively(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            nested = root / "attack-pattern"
            nested.mkdir()
            (nested / "one.json").write_text(
                json.dumps({"objects": [{"id": "attack-pattern--one", "name_fa": "یک"}]}, ensure_ascii=False),
                encoding="utf8",
            )

            result = stixhelpers.load_stix_translations(str(root))

            self.assertEqual(result, [{"id": "attack-pattern--one", "name_fa": "یک"}])

    def test_javascript_literal_escapes_line_separators(self):
        literal = stixhelpers.to_javascript_object_literal({"fa": {"quote\"slash\\line\n": "الف\u2028ب"}})

        self.assertIn('quote\\"slash\\\\line\\n', literal)
        self.assertIn("الف\\u2028ب", literal)
        self.assertNotIn("\u2028", literal)


if __name__ == "__main__":
    unittest.main()
