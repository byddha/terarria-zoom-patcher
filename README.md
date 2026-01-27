# Terraria Zoom Patcher

Terraria calculates minimum zoom as `max(1.0, screenWidth/1920, screenHeight/1200)`. On ultrawide (3440x1440), this means 1.79x minimum - the slider shows "100%" but you're actually at 179%, seeing the same world as a 1920x1200 monitor. This patcher removes that limit.

For resolutions above 4096 (e.g. 5120x1440), use the `--8k` flag.

## Requirements
Python available in PATH

## Usage

```bash
python patcher.py <PATH_TO_TERRARIA_EXE>
```

For resolutions exceeding 4096 in width or height (e.g. 5120x1440), add the `--8k` flag:
```bash
python patcher.py <PATH_TO_TERRARIA_EXE> --8k
```

> [!NOTE]
> Windows users: check if python is installed with `python --version`. If not, install with `winget install Python`.

### One-liner (Linux)
```bash
curl -sSL https://raw.githubusercontent.com/byddha/terarria-zoom-patcher/refs/heads/main/patcher.py | python - <PATH_TO_TERRARIA_EXE>
```

### One-liner (Windows PowerShell)
```powershell
powershell -NoProfile -ExecutionPolicy ByPass -Command "& { (Invoke-WebRequest -Uri https://raw.githubusercontent.com/byddha/terarria-zoom-patcher/refs/heads/main/patcher.py).Content | python - '<PATH_TO_TERRARIA_EXE>' }"
```

## Backup
The script creates `Terraria.exe.bak` before patching. To restore, delete `Terraria.exe` and rename `Terraria.exe.bak` back.

## What it patches
1. `ForcedMinimumZoom = 1.0` - removes forced zoom-in
2. Render target size cap removal - fixes culling at certain zoom levels
3. `--8k`: 4096 → 8192 limit - for resolutions exceeding 4096 in any dimension

## Screenshots (3440x1440)

Pre-fix (zoom "100%" / actual 177%):
![image](https://github.com/user-attachments/assets/0cd47ca2-2750-4a97-9cb4-6dbf2a738eef)

Post-fix (zoom 100%):
![image](https://github.com/user-attachments/assets/cacc6de4-0017-4235-b944-55e6d7778cf5)

Post-fix (zoom 125%):
![image](https://github.com/user-attachments/assets/40eed5b0-77aa-46f9-8c1f-c509eba9d5d9)

Post-fix (zoom 150%):
![image](https://github.com/user-attachments/assets/a91b8afb-861a-47f1-b83b-92cf45f38db3)
