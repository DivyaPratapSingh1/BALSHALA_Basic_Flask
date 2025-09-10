import json, os
from pathlib import Path
from typing import Dict, Any, List

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "user_logs.json"

def load_logs() -> List[Dict[str, Any]]:
    if DATA_PATH.exists():
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_log(entry: Dict[str, Any]) -> None:
    logs = load_logs()
    logs.append(entry)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
