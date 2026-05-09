"""
MWIT #14 Dashboard refresh script.

Reads ../MWIT14_tracker.xlsx and writes data.json next to index.html.
Run this every day after you update the Excel file, then push the
updated data.json to GitHub (or re-drag the folder into Netlify Drop).

Usage:
    python3 refresh.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, date
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("Missing dependency. Install with: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

HERE = Path(__file__).resolve().parent
EXCEL_PATH = HERE.parent / "MWIT14_tracker.xlsx"
OUT_PATH = HERE / "data.json"


def to_iso(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    return str(value) if value is not None else None


def extract():
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb.active

    rows = list(ws.iter_rows(values_only=True))

    # Header row(s)
    title = rows[0][0]                       # "TICKET SALES TRACKER"
    event = "MWIT#14 - Rātrī Sritrang 2026"  # display name shown on dashboard
    as_of = to_iso(rows[1][3])               # date in column D of row 2

    # Per-room rows: start at index 3 until we hit "TOTAL" or empty
    room_data = []
    for r in rows[3:]:
        first = r[0]
        if first is None or str(first).strip().upper() == "TOTAL":
            break
        try:
            room_num = int(first)
        except (TypeError, ValueError):
            continue
        members = int(r[1] or 0)
        sold = int(r[2] or 0)
        left = int(r[3] or 0)
        room_data.append(
            {
                "room": room_num,
                "members": members,
                "sold": sold,
                "left": left,
            }
        )

    total_members = sum(r["members"] for r in room_data)
    total_sold = sum(r["sold"] for r in room_data)
    total_left = sum(r["left"] for r in room_data)

    # Find target row ("Sales Target:")
    target = 0
    for r in rows:
        if r and isinstance(r[0], str) and "sales target" in r[0].lower():
            target = int(r[2] or 0)
            break

    progress = round(total_sold / target, 4) if target else 0.0
    to_goal = max(target - total_sold, 0)

    return {
        "title": title,
        "event": event,
        "as_of": as_of,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "target": target,
        "totals": {
            "members": total_members,
            "sold": total_sold,
            "left": total_left,
            "to_goal": to_goal,
            "progress": progress,
        },
        "rooms": room_data,
    }


def main():
    if not EXCEL_PATH.exists():
        print(f"Excel file not found: {EXCEL_PATH}", file=sys.stderr)
        sys.exit(1)

    payload = extract()
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    t = payload["totals"]
    print(f"Wrote {OUT_PATH}")
    print(f"As of: {payload['as_of']}  |  generated: {payload['generated_at']}")
    print(
        f"Target {payload['target']}  |  Sold {t['sold']}  |  "
        f"To goal {t['to_goal']}  |  Progress {t['progress']:.0%}"
    )


if __name__ == "__main__":
    main()
