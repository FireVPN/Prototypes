#!/bin/bash
echo "----------Detecting the Package-Management----------"
haveProg() {
    [ -x "$(which $1)" ]
}

if haveProg apt-get ; then pac=apt-get
elif haveProg yum ; then pac=yum
elif havePrg pacman ; then pac=pacman
fi
if [ -z "$pac" ]; then echo "Package-Management not found! !!!Only APT-GET, YUM and PACMAN are supported" && exit
fi
echo "Package-Management detected ---> $pac"
echo "----------Uninstalling OpenVPN----------"
if [ "$pac" = "pacman" ] ; then $pac -R openvpn easy-rsa --noconfirm
else
$pac remove OpenVPN easy-rsa -y
fi
rm -rf /etc/openvpn