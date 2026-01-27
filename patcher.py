#!/usr/bin/env python3
"""
Terraria Zoom Patcher - allows zooming out on ultrawide/high-res monitors.

Instead of forcing ForcedMinimumZoom=1.0 (which breaks tile culling at zoom>1.0),
this patches the GameZoomTarget clamp minimum from 1.0 to 0.5, allowing you to
set the zoom slider lower to achieve true 1.0x zoom on ultrawide screens.

On a 3440x1440 ultrawide, ForcedMinimumZoom is ~1.79. Setting GameZoomTarget to
~0.56 gives you actual zoom of 1.79 * 0.56 = 1.0, showing more of the world.
"""

import sys
import os
import shutil
import re

# Pattern: ldc.r4 1.0f, ldc.r4 2.0f (the clamp bounds)
# 22 = ldc.r4 opcode, 00 00 80 3f = 1.0f, 00 00 00 40 = 2.0f
CLAMP_PATTERN = rb"\x22\x00\x00\x80\x3f\x22\x00\x00\x00\x40"

# 1.0f = 00 00 80 3f, 0.5f = 00 00 00 3f (change 0x80 to 0x00 at offset +3)
OLD_FLOAT = 0x80
NEW_FLOAT = 0x00
FLOAT_OFFSET = 3  # offset within the ldc.r4 instruction to the byte we change


def die(msg):
    print(f"[!] {msg}")
    sys.exit(1)


def find_zoom_clamps(data):
    """Find clamp(1.0, 2.0) patterns that are related to GameZoomTarget."""
    candidates = []

    for m in re.finditer(CLAMP_PATTERN, data):
        pos = m.start()
        # Check context after: should be call + stsfld (for keyboard zoom)
        # or call + mul + newobj (for GameViewMatrix.Zoom)
        after = data[pos+10:pos+20]

        # call opcode is 0x28
        if len(after) >= 5 and after[0] == 0x28:
            # After the call, check for stsfld (0x80) or mul (0x5a)
            call_end = 5
            next_op = after[call_end] if len(after) > call_end else 0

            if next_op == 0x80:  # stsfld - this is keyboard zoom
                candidates.append(("keyboard_zoom", pos))
            elif next_op == 0x5a:  # mul - this is GameViewMatrix.Zoom
                candidates.append(("view_matrix_zoom", pos))

    return candidates


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

    # find zoom clamp locations
    clamps = find_zoom_clamps(bytes(data))

    if not clamps:
        die("No zoom clamp patterns found - wrong terraria version?")

    print(f"[+] Found {len(clamps)} zoom clamp location(s)")

    patched = 0
    for name, pos in clamps:
        byte_pos = pos + FLOAT_OFFSET
        if data[byte_pos] == OLD_FLOAT:
            print(f"[+] Patching {name} at {hex(pos)} (byte {hex(byte_pos)})")
            data[byte_pos] = NEW_FLOAT
            patched += 1
        else:
            print(f"[*] {name} at {hex(pos)} already patched or different value")

    if patched == 0:
        print("[*] Nothing to patch - already patched?")
        return

    with open(exe_path, "wb") as f:
        f.write(data)

    print(f"[+] Done! Patched {patched} location(s).")
    print("[*] Zoom slider minimum changed from 1.0 to 0.5")
    print("[*] Set zoom to ~56% on ultrawide for true 1.0x zoom")


if __name__ == "__main__":
    main()
