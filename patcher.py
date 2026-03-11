#!/usr/bin/env python3
"""
Terraria zoom patcher for ultrawide/high-res monitors.

Flips SupportWideScreen from false to true in Main's static initializer.
With SupportWideScreen enabled, the game skips its forced zoom-in and removes the 1920x1200 render-target cap.

ReLogic looks to be planning to natively support this feature, so the need for this utility should be temporary.
"""

import sys
import os
import shutil


def die(msg):
    print(f"[!] {msg}")
    sys.exit(1)


def find_and_patch_support_widescreen(data):
    """Flip SupportWideScreen from false to true in Main's static initializer."""
    # Anchor: _renderTargetMaxSize = 2048
    #   IL: ldc.i4 2048 (20 00 08 00 00) + stsfld (80 XX XX XX 04)
    # Followed immediately by: SupportWideScreen = false
    #   IL: ldc.i4.0 (16) + stsfld (80 XX XX XX 04)
    anchor = bytes.fromhex("20 00 08 00 00 80")
    pos = 0
    while True:
        pos = data.find(anchor, pos)
        if pos == -1:
            break
        if pos + 16 <= len(data) and data[pos + 9] == 0x04:
            target = pos + 10
            if data[target] == 0x16 and data[target + 1] == 0x80 and data[target + 5] == 0x04:
                print(f"[+] Found SupportWideScreen = false at {hex(target)}")
                data[target] = 0x17  # ldc.i4.1 (true)
                print(f"[+] Set SupportWideScreen = true")
                return True
            if data[target] == 0x17 and data[target + 1] == 0x80 and data[target + 5] == 0x04:
                print(f"[*] SupportWideScreen already patched at {hex(target)}")
                return True
        pos += 1
    return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(args) < 1:
        print("Usage: python patcher.py /path/to/Terraria.exe")
        sys.exit(1)

    exe_path = args[0]
    backup_path = f"{exe_path}.bak"

    if not os.path.exists(exe_path):
        die(f"File not found: {exe_path}")

    print("--- Terraria Zoom Patcher ---")

    if not os.path.exists(backup_path):
        print(f"[*] Creating backup: {backup_path}")
        shutil.copy2(exe_path, backup_path)
    else:
        print(f"[*] Backup exists: {backup_path}")

    with open(exe_path, "rb") as f:
        data = bytearray(f.read())

    if not find_and_patch_support_widescreen(data):
        die("Could not find SupportWideScreen field")

    with open(exe_path, "wb") as f:
        f.write(data)

    print("[+] Done! Widescreen support enabled.")


if __name__ == "__main__":
    main()
