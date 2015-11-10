IF [%1] == [] (
echo Bitte einen Parameter angeben [server/client]
exit /b
)
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
echo set KEY_DIR=.\keys>> vars.bat
echo set KEY_SIZE=1024>> vars.bat
echo set KEY_COUNTRY=AT>> vars.bat
echo set KEY_PROVINCE=VIE>> vars.bat
echo set KEY_CITY=Vienna>> vars.bat
echo set KEY_ORG=FireVPN>> vars.bat
echo set KEY_EMAIL=mail@host.domain>> vars.bat
call vars
call clean-all
copy %STARTDIR%\client.ovpn ..\config
if %1==server (
echo -----Zertifikate für Server einrichten-----
cd %HOME%
copy %STARTDIR%\server.ovpn ..\config
(
echo .
echo .
echo .
echo .
echo .
echo FireVPN
echo .
)| ..\bin\openssl.exe req -days 3650 -nodes -new -x509 -keyout %KEY_DIR%\ca.key -out %KEY_DIR%\ca.crt -config %KEY_CONFIG%
(
echo .
echo .
echo .
echo .
echo .
echo server
echo .
echo FireVPNPasswort
echo .
)| ..\bin\openssl.exe req -days 3650 -nodes -new -keyout %KEY_DIR%\server.key -out %KEY_DIR%\server.csr -config %KEY_CONFIG%
(
echo y
echo y
)| ..\bin\openssl.exe ca -days 3650 -out %KEY_DIR%\server.crt -in %KEY_DIR%\server.csr -extensions server -config %KEY_CONFIG%
del /q %KEY_DIR%\*.old
(
echo .
echo .
echo .
echo .
echo .
echo client
echo .
echo FireVPNPasswort
echo .
)| ..\bin\openssl.exe req -days 3650 -nodes -new -keyout %KEY_DIR%\client.key -out %KEY_DIR%\client.csr -config %KEY_CONFIG%
(
echo y
echo y
)| ..\bin\openssl.exe ca -days 3650 -out %KEY_DIR%\client.crt -in %KEY_DIR%\client.csr -config %KEY_CONFIG%
echo -----Diffie Hellman Parameter generieren-----
build-dh
copy keys\ca.crt ..\config
copy keys\dh1024.pem ..\config
copy keys\server.crt ..\config
copy keys\server.key ..\config
mkdir ..\transfer_to_client
copy keys\ca.crt ..\transfer_to_client
copy keys\client.crt ..\transfer_to_client
copy keys\client.key ..\transfer_to_client
echo "nach C:\\Programme\Openvpn\config" > ..\transfer_to_client\readme.txt
explorer.exe ..\transfer_to_client
del /q %KEY_DIR%\*.old
cd %STARTDIR%
)
cd %STARTDIR%
powershell "cd '%HOME%\..\bin\'; $temp=.\openvpn.exe --show-adapters | select-object -last 1 ; $temp.SubString(0, $temp.LastIndexOf(' '))" > tmp.txt
set /p adaptername=<tmp.txt
set adaptername=%adaptername:~1,-1%
netsh interface set interface name="%adaptername%" newname="MyTap"
del tmp.txt