Version agnostic zoom patcher for terraria. Useful for ultrawide/widescreen monitor users, because Terraria doesn't handle zoom well for those (you will see less content on the screen than on a normal monitor). Unless terraria itself adresses this issue or receives some huge engine changes, this script will work on upcoming updates.

If you don't want to use this script, you can check out https://www.reddit.com/r/widescreengamingforum/comments/r21dfz/terraria_ultrawide_fix_1400_1432_219_2560x1080/, find the appropriate values for your terraria version and manually edit the hex values of Terraria.exe; When terraria updates, you will have to wait until someone drops the new values for the current version. To find them yourself, search for such a pattern `00 00 F0 44 ?? ?? ?? ?? ?? ?? 00 00 96 44`, then apply the same fix. The question marks are the values that change between updates. 

## Requirements:
Python available in PATH

## Usage
### Manual
Download `patcher.py` and run it using `python patcher.py <PATH_TO_TERRARIA_EXE>`. If you find it more convenient, use one of the commands below.
> [!NOTE]  
> If you are using Windows there is a high chance you don't have python installed. You can check using `python --version` in powershell. If you don't know what you are doing, the easiest way to install python on windows is using `winget install Python`.

### Linux
Adapt the path to terraria exe
```bash
curl -sSL https://raw.githubusercontent.com/drzbida/terarria-zoom-patcher/refs/heads/main/patcher.py | python - <PATH_TO_TERRARIA_EXE>
```

Alternatively, if you have fd

```bash
curl -sSL https://raw.githubusercontent.com/drzbida/terarria-zoom-patcher/refs/heads/main/patcher.py | python - $(fd Terraria.exe --base-directory / --absolute-path)
```

### Windows

Adapt the path to terraria exe
```powershell
powershell -NoProfile -ExecutionPolicy ByPass -Command "& { (Invoke-WebRequest -Uri https://raw.githubusercontent.com/drzbida/terarria-zoom-patcher/refs/heads/main/patcher.py).Content | python - '<PATH_TO_TERRARIA_EXE>' }"
```

### Screenshots
Pre-fix (zoom "100%" / normal 177%):
![image](https://github.com/user-attachments/assets/0cd47ca2-2750-4a97-9cb4-6dbf2a738eef)

Post-fix (zoom 100%)
![image](https://github.com/user-attachments/assets/cacc6de4-0017-4235-b944-55e6d7778cf5)

Post-fix (zoom 125%)
![image](https://github.com/user-attachments/assets/40eed5b0-77aa-46f9-8c1f-c509eba9d5d9)

Post-fix (zoom 150%)
![image](https://github.com/user-attachments/assets/a91b8afb-861a-47f1-b83b-92cf45f38db3)
