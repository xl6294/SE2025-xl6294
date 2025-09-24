#!/usr/bin/env python3
"""
Print the first Arduino-like serial port to stdout.
Exits non-zero if nothing is found.
Requires: pyserial
"""
import sys
import serial.tools.list_ports

def main():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        desc = (p.description or "").lower()
        dev  = (p.device or "")
        if ("arduino" in desc or "usbmodem" in dev or "usbserial" in dev or
            "wch" in desc or "ch340" in desc):
            print(dev)
            return 0
    if len(ports) == 1:
        print(ports[0].device)
        return 0
    sys.stderr.write("[find_arduino_port] No Arduino-like serial port found.\n")
    for p in ports:
        sys.stderr.write(f"  - {p.device}  {p.description}\n")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())