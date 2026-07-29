@echo off
setlocal EnableDelayedExpansion
REM JAZZ-UI-001: stand-in for hgnvcompress (called by ModItemDecalEntity:ImportImage).
REM Do NOT rely on %~dp0 ??? paths with spaces ("Jagged Alliance 3") break it under CreateProcess/cmd.

set "LOGDIR=%APPDATA%\Jagged Alliance 3\Editor\e6L4ECj"
if not exist "%LOGDIR%" mkdir "%LOGDIR%" >nul 2>&1
set "LOG=%LOGDIR%\wepicon_hook.log"
echo [%DATE% %TIME%] args: %*>>"%LOG%"

REM --- find raw capture among args (quoted paths with spaces OK via %~1) ---
set "IMG="
:parse
if "%~1"=="" goto parsed
echo %~1| findstr /i /c:".raw.png" >nul
if not errorlevel 1 set "IMG=%~1"
shift
goto parse
:parsed

if not defined IMG (
  echo [%DATE% %TIME%] no .raw.png in args>>"%LOG%"
  exit /b 1
)

set "OUT=!IMG:.raw.png=.png!"

REM --- locate key_weapon_icon.ps1 without %~dp0 ---
set "SCRIPT="
for /d %%D in ("%APPDATA%\Jagged Alliance 3\Mods\*") do (
  if exist "%%~D\Code\key_weapon_icon.ps1" set "SCRIPT=%%~D\Code\key_weapon_icon.ps1"
)
if not defined SCRIPT if exist "%~dp0key_weapon_icon.ps1" set "SCRIPT=%~dp0key_weapon_icon.ps1"

echo [%DATE% %TIME%] key "!IMG!" -^> "!OUT!">>"%LOG%"
echo [%DATE% %TIME%] script="!SCRIPT!">>"%LOG%"

if not defined SCRIPT (
  echo [%DATE% %TIME%] SCRIPT not found under Mods/*/Code>>"%LOG%"
  exit /b 2
)
if not exist "!SCRIPT!" (
  echo [%DATE% %TIME%] SCRIPT MISSING on disk>>"%LOG%"
  exit /b 2
)
if not exist "!IMG!" (
  echo [%DATE% %TIME%] IMG MISSING on disk>>"%LOG%"
  exit /b 3
)

powershell -NoProfile -ExecutionPolicy Bypass -File "!SCRIPT!" -Path "!IMG!" -OutPath "!OUT!" -Compress 0.57 -OutW 512 -OutH 256 >>"%LOG%" 2>&1
set "ERR=!ERRORLEVEL!"
echo [%DATE% %TIME%] powershell exit=!ERR!>>"%LOG%"
if exist "!OUT!" (
  for %%Z in ("!OUT!") do echo [%DATE% %TIME%] OUT bytes=%%~zZ>>"%LOG%"
) else (
  echo [%DATE% %TIME%] OUT MISSING>>"%LOG%"
)
exit /b !ERR!
