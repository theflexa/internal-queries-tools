#define MyAppName "DeepSeek Tool"
#define MyAppVersion "0.0.12"
#define MyAppPublisher "Flexa"
#define MyAppURL "https://github.com/theflexa/internal-queries-tools"
#define MyAppExeName "DeepSeek-Tool-v0.0.12.exe"

[Setup]
; Configurações básicas
AppId={{B8E5F0A0-D1C4-4F1B-9B4E-3E0E0A0F0B0B}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\..\LICENSE.txt
OutputDir=..\..\installer
OutputBaseFilename=DeepSeek-Tool-Setup
SetupIconFile=..\..\assets\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; Requisitos mínimos
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Arquivo principal
Source: "..\..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Arquivos adicionais
Source: "..\..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\..\\.env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{app}\logs"; Permissions: users-full

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Cria diretório de logs com permissões corretas
    ForceDirectories(ExpandConstant('{app}\logs'));
    // Garante permissões de escrita para usuários
    Exec('icacls.exe', ExpandConstant('"{app}\logs" /grant Users:(OI)(CI)F'), '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end; 