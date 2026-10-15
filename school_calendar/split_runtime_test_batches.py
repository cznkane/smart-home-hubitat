"""Split the approved device-free TEST matrix into transport-sized candidates.

This tool does not upload, execute, or change any piston. It preserves every
original assertion and local variable declaration, and emits a manifest for
fresh WebCoRE preparation. The 99-chunk limit must still be verified by the
live connector; JSON byte count alone cannot certify URL chunk count.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "cutover" / "2026-10-14"
SOURCE = ROOT / "candidates"
DEST = ROOT / "resized_test_candidates"


def partition(statements):
    """One independently testable calendar or freshness case per body."""
    pos = 0
    while pos < len(statements):
        if statements[pos].get("t") != "action":
            raise ValueError(f"Unexpected TEST section at index {pos}")
        if pos + 1 < len(statements) and statements[pos + 1].get("t") == "if":
            count = 2
        elif (pos + 2 < len(statements)
              and statements[pos + 1].get("t") == "action"
              and statements[pos + 2].get("t") == "if"):
            count = 3
        else:
            raise ValueError(f"Unexpected TEST case structure at index {pos}")
        yield statements[pos:pos + count]
        pos += count


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    entries = []
    total_calendar = total_freshness = 0
    for batch in range(1, 8):
        original = json.loads((SOURCE / f"TEST_{batch}.json").read_text())
        groups = list(partition(original["s"]))
        for number, group in enumerate(groups, 1):
            body = copy.deepcopy(original)
            body["s"] = copy.deepcopy(group)
            kind = "freshness" if len(group) == 3 else "calendar"
            total_calendar += kind == "calendar"
            total_freshness += kind == "freshness"
            name = f"TEST_{batch}_{number:02d}.json"
            encoded = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
            (DEST / name).write_text(encoded + "\n")
            entries.append({
                "file": name, "source": f"TEST_{batch}.json",
                "source_case": number, "kind": kind,
                "logic_sections": len(group), "json_bytes": len(encoded.encode()),
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
                "prepared": False, "transport_verified": False,
                "runtime_verified": False,
            })
    if (total_calendar, total_freshness) != (64, 16):
        raise ValueError(f"Coverage changed: {total_calendar} calendar, {total_freshness} freshness")
    manifest = {"source_commit": "b2aef538834eb7ffe0c7a2a7fcda73e89e7b3f5a",
                "approval_status": "NEW_APPROVAL_REQUIRED",
                "calendar_cases": total_calendar,
                "freshness_cases": total_freshness, "entries": entries}
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = build()
    print(f"Generated {len(result['entries'])} one-case TEST bodies; "
          "fresh preparation, upload-size verification and approval required.")
