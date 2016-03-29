#!/bin/bash
if [ -z ${1+x} ]; then echo "Bitte einen Parameter angeben [server/client]" && exit; fi
echo "----------Überprüfen, ob openvpn und easy-rsa installiert sind----------"
if [ $(dpkg-query -W -f='${Status}' openvpn 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    echo "-----OpenVPN installieren-----"
    apt-get install openvpn -y
fi
if [ $(dpkg-query -W -f='${Status}' easy-rsa 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    echo "-----easy-rsa installieren-----"
    apt-get install wget -y
	wget http://ftp.at.debian.org/debian/pool/main/e/easy-rsa/easy-rsa_2.2.2-1_all.deb
	dpkg --install easy-rsa_2.2.2-1_all.deb
fi
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
    . ./vars
    ./clean-all
    printf "\n\n\n\n\n\n\n\n" | ./build-ca
    printf "\n\n\n\n\n\n\n\n\n\ny" | ./build-key-server --batch server
    printf "\n\n\n\n\n\n\n\n\n\ny" | ./build-key --batch client
	./build-dh
fi
