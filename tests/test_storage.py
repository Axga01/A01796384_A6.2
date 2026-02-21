"""Unit tests for the FileStore JSON persistence layer."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.storage import FileStore


class TestFileStore(unittest.TestCase):
    """Tests for loading and saving JSON data with FileStore."""

    def test_load_nonexistent_file_returns_empty(self):
        """load() returns an empty dict when the file does not exist."""
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/missing.json")
            data = store.load()
            self.assertEqual(data, {})

    def test_save_and_load_json(self):
        """save() persists data and load() returns the same dict."""
        with TemporaryDirectory() as tmp:
            file_path = f"{tmp}/data.json"
            store = FileStore(file_path)

            sample = {"A": {"value": 1}}
            store.save(sample)

            loaded = store.load()
            self.assertEqual(loaded, sample)

    def test_load_invalid_json_returns_empty(self):
        """load() returns an empty dict when the JSON is invalid."""
        with TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "bad.json"
            file_path.write_text("{ invalid json", encoding="utf-8")

            store = FileStore(str(file_path))
            data = store.load()

            self.assertEqual(data, {})


if __name__ == "__main__":
    unittest.main()
