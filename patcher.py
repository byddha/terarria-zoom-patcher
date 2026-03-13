#!/usr/bin/env python3
"""
Terraria zoom patcher for ultrawide/high-res monitors.

Flips SupportWideScreen from false to true in Main's static initializer.
With SupportWideScreen enabled, the game skips its forced zoom-in and removes the 1920x1200 render-target cap.

Optional --8k flag raises the 4096 caps to 8192 for 32:9 / 8K displays.
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


def find_and_patch_8k_limits(data):
    """Patch 4096 -> 8192 for 32:9 / 8K monitors.

    Patches the following:
      - SetGraphicsProfileInternal: maxScreenW, maxScreenH, _renderTargetMaxSize (3x)
      - InitTargets: val = 4096 render target dimension cap (1x)
    """
    ok = False

    # Three consecutive: ldc.i4 4096 (20 00 10 00 00) + stsfld (80 XX XX XX XX)
    pattern_4096 = bytes.fromhex("20 00 10 00 00 80")
    pattern_8192 = bytes.fromhex("20 00 20 00 00 80")

    for pattern, already in [(pattern_4096, False), (pattern_8192, True)]:
        pos = 0
        while pos < len(data) - 30:
            pos = data.find(pattern, pos)
            if pos == -1:
                break
            # verify all three are consecutive (each is 10 bytes: 5 ldc.i4 + 5 stsfld)
            if data[pos + 10:pos + 16] == pattern and data[pos + 20:pos + 26] == pattern:
                if already:
                    print("[*] SetGraphicsProfileInternal already at 8192")
                else:
                    for i in range(3):
                        off = pos + i * 10
                        print(f"[+] 4096 -> 8192 at {hex(off)}")
                        data[off + 2] = 0x20 # 0x10 (4096) -> 0x20 (8192)
                ok = True
                break
            pos += 1
        if ok:
            break

    # ldc.i4 4096 (20 00 10 00 00) + stloc, preceded by ldc.i4.1 (true) + branch
    STLOC = (0x0a, 0x0b, 0x0c, 0x0d, 0x13)  # stloc.0 through stloc.s
    BRANCH = (0x33, 0x40, 0xFE)             # brfalse.s, brfalse, ceq/prefix

    for needle, is_patched in [(b"\x20\x00\x10\x00\x00", False),
                               (b"\x20\x00\x20\x00\x00", True)]:
        pos = 0
        found = False
        while pos < len(data) - 6:
            pos = data.find(needle, pos)
            if pos == -1:
                break
            # must be followed by a stloc
            if data[pos + 5] not in STLOC:
                pos += 1
                continue
            # look back for ldc.i4.1 (0x17) + branch
            window = data[max(0, pos - 15):pos]
            has_hidef_check = any(
                window[i] == 0x17 and window[i + 1] in BRANCH
                for i in range(len(window) - 1)
            )
            if has_hidef_check:
                if is_patched:
                    print("[*] InitTargets already at 8192")
                else:
                    print(f"[+] 4096 -> 8192 at {hex(pos)} (InitTargets)")
                    data[pos + 2] = 0x20
                ok = True
                found = True
                break
            pos += 1
        if found:
            break

    return ok


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if len(args) < 1:
        print("Usage: python patcher.py /path/to/Terraria.exe [--8k]")
        print("  --8k  Patch 4096->8192 limit for 32:9 / 8K monitors")
        sys.exit(1)

    exe_path = args[0]
    enable_8k = "--8k" in flags
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

    if enable_8k:
        if not find_and_patch_8k_limits(data):
            die("Could not find 4096 limits for 8K patch")

    with open(exe_path, "wb") as f:
        f.write(data)

    msg = "Widescreen support enabled"
    if enable_8k:
        msg += " + 8K limits raised"
    print(f"[+] Done! {msg}.")


if __name__ == "__main__":
    main()
