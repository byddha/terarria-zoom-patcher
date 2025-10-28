Version agnostic zoom patcher for terraria. Useful for ultrawide/widescreen monitor users, because Terraria doesn't handle zoom well for those (you will see less content on the screen than on a normal monitor). Unless terraria itself adresses this issue or receives some huge engine changes, this script will work on upcoming updates.

If you don't want to use this script, you can check out this [Reddit post](https://github.com/byddha/terarria-zoom-patcher/blob/main/README.md#reddit-post)

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

### Reddit post
https://www.reddit.com/r/widescreengamingforum/comments/r21dfz/terraria_ultrawide_fix_1400_1432_219_2560x1080/ : find the appropriate values for your terraria version and manually edit the hex values of Terraria.exe; When terraria updates, you will have to wait until someone drops the new values for the current version. To find them yourself, search for such a pattern `00 00 F0 44 ?? ?? ?? ?? ?? ?? 00 00 96 44`, then apply the same fix. The question marks are the values that change between updates. 

I've copied the content of the post below, in case it gets deleted / link doesn't work anymore etc.

```
r/widescreengamingforum icon
Go to widescreengamingforum
r/widescreengamingforum
•
4 yr. ago
REDACTED
Terraria Ultrawide Fix 1.4.0.0 - 1.4.3.2 (21:9 2560x1080)
PSA

Use the HxD editor to open the Terraria.exe file and replace the following lines.

Video: https://www.youtube.com/watch?v=NEQNca-o2rY

HxD Editor: https://mh-nexus.de/en/hxd/

1.4.0.0 - 1.4.0.1 - 1.4.0.2

Search for: "00 00 F0 44 80 38 0B 00 04 22 00 00 96 44"

Replace with: "00 00 00 46 80 38 0B 00 04 22 00 00 00 46"

1.4.0.3

Search for: "00 00 F0 44 80 3B 0B 00 04 22 00 00 96 44"

Replace with: "00 00 00 46 80 3B 0B 00 04 22 00 00 00 46"

1.4.0.4

Search for: " 00 00 F0 44 80 3D 0B 00 04 22 00 00 96 44 "

Replace with: " 00 00 00 46 80 3D 0B 00 04 22 00 00 00 46 "

1.4.0.5

Search for: "00 00 F0 44 80 4C 0B 00 04 22 00 00 96 44"

Replace with: "00 00 00 46 80 4C 0B 00 04 22 00 00 00 46"

1.4.1.0 - 1.4.1.1

Seach for: "00 00 F0 44 80 7A 0B 00 04 22 00 00 96 44"

Replace with: "00 00 00 46 80 7A 0B 00 04 22 00 00 00 46"

1.4.1.2

Seach for: "00 00 F0 44 80 7A 0B 00 04 22 00 00 96 44"

Replace with: "00 00 00 46 80 82 0B 00 04 22 00 00 00 46"

1.4.2.2

Seach for: "00 00 F0 44 80 86 0B 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 86 0B 00 04 22 00 00 96 44"

1.4.2.3

Seach for: "00 00 F0 44 80 87 0B 00 04 22 00 00 96 44"

Replace with: "00 00 FF 55 80 87 0B 00 04 22 00 00 96 44"

1.4.3.0 - 1.4.3.1

Seach for: "00 00 F0 44 80 A6 0B 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 A6 0B 00 04 22 00 00 96 44"

1.4.3.2

Seach for: "00 00 F0 44 80 AC 0B 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 AC 0B 00 04 22 00 00 96 44"

1.4.4.5

Seach for: "00 00 F0 44 80 67 0C 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 67 0C 00 04 22 00 00 96 55"

1.4.4.6

Search for: "00 00 F0 44 80 6B 0C 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 6B 0C 00 04 22 00 00 96 44"

1.4.4.8

Search for: "00 00 F0 44 80 53 0C 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 53 0C 00 04 22 00 00 96 44"

1.4.4.8.1

Search for: "00 00 F0 44 80 53 0C 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 53 0C 00 04 22 00 00 96 44"

1.4.4.9

Search for: "00 00 F0 44 80 55 0C 00 04 22 00 00 96 44"

Replace with: "00 00 F0 55 80 55 0C 00 04 22 00 00 96 44"

I only tested it myself with a 21:9 aspect ratio at 2560x1080 resolution. It works perfectly for me. Good luck for everyone. ;)
```
