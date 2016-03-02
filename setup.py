__author__ = 'Elias Eckenfellner'
from sys import platform as _platform
from subprocess import check_output
import subprocess
import urllib.request
import sys
if _platform == "linux" or _platform == "linux2":
    subprocess.call(["apt-get", "install", "openvpn", "easy-rsa", "python3-pyqt4", "-y"])
elif _platform == "win32":
    print("PyQT wird heruntergeladen...")
    if(sys.maxsize > 2**32):
        print("64Bit-Version wird heruntergeladen...")
        urllib.request.urlretrieve("http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py3.4-Qt4.8.7-x64.exe", "installer.exe")
    else:
        print("32Bit-Version wird heruntergeladen...")
        urllib.request.urlretrieve("http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py3.4-Qt4.8.7-x32.exe", "installer.exe")
    print("PyQT wird installiert...")
    check_output("installer.exe /S", shell=True)
    check_output("del installer.exe /S", shell=True)
    print("OpenVPN wird heruntergeladen...")
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    request=urllib.request.Request("http://www.openvpn.net/release/openvpn-2.1.3-install.exe",None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    with open("installer.exe", "wb") as installer:
        installer.write(data)
    print("OpenVPN wird installiert...")
    check_output("installer.exe /SELECT_OPENSSL_UTILITIES=1 /SELECT_EASYRSA=1 /S", shell=True)
    check_output("del installer.exe /S", shell=True)
    print("Installation abgeschlossen!")
