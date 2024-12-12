[Setup]
AppName=Escaner AT
AppVersion=1.0
DefaultDirName={pf}\Escaner_AT
DefaultGroupName=Escaner AT
OutputBaseFilename=Instalador_Escaner_AT
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\APUESTA TOTAL\Documents\py\escaner_at-main\dist\ESCANER AT.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\APUESTA TOTAL\Documents\py\escaner_at-main\build\*"; DestDir: "{app}\recursos"; Flags: recursesubdirs

[Icons]
Name: "{commondesktop}\Escaner AT"; Filename: "{app}\ESCANER AT.exe"; WorkingDir: "{app}"; 
Name: "{group}\Escaner AT"; Filename: "{app}\ESCANER_AT.exe"
Name: "{group}\Uninstall Escaner AT"; Filename: "{uninstallexe}"