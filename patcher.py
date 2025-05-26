import sys
import os
import re
import shutil

EXE_PATH = sys.argv[1] if len(sys.argv) > 1 else None
BACKUP_PATH = f"{EXE_PATH}.bak" if EXE_PATH else None

# Pattern: 00 00 F0 44 ?? ?? ?? ?? ?? ?? 00 00 96 44
# The ?? are variable bytes depending on the version
SEARCH_BYTES = b"\x00\x00\xf0\x44" + b"." * 6 + b"\x00\x00\x96\x44"

EXPECTED_BYTE_VAL = 0x44
REPLACEMENT_BYTE_VAL = 0x55

if not EXE_PATH:
    print("Usage: python patcher.py /path/to/Terraria.exe")
    sys.exit(1)

if not os.path.exists(EXE_PATH):
    print(f"[!] Error: File not found: {EXE_PATH}")
    sys.exit(1)

print("--- Terraria Zoom Patcher ---")

if not os.path.exists(BACKUP_PATH):
    print(f"[*] Creating backup: {BACKUP_PATH}")
    try:
        shutil.copy2(EXE_PATH, BACKUP_PATH)
    except Exception as e:
        print(f"[!] Error creating backup: {e}")
        sys.exit(1)
else:
    print(f"[*] Backup already exists: {BACKUP_PATH}")

print("[*] Reading executable...")
try:
    with open(EXE_PATH, "rb") as f:
        data = bytearray(f.read())
except Exception as e:
    print(f"[!] Error reading file: {e}")
    sys.exit(1)

print("[*] Searching for default resolution limit pattern...")
matches_found = 0
patches_applied = 0

for match in re.finditer(SEARCH_BYTES, data, re.DOTALL):
    matches_found += 1
    offset = match.start()
    print(f"\n  [+] Found potential limit signature at {hex(offset)}.")

    pos1 = offset + 3
    pos2 = offset + 13
    patched_here = False

    if data[pos1] == EXPECTED_BYTE_VAL:
        print(f"    - Patching Max Width at {hex(pos1)}: Unlocking limit (44 -> 55).")
        data[pos1] = REPLACEMENT_BYTE_VAL
        patched_here = True
    else:
        print(
            f"    - Skipping Max Width ({hex(pos1)}): Found 0x{data[pos1]:X} (Expected 0x44)."
        )

    if data[pos2] == EXPECTED_BYTE_VAL:
        print(f"    - Patching Max Height at {hex(pos2)}: Unlocking limit (44 -> 55).")
        data[pos2] = REPLACEMENT_BYTE_VAL
        patched_here = True
    else:
        print(
            f"    - Skipping Max Height ({hex(pos2)}): Found 0x{data[pos2]:X} (Expected 0x44)."
        )

    if patched_here:
        patches_applied += 1

if matches_found == 0:
    print("\n[!] Default resolution pattern not found. No changes made.")
    sys.exit(0)

if patches_applied == 0:
    print("\n[*] Pattern found, but no changes needed (likely already patched).")
    sys.exit(0)

print(f"\n[*] Writing {patches_applied} change(s) to Terraria.exe...")
try:
    with open(EXE_PATH, "wb") as f:
        _ = f.write(data)
    print("\n[+] Success! Terraria's resolution limits are unlocked.")
except Exception as e:
    print(f"[!] Error writing file: {e}")
    print("[!] CRITICAL: Please restore your game from the .bak file.")
    sys.exit(1)
