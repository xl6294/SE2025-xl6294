#!/usr/bin/env python3
"""
Serial logger for Arduino CSV output.

Features:
- Auto-detects Arduino serial port (pyserial)
- Saves to ~/Downloads/arduino_logs
- Rotates files at configurable intervals (ROTATE_EVERY in seconds)
- Baud rate provided via --baud (from VS Code task dropdown)
- NEW: Reads CSV header from the .ino file name via --sketch-name
       Convention: <anything>__csv_col1+col2+col3.ino
"""

import os, sys, csv, time, argparse
from datetime import datetime
import serial, serial.tools.list_ports

# -------------------- USER SETTINGS --------------------

LOG_DIR = os.path.expanduser("~/Downloads/arduino_logs")

# Python will write a header to each NEW file using:
#   [iso_time] + CSV_HEADER (either parsed from sketch name or DEFAULT_HEADER)
ADD_PC_TIMESTAMP = True
WRITE_HEADER_EACH_FILE = True
DEFAULT_HEADER = ["t_s", "temperature_C", "humidity_pct"]  # fallback if not encoded in filename

# Rotate every N seconds. 
# Examples: 
    # 60 (1 min), 
    # 600 (10 min), 
    # 3600 (1 hr), 
    # 7200 (2 hr), 
    # 86400 (1 day)
ROTATE_EVERY = 30  # <--- change here for new-file frequency

# Optional throttle: write at most once every N seconds (0 = write every received line)
THROTTLE_SECONDS = 0

# ---------------- END SETTINGS -------------------------

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def file_path(now: datetime) -> str:
    """Return file path based on interval bucket start time."""
    ensure_dir(LOG_DIR)
    epoch = int(now.timestamp())
    bucket = epoch // ROTATE_EVERY * ROTATE_EVERY
    dt_bucket = datetime.fromtimestamp(bucket)
    return os.path.join(LOG_DIR, dt_bucket.strftime("%Y-%m-%d_%H-%M.csv"))

def parse_header_from_sketch_name(sketch_name: str):
    """
    Extract header columns from a sketch file name using the convention:
      <anything>__csv_col1+col2+col3.ino
    Returns a list of column names or None if not found.
    """
    if not sketch_name:
        return None
    name = sketch_name
    # strip extension if present
    if name.lower().endswith(".ino"):
        name = name[:-4]
    marker = "__csv_"
    idx = name.find(marker)
    if idx == -1:
        return None
    encoded = name[idx + len(marker):]  # part after __csv_
    if not encoded:
        return None
    # split on '+'; replace spaces around items
    cols = [part.strip() for part in encoded.split("+") if part.strip()]
    return cols if cols else None

def open_log_file(now: datetime, csv_header):
    path = file_path(now)
    new_file = not os.path.exists(path) or os.path.getsize(path) == 0
    f = open(path, "a", newline="")
    w = csv.writer(f)
    if new_file and WRITE_HEADER_EACH_FILE:
        hdr = (["iso_time"] if ADD_PC_TIMESTAMP else []) + csv_header
        w.writerow(hdr)
    return f, w, path

def auto_detect_port() -> str:
    ports = list(serial.tools.list_ports.comports())
    candidates = []
    for p in ports:
        desc = (p.description or "").lower()
        dev  = (p.device or "")
        if ("arduino" in desc or "usbmodem" in dev or "usbserial" in dev or
            "wch" in desc or "ch340" in desc):
            candidates.append(p.device)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        print(f"[logger] multiple candidates found, picking {candidates[0]}. others: {', '.join(candidates[1:])}")
        return candidates[0]
    if not ports:
        sys.exit("[error] no serial ports found. plug in Arduino and try again.")
    sys.exit("[error] could not auto-detect Arduino. run with explicit port")

def parse_args():
    ap = argparse.ArgumentParser(description="Arduino Serial Logger")
    ap.add_argument("port", nargs="?", help="Serial port (auto-detect if omitted)")
    ap.add_argument("--baud", type=int, default=115200,
                    help="Baud rate (e.g., 9600, 115200). Default 115200.")
    ap.add_argument("--sketch-name", default="",
                    help="Active .ino file name so logger can parse CSV header from it.")
    return ap.parse_args()

def main():
    args = parse_args()
    port = args.port if args.port else auto_detect_port()
    baud = args.baud

    # Determine CSV header to use
    parsed_header = parse_header_from_sketch_name(args.sketch_name)
    csv_header = parsed_header if parsed_header else DEFAULT_HEADER
    if parsed_header:
        print(f"[logger] header from sketch name: {csv_header}")
    else:
        print(f"[logger] using DEFAULT header: {csv_header} (no __csv_... in sketch name)")

    print(f"[logger] connecting to {port} @ {baud}")
    ser = serial.Serial(port, baud, timeout=1)
    ser.readline()  # discard partial first line

    current_file = None
    current_path = None
    writer = None
    last_write_ts = 0.0

    try:
        while True:
            raw = ser.readline().decode(errors="ignore").strip()
            if not raw:
                continue

            now = datetime.now()
            new_path = file_path(now)

            if new_path != current_path or writer is None:
                if current_file: current_file.close()
                current_file, writer, current_path = open_log_file(now, csv_header)
                print(f"[logger] writing to {current_path}")

            if THROTTLE_SECONDS > 0:
                t = time.time()
                if (t - last_write_ts) < THROTTLE_SECONDS:
                    continue
                last_write_ts = t

            fields = [s.strip() for s in raw.split(",")]
            if ADD_PC_TIMESTAMP:
                writer.writerow([now.isoformat()] + fields)
            else:
                writer.writerow(fields)
            current_file.flush()

    except KeyboardInterrupt:
        print("\n[logger] stopping (Ctrl+C)")
    finally:
        if current_file: current_file.close()
        ser.close()

if __name__ == "__main__":
    main()