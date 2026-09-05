"""Check that changes to the actual manuscript cannot silently bypass verification."""

import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest

import check_examples


class ManuscriptVerificationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cs-doc-verifier-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "chapters").mkdir()
        for filename in ("01-digital-computer.tex", check_examples.ANSWERS):
            shutil.copyfile(check_examples.ROOT / "chapters" / filename,
                            self.root / "chapters" / filename)

    def replace(self, filename, old, new):
        path = self.root / "chapters" / filename
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def verify(self):
        with contextlib.redirect_stdout(io.StringIO()):
            check_examples.check_python(
                self.root, self.root, "01-digital-computer.tex",
                "手を動かす：数の表現", "第1章：数の表現",
            )

    def test_printed_example_passes(self):
        self.verify()

    def test_changed_code_fails_with_output_diff(self):
        self.replace("01-digital-computer.tex", "return x & 0xff", "return x & 0x7f")
        with self.assertRaisesRegex(ValueError, "output mismatch\n--- printed answer"):
            self.verify()

    def test_changed_answer_fails(self):
        self.replace(check_examples.ANSWERS, "127 01111111 127", "127 01111111 126")
        with self.assertRaisesRegex(ValueError, "output mismatch"):
            self.verify()

    def test_missing_listing_fails(self):
        self.replace("01-digital-computer.tex", "language=Python", "language=text")
        with self.assertRaisesRegex(ValueError, "expected 1 Python listings, found 0"):
            self.verify()

    def test_runtime_error_fails(self):
        self.replace("01-digital-computer.tex", "return x & 0xff", "return x / 0")
        with self.assertRaisesRegex(ValueError, "exited 1"):
            self.verify()

    def test_missing_expected_output_fails(self):
        self.replace(check_examples.ANSWERS, "language=bash", "language=text")
        with self.assertRaisesRegex(ValueError, "expected 1 bash listings, found 0"):
            self.verify()


if __name__ == "__main__":
    unittest.main()
