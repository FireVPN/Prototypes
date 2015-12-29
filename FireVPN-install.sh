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
	cp -r /usr/share/easy-rsa /etc/openvpn/easy-rsa2
	cd /etc/openvpn/easy-rsa2/easy-rsa
	echo "export EASY_RSA=/etc/openvpn/easy-rsa2/easy-rsa"> vars
	echo 'export KEY_CONFIG="$EASY_RSA/openssl.cnf"'>> vars
	echo "export KEY_DIR=.\keys">> vars
	echo "export KEY_SIZE=1024">> vars
	echo "export KEY_COUNTRY=AT">> vars
	echo "export KEY_PROVINCE=VIE">> vars
	echo "export KEY_CITY=Vienna">> vars
	echo "export KEY_ORG=FireVPN">> vars
	echo "export KEY_EMAIL=mail@host.domain">> vars
	echo 'export KEY_ALTNAMES="FireVPN"'>> vars
	mkdir -p keys
	OPEN="$(find -name 'openssl-*.cnf' | sort -V | tail -1)"
	cp "$OPEN" openssl.cnf
	source ./vars
	./clean-all
	printf "\n\n\n\n\n\nserver\n" | ./build-ca
	./build-key-server server
fi