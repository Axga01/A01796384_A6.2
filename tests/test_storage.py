import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from src.storage import FileStore


class TestFileStore(unittest.TestCase):

    def test_load_nonexistent_file_returns_empty(self):
        with TemporaryDirectory() as tmp:
            store = FileStore(f"{tmp}/missing.json")
            data = store.load()
            self.assertEqual(data, {})

    def test_save_and_load_json(self):
        with TemporaryDirectory() as tmp:
            file_path = f"{tmp}/data.json"
            store = FileStore(file_path)

            sample = {"A": {"value": 1}}
            store.save(sample)

            loaded = store.load()
            self.assertEqual(loaded, sample)

    def test_load_invalid_json_returns_empty(self):
        with TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "bad.json"
            file_path.write_text("{ invalid json")

            store = FileStore(str(file_path))
            data = store.load()

            self.assertEqual(data, {})