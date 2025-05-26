## Requirements:
Python available in PATH

## Usage
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
