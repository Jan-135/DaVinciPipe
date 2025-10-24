@echo off
rem------------------------------------------------------
rem Launching DaVinci Resolve
rem------------------------------------------------------

rem Resolve Path
set "DAVINCI_RESOLVE_PATH=C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"

rem Set Environment Variables
RESOLVE_SCRIPT_API ="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
PYTHONPATH = "%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\;N:\vendor"

rem Set Startup Scripting
set "DAVINCI_RESOLVE_STARTUP_SCRIPT=N:\test\startup.py"

rem Launch
echo Launching DaVinci Resolve
start "" "&DAVINCI_RESOLVE_PATH" "&DAVINCI_RESOLVE_STARTUP_SCRIPT"

exit /b 0