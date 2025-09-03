# src/search.py
from typing import List, Dict, Any, Set

def all_field_labels(entries: List[Dict[str, Any]]) -> List[str]:
    base = ["name", "protocol", "website", "username", "password", "notes"]
    extras: Set[str] = set()
    for e in entries:
        for k in (e.get("custom") or {}).keys():
            extras.add(k)
    return base + sorted(extras)

def matches(entry: Dict[str, Any], term: str, field: str | None) -> bool:
    t = term.lower()
    if not field or field == "Any":
        return _any_match(entry, t)
    # base
    if field in entry and isinstance(entry[field], str):
        return t in entry[field].lower()
    # custom
    if field in (entry.get("custom") or {}):
        v = entry["custom"][field]
        return t in str(v).lower()
    return False

def _any_match(e: Dict[str, Any], t: str) -> bool:
    for k in ["name","protocol","website","username","password","notes"]:
        v = e.get(k)
        if isinstance(v, str) and t in v.lower():
            return True
    for k, v in (e.get("custom") or {}).items():
        if t in str(v).lower():
            return True
    return False

def sort_entries(entries: List[Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
    if mode == "A→Z":
        return sorted(entries, key=lambda e: (e.get("name") or "").lower())
    if mode == "Recently Updated":
        return sorted(entries, key=lambda e: e.get("updated_at") or 0, reverse=True)
    if mode == "Recently Added":
        return sorted(entries, key=lambda e: e.get("created_at") or 0, reverse=True)
    if mode == "Most Used":
        return sorted(entries, key=lambda e: (e.get("access_count") or 0, e.get("last_access_at") or 0), reverse=True)
    return entries
