#!/usr/bin/env python3

import sys
import os
import shutil

FORCED_ZOOM_FIELD = b"\xdc\x09\x00\x04"
SCREEN_WIDTH_FIELD = b"\x7e\xa6\x0c\x00\x04"
MAX_VIEW_SIZE_FIELD = b"\x7e\xb7\x0a\x00\x04"

def die(msg):
    print(f"[!] {msg}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        die("Usage: python patcher.py /path/to/Terraria.exe")

    exe_path = sys.argv[1]
    backup_path = f"{exe_path}.bak"

    if not os.path.exists(exe_path):
        die(f"File not found: {exe_path}")

    print("--- Terraria Zoom Patcher ---")

    # backup
    if not os.path.exists(backup_path):
        print(f"[*] Creating backup: {backup_path}")
        shutil.copy2(exe_path, backup_path)
    else:
        print(f"[*] Backup exists: {backup_path}")

    with open(exe_path, "rb") as f:
        data = bytearray(f.read())

    # find stsfld ForcedMinimumZoom
    stsfld = data.find(b"\x80" + FORCED_ZOOM_FIELD)
    if stsfld == -1:
        die("ForcedMinimumZoom field not found - wrong terraria version?")

    print(f"[+] Found ForcedMinimumZoom store at {hex(stsfld)}")

    # find calculation start (ldsfld screenWidth, conv.r4, ldsfld MaxWorldViewSize)
    calc_start = None
    for i in range(stsfld - 70, stsfld - 30):
        if data[i:i+5] == SCREEN_WIDTH_FIELD and data[i+5] == 0x6b:  # conv.r4
            if data[i+6:i+11] == MAX_VIEW_SIZE_FIELD:
                calc_start = i
                break

    if not calc_start:
        die("Could not find calculation start - wrong terraria version?")

    calc_end = stsfld + 5
    calc_len = calc_end - calc_start
    print(f"[+] Patching {calc_len} bytes at {hex(calc_start)}")

    # replace with: ldc.r4 1.0f; stsfld ForcedMinimumZoom; nop*
    patch = b"\x22\x00\x00\x80\x3f"  # ldc.r4 1.0f
    patch += b"\x80" + FORCED_ZOOM_FIELD  # stsfld
    patch += b"\x00" * (calc_len - len(patch))  # nops

    data[calc_start:calc_end] = patch

    with open(exe_path, "wb") as f:
        f.write(data)

    print("[+] Done! Zoom limit removed.")

if __name__ == "__main__":
    main()
