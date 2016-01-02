#!/bin/bash
if [ -z ${1+x} ]; then echo "Bitte einen Parameter angeben [server/client]" && exit; fi
echo "----------Paket-Management erkennen----------"
declare -A osInfo;
osInfo[/etc/redhat-release]=yum
osInfo[/etc/arch-release]=pacman
osInfo[/etc/gentoo-release]=emerge
osInfo[/etc/SuSE-release]=zypp
osInfo[/etc/debian_version]=apt-get

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        echo Package manager: ${osInfo[$f]}
    echo "-----OpenVPN installieren-----"
	${osInfo[$f]} install OpenVPN easy-rsa --assume-yes
    fi
done
echo "-----OpenVPN konfigurieren-----"
if [ "$1" = "server" ];then
	cp server.ovpn /etc/openvpn
fi
if [ "$1" = "client" ];then
	cp client.ovpn /etc/openvpn
fi
if [ "$1" = "server" ];then
	cp -r /usr/share/easy-rsa /etc/openvpn/easy-rsa
	cd /etc/openvpn/easy-rsa
	echo 'export EASY_RSA="`pwd`"'> vars
	echo 'export OPENSSL="openssl"'>> vars
	echo 'export PKCS11TOOL="pkcs11-tool"'>> vars
	echo 'export GREP="grep"'>> vars
	echo 'export KEY_CONFIG=`$EASY_RSA/whichopensslcnf $EASY_RSA`'>> vars
	echo 'export KEY_DIR="$EASY_RSA/keys"'>> vars
	echo 'export PKCS11_MODULE_PATH="dummy"'>> vars
	echo 'export PKCS11_PIN="dummy"'>> vars
	echo "export KEY_SIZE=1024">> vars
	echo "export CA_EXPIRE=3650">> vars
	echo "export KEY_EXPIRE=3650">> vars
	echo "export KEY_COUNTRY=AT">> vars
	echo "export KEY_PROVINCE=VIE">> vars
	echo "export KEY_CITY=Vienna">> vars
	echo "export KEY_ORG=FireVPN">> vars
	echo "export KEY_EMAIL=mail@host.domain">> vars
	echo "export KEY_OU=FireVPN">> vars
	echo 'export KEY_ALTNAMES="FireVPN"'>> vars
	echo 'export KEY_NAME="server"'>> vars
	mkdir -p keys
	source ./vars
	./clean-all
	printf "\n\n\n\n\n\n\n\n" | ./build-ca
	printf "\n\n\n\n\n\n\n\n\n\ny" | ./build-key-server --batch server
	printf "\n\n\n\n\n\n\n\n\n\ny" | ./build-key --batch client
fi
