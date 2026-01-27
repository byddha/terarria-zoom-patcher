#!/usr/bin/env python3
"""
Terraria zoom patcher for ultrawide/high-res monitors.

Patches:
1. ForcedMinimumZoom = 1.0 (removes forced zoom-in)
2. Removes render target 1920x1200 cap (prevents culling artifacts)
3. [optional] 4096 -> 8192 limit (for 32:9 / 8K monitors)
"""

import sys
import os
import shutil


def die(msg):
    print(f"[!] {msg}")
    sys.exit(1)


def find_and_patch_8k_limit(data):
    """Patch 4096 limits to 8192 for 32:9 / 8K support"""
    # pattern: ldc.i4 4096 (20 00 10 00 00) + stsfld (80)
    # three consecutive: maxScreenW, maxScreenH, _renderTargetMaxSize

    pattern = b"\x20\x00\x10\x00\x00\x80"
    new_val = b"\x20\x00\x20\x00\x00"  # 8192

    pos = data.find(pattern)
    if pos == -1:
        print("[*] 4096 limit not found (may already be patched)")
        return True

    # patch all three (they're consecutive)
    count = 0
    for i in range(3):
        p = data.find(pattern, pos if i == 0 else pos + 1)
        if p == -1:
            break
        print(f"[+] Patching 4096 -> 8192 at {hex(p)}")
        data[p:p+5] = new_val
        pos = p + 5
        count += 1

    return count > 0


def find_and_patch_forced_zoom(data):
    """Replace ForcedMinimumZoom = Math.Max(...) with ForcedMinimumZoom = 1.0f"""
    pos = 0
    while True:
        pos = data.find(b"\x80", pos)  # stsfld opcode
        if pos == -1:
            return False

        # field token 0x040009XX = Main class static fields
        if pos + 5 <= len(data) and data[pos+4] == 0x04 and data[pos+3] == 0x00 and data[pos+2] == 0x09:
            before = data[pos-30:pos]

            # two Math.Max calls before stsfld
            if before.count(b"\x28") >= 2 and b"\x00\x0a" in before:
                calc_region = data[pos-70:pos]
                if b"\x22\x00\x00\x80\x3f" in calc_region:  # ldc.r4 1.0f
                    # find calc start: ldsfld screenWidth + conv.r4
                    for i in range(pos-70, pos-20):
                        if (data[i] == 0x7e and data[i+4] == 0x04 and
                            data[i+3] == 0x00 and data[i+5] == 0x6b):
                            calc_start = i
                            calc_end = pos + 5
                            field_token = data[pos+1:pos+5]

                            print(f"[+] Found ForcedMinimumZoom calculation at {hex(calc_start)}-{hex(calc_end)}")

                            # ldc.r4 1.0f + stsfld + nops
                            patch = b"\x22\x00\x00\x80\x3f"
                            patch += b"\x80" + field_token
                            patch += b"\x00" * (calc_end - calc_start - len(patch))

                            data[calc_start:calc_end] = patch
                            return True
        pos += 1
    return False


def find_and_patch_render_targets(data):
    """Remove Math.Min(backBuffer, MaxWorldViewSize) cap on render targets"""
    # pattern: ldsfld MaxWorldViewSize; ldfld Point.X/Y; call Math.Min
    # replace with nops to keep backBuffer value unchanged

    patterns_found = []
    pos = 0
    while pos < len(data) - 20:
        # ldsfld (7e) + ldfld (7b) + call (28), each 5 bytes
        if (data[pos] == 0x7e and
            pos + 15 <= len(data) and
            data[pos + 5] == 0x7b and
            data[pos + 10] == 0x28):

            call_token = data[pos + 11:pos + 15]
            if call_token[3] == 0x0a:  # memberref (system method)
                after = data[pos + 15] if pos + 15 < len(data) else 0
                if after in [0x0a, 0x0b, 0x0c, 0x0d, 0x13]:  # stloc
                    field_token = data[pos + 1:pos + 5]
                    if field_token[3] == 0x04:  # field def
                        patterns_found.append(pos)
        pos += 1

    if not patterns_found:
        print("[*] Render target limit not found (may already be patched)")
        return True

    print(f"[+] Found {len(patterns_found)} render target limit(s)")

    for pos in patterns_found[:2]:
        print(f"[+] Patching render target limit at {hex(pos)}")
        for i in range(15):
            data[pos + i] = 0x00

    return True


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

    if not find_and_patch_forced_zoom(data):
        die("Could not find ForcedMinimumZoom calculation")

    find_and_patch_render_targets(data)

    if enable_8k:
        find_and_patch_8k_limit(data)

    with open(exe_path, "wb") as f:
        f.write(data)

    print("[+] Done! Zoom limit removed.")


if __name__ == "__main__":
    main()
