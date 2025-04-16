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
; Optional icon if you want to install it
Source: "app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Screen Time Limiter"; Filename: "{app}\screen_time_limiter.exe"
Name: "{group}\Uninstall Screen Time Limiter"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Screen Time Limiter"; Filename: "{app}\screen_time_limiter.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\screen_time_limiter.exe"; Description: "Launch app"; Flags: nowait postinstall skipifsilent
