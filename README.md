Useful for ultrawide/widescreen monitor users, because Terraria doesn't handle zoom well for those (you will see less content on the screen than on a normal monitor)

## Requirements:
Python available in PATH

## Backup
This script creates a `Terraria.exe.bak` for you before applying the patch. If somehow in the far future this doesn't work anymore, you can just delete your `Terraria.exe` and rename `Terraria.exe.bak` to `Terraria.exe`.

## Usage
### Manual
Download `patcher.py` and run it using `python patcher.py <PATH_TO_TERRARIA_EXE>`. If you find it more convenient, use one of the commands below.
> [!NOTE]  
> If you are using Windows there is a high chance you don't have python installed. You can check using `python --version` in powershell. If you don't know what you are doing, the easiest way to install python on windows is using `winget install Python`.

### Linux
Adapt the path to terraria exe
```bash
curl -sSL https://raw.githubusercontent.com/byddha/terarria-zoom-patcher/refs/heads/main/patcher.py | python - <PATH_TO_TERRARIA_EXE>
```

Alternatively, if you have fd

```bash
curl -sSL https://raw.githubusercontent.com/byddha/terarria-zoom-patcher/refs/heads/main/patcher.py | python - $(fd Terraria.exe --base-directory / --absolute-path)
```

### Windows

Adapt the path to terraria exe
```powershell
powershell -NoProfile -ExecutionPolicy ByPass -Command "& { (Invoke-WebRequest -Uri https://raw.githubusercontent.com/byddha/terarria-zoom-patcher/refs/heads/main/patcher.py).Content | python - '<PATH_TO_TERRARIA_EXE>' }"
```

### Screenshots (3440x1440)
Pre-fix (zoom "100%" / normal 177%):
![image](https://github.com/user-attachments/assets/0cd47ca2-2750-4a97-9cb4-6dbf2a738eef)

Post-fix (zoom 100%)
![image](https://github.com/user-attachments/assets/cacc6de4-0017-4235-b944-55e6d7778cf5)

Post-fix (zoom 125%)
![image](https://github.com/user-attachments/assets/40eed5b0-77aa-46f9-8c1f-c509eba9d5d9)

Post-fix (zoom 150%)
![image](https://github.com/user-attachments/assets/a91b8afb-861a-47f1-b83b-92cf45f38db3)

Replace with: "00 00 F0 55 80 55 0C 00 04 22 00 00 96 44"

I only tested it myself with a 21:9 aspect ratio at 2560x1080 resolution. It works perfectly for me. Good luck for everyone. ;)
```
