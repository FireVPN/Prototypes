from subprocess import Popen
p = Popen(["/home/programmierer/FireVPN/FireVPN/FireVPN-install.sh", "server"], bufsize=0)
stdout, stderr = p.communicate()