# Screen Time Limiter

## Overview

The **Screen Time Limiter** is a Python-based desktop utility that allows users to restrict the amount of time specific applications can run on their system. Once the allotted screen time is used up, the tracked application is automatically terminated.

## Features

- Add any executable application and assign a custom usage time.
- Accurate tracking using full-path process detection.
- Automatically terminates processes that exceed allowed time.
- GUI display of remaining screen time.
- Save/load tracked applications from a JSON file.
- Minimize app to system tray.
- Basic password authentication to prevent unauthorized changes.
- Packaged as a `.exe` for Windows with a professional installer.

## Tech Stack

- **Language:** Python 3.9+
- **GUI Framework:** Tkinter
- **Process Management:** psutil
- **Tray Icon Support:** pystray, Pillow
- **Installer Tools:** PyInstaller and Inno Setup

## Dependencies

Install via pip:

```bash
pip install psutil pystray pillow
```

## How it Works

1. User selects an application (.exe) to track.
2. Specifies a time limit in minutes.
3. Tracker monitors all system processes.
4. If the tracked app is detected and exceeds the allowed time, it is terminated.
5. Remaining time is shown live in the app GUI.

## Authentication

- Basic password prompt at startup using `tkinter.simpledialog`.
- Default password: `admin123` (can be changed in the script).

## File Structure

- `screen_time_limiter.py`: Main application code.
- `tracked_apps.json`: JSON file to store app paths and time limits.
- `screen_time_limiter.exe`: Compiled executable (via PyInstaller).
- `ScreenTimeLimiterSetup.exe`: Windows installer (via Inno Setup).

## Building the Executable

Use PyInstaller:

```bash
pyinstaller --onefile --noconsole --icon=app.ico screen_time_limiter.py
```

## Creating the Installer

Use Inno Setup with the following script:

```ini
[Setup]
AppName=Screen Time Limiter
AppVersion=1.0
DefaultDirName={pf}\Screen Time Limiter
DefaultGroupName=Screen Time Limiter
OutputBaseFilename=ScreenTimeLimiterSetup
Compression=lzma
SolidCompression=yes
DefaultIconFilename=app.ico

[Files]
Source: "screen_time_limiter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Screen Time Limiter"; Filename: "{app}\screen_time_limiter.exe"
Name: "{group}\Uninstall Screen Time Limiter"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Screen Time Limiter"; Filename: "{app}\screen_time_limiter.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\screen_time_limiter.exe"; Description: "Launch app"; Flags: nowait postinstall skipifsilent
```

## Tested On

- Windows 10/11 (64-bit)
- Python 3.10+

## References

- [psutil Documentation](https://psutil.readthedocs.io/en/latest/)
- [Tkinter (Python Docs)](https://docs.python.org/3/library/tkinter.html)
- [Pystray GitHub](https://github.com/moses-palmer/pystray)
- [Pillow Docs](https://pillow.readthedocs.io/en/stable/)
- [PyInstaller](https://pyinstaller.org/)
- [Inno Setup](https://jrsoftware.org/isinfo.php)

## Future Improvements

- Usage history with charts
- Scheduled app availability
- Enhanced authentication system
- Time warnings and parental control mode

---

Built with ❤ by Ife_code
