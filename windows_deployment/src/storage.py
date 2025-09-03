# src/storage.py
import json, os, time, hashlib, base64, uuid
from typing import Dict, List, Any

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vault.json")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "config.json")

class Storage:
    def __init__(self):
        self.config = self._load_config()
        self.encryption_enabled = self.config.get("encryption_enabled", False)
        self._key = None  # only used if you later enable Fernet
        self.data = self._load()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(CONFIG_PATH):
            return {"encryption_enabled": False}
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(DATA_PATH):
            return {"entries": []}
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # --- Entries API ---
    def all_entries(self) -> List[Dict[str, Any]]:
        return self.data.get("entries", [])

    def add_entry(self, base_fields: Dict[str, Any], custom_fields: Dict[str, Any]):
        now = int(time.time())
        entry = {
            "id": str(uuid.uuid4()),
            "name": base_fields.get("name","").strip(),
            "protocol": base_fields.get("protocol","").strip(),
            "website": base_fields.get("website","").strip(),
            "username": base_fields.get("username","").strip(),
            "password": base_fields.get("password",""),
            "notes": base_fields.get("notes",""),
            "custom": custom_fields or {},
            "created_at": now,
            "updated_at": now,
            "access_count": 0,
            "last_access_at": None
        }
        self.data.setdefault("entries", []).append(entry)
        self.save()

    def update_entry(self, entry_id: str, base_fields: Dict[str, Any], custom_fields: Dict[str, Any]):
        for e in self.data.get("entries", []):
            if e["id"] == entry_id:
                for k in ("name","protocol","website","username","password","notes"):
                    if k in base_fields:
                        e[k] = base_fields[k]
                e["custom"] = custom_fields or {}
                e["updated_at"] = int(time.time())
                self.save()
                return True
        return False

    def delete_entry(self, entry_id: str):
        self.data["entries"] = [e for e in self.data.get("entries", []) if e["id"] != entry_id]
        self.save()

    def record_access(self, entry_id: str):
        for e in self.data.get("entries", []):
            if e["id"] == entry_id:
                e["access_count"] = (e.get("access_count") or 0) + 1
                e["last_access_at"] = int(time.time())
                self.save()
                return
