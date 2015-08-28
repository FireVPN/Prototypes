cd > temp.txt
set /p STARTDIR=<temp.txt
del temp.txt
echo -----OpenVPN herunterladen-----
bitsadmin /transfer FireVPN /download /priority high http://www.openvpn.net/release/openvpn-2.1.3-install.exe c:\openvpn-install.exe
echo -----OpenVPN installieren-----
c:\openvpn-install.exe /SELECT_OPENSSL_UTILITIES=1 /SELECT_EASYRSA=1 /S
echo -----OpenVPN konfigurieren-----
if %PROCESSOR_ARCHITECTURE%==x86 (
  cd "C:\Program Files\OpenVPN\easy-rsa"
) else (
  cd "C:\Program Files (x86)\OpenVPN\easy-rsa"
)
call init-config
if %PROCESSOR_ARCHITECTURE%==x86 (
  echo set HOME="C:\Program Files\OpenVPN\easy-rsa"> vars.bat
) else (
  echo set HOME="C:\Program Files (x86)\OpenVPN\easy-rsa"> vars.bat
)
echo set KEY_CONFIG=openssl.cnf>> vars.bat
echo set KEY_DIR=keys>> vars.bat
echo set KEY_SIZE=1024>> vars.bat
echo set KEY_COUNTRY=AT>> vars.bat
echo set KEY_PROVINCE=VIE>> vars.bat
echo set KEY_CITY=Vienna>> vars.bat
echo set KEY_ORG=FireVPN>> vars.bat
echo set KEY_EMAIL=mail@host.domain>> vars.bat
call vars
call clean-all
echo Zertifikate einrichtenm
(
echo(
echo(
echo(
echo(
echo(
echo server
echo(
) | ..\bin\openssl req -days 3650 -nodes -new -x509 -keyout %KEY_DIR%\ca.key -out %KEY_DIR%\ca.crt -config %KEY_CONFIG%


cd %STARTDIR%