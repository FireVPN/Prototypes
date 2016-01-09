from subprocess import Popen
p = Popen(["C:\\Users\\User\\FireVPN\\FireVPN-install.bat", "server"], bufsize=0)
stdout, stderr = p.communicate()