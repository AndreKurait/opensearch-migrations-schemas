import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_manifest import validate


class JsonValidationTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.manifest = {
            "latest": "1.0",
            "versions": {"1.0": {"schema": "schema.json"}},
        }
        (self.root / "versions.json").write_text(json.dumps(self.manifest))
        (self.root / "schema.json").write_text('{"type": "object"}')

    def test_valid_artifact(self):
        self.assertEqual(validate(self.root), (1, 1))

    def test_nonstandard_numbers_in_artifact_are_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                (self.root / "schema.json").write_text('{"default": ' + value + '}')
                with self.assertRaisesRegex(ValueError, "Non-standard JSON number"):
                    validate(self.root)

    def test_nonstandard_numbers_in_manifest_are_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                content = json.dumps(self.manifest)[:-1] + ', "invalid": ' + value + '}'
                (self.root / "versions.json").write_text(content)
                with self.assertRaisesRegex(ValueError, "Non-standard JSON number"):
                    validate(self.root)


if __name__ == "__main__":
    unittest.main()
