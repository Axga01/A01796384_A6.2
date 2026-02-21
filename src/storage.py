"""JSON file persistence layer with basic error handling."""

import json
from pathlib import Path
from typing import Any, Dict


class FileStore:
    """Simple JSON file store with graceful error handling."""

    def __init__(self, filepath: str) -> None:
        """Initialize store with a file path."""
        self.path = Path(filepath)

    def load(self) -> Dict[str, Any]:
        """Load JSON data from file. Return empty dict on error."""
        if not self.path.exists():
            return {}

        try:
            raw = self.path.read_text(encoding="utf-8").strip()
            if not raw:
                return {}

            data = json.loads(raw)

            if not isinstance(data, dict):
                print(
                    f"[WARN] Invalid data structure in "
                    f"{self.path}. Using empty."
                )
                return {}

            return data

        except (OSError, json.JSONDecodeError) as exc:
            print(
                f"[WARN] Could not load {self.path}: "
                f"{exc}. Using empty."
            )
            return {}

    def save(self, data: Dict[str, Any]) -> None:
        """Save dictionary as formatted JSON."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            print(
                f"[WARN] Could not save {self.path}: "
                f"{exc}."
            )
