@echo off
setlocal EnableDelayedExpansion
REM JAZZ-UI-001: stand-in for hgnvcompress. If any arg is a wepicon*.raw.png, key it to .png.
REM Otherwise exit 1 (decal import in Mod Editor will fail while jazz is loaded — acceptable for now).

set "LOG=%APPDATA%\Jagged Alliance 3\Editor\e6L4ECj\wepicon_hook.log"
if not exist "%APPDATA%\Jagged Alliance 3\Editor\e6L4ECj" mkdir "%APPDATA%\Jagged Alliance 3\Editor\e6L4ECj" >nul 2>&1
echo [%DATE% %TIME%] args: %*>>"%LOG%"

set "IMG="
for %%A in (%*) do (
  echo %%~A| findstr /i /c:".raw.png" >nul && set "IMG=%%~A"
)

if not defined IMG (
  echo [%DATE% %TIME%] no .raw.png in args>>"%LOG%"
  exit /b 1
)

set "OUT=!IMG:.raw.png=.png!"
set "SCRIPT=%~dp0key_weapon_icon.ps1"
echo [%DATE% %TIME%] key "!IMG!" -^> "!OUT!" script="!SCRIPT!">>"%LOG%"

powershell -NoProfile -ExecutionPolicy Bypass -File "!SCRIPT!" -Path "!IMG!" -OutPath "!OUT!" -Compress 0.50 -OutW 512 -OutH 256 >>"%LOG%" 2>&1
set "ERR=!ERRORLEVEL!"
echo [%DATE% %TIME%] powershell exit=!ERR!>>"%LOG%"
if exist "!OUT!" (
  echo [%DATE% %TIME%] OUT exists>>"%LOG%"
) else (
  echo [%DATE% %TIME%] OUT MISSING>>"%LOG%"
)
exit /b !ERR!
