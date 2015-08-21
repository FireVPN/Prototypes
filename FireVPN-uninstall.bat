@echo off
echo -----FireVPN deinstallieren-----
if %PROCESSOR_ARCHITECTURE%==x86 (
  cd "C:\Program Files\OpenVPN"
) else (
  cd "C:\Program Files (x86)\OpenVPN"
)
Uninstall.exe /S
echo -----Daten entfernen-----
cd ..
timeout 5 > NUL
del /S /Q OpenVPN
rd /s /Q OpenVPN