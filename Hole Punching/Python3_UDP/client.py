import socket, sys, pickle, threading, time
import tkinter as tk


class Client():
    def __init__(self, master, ip, port):
        # GUI
        self.master = master
        master.title("Client")

        self.conn = tk.Button(self.master, height=1, width=50)
        self.conn.config(text="connect")
        self.conn.config(command=lambda: self.startSending())

        self.refresh = tk.Button(self.master,height=1, width=50)
        self.refresh.config(text="refresh")
        self.refresh.config(command=lambda: self.reload())

        self.variable = tk.StringVar()
        self.option = tk.OptionMenu(self.master, self.variable, "Bitte auswaehlen")
        self.option.config(width="50")

        self.text = tk.Entry(self.master,width="50")

        self.show = tk.Text(self.master, width="50")

        # LAYOUT
        self.conn.grid(row=0, column=0, sticky=tk.N)
        self.refresh.grid(row=0, column=1, sticky=tk.W)
        self.option.grid(row=1, column=1, sticky=tk.W)
        self.text.grid(row=2, column=0, sticky=tk.W)
        self.show.grid(row=2, column=1, sticky=tk.W)

        # NETWORKING
        self.SERV_IP = ip
        self.SERV_PORT = port
        self.logins = set()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Could not set up socket.")
            sys.exit(1)

        # connect to server
        self.connect()
        #first reload of clients
        self.reload()

    def updateMenu(self, logins):
        self.option['menu'].delete(0, 'end')

        for choice in logins:
            self.option['menu'].add_command(label=choice, command=tk._setit(self.variable, choice[0]))

    def connect(self):
        try:
            self.sock.sendto('L'.encode('utf-8'), (self.SERV_IP, self.SERV_PORT))
        except:
            print ("Could not send login.")
            sys.exit(1)

    def reload(self):
        try:
            self.sock.sendto('R'.encode('utf-8'), (self.SERV_IP, self.SERV_PORT))
        except:
            print ("Could not send refresh.")
            sys.exit(1)

        data, addr = self.sock.recvfrom(1024)
        self.logins = pickle.loads(data)
        self.updateMenu(self.logins)

    def send(self):
        ip = self.variable.get()
        port = None
        for i in self.logins:
            if ip == i[0]:
                port = i[1]
        while True:
            try:
                self.sock.sendto(self.text.get().encode('utf-8'), (ip, int(port)))
                time.sleep(1)
            except:
                print ("Could not send messages.")
                sys.exit(1)

    def receive(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                utf_data = data.decode('utf-8')
                self.show.insert(tk.END,"\n"+utf_data)
            except:
                print ("Could not receive messages.")
                sys.exit(1)


    def startSending(self):
        self.conn.config(state=tk.DISABLED)
        s = threading.Thread(target=lambda: self.send())
        r = threading.Thread(target=lambda: self.receive())
        s.start()
        r.start()

def main():
    root = tk.Tk()
    gui = Client(root, "10.14.87.18", 4567)
    threading.Thread(target=root.mainloop()).start()

if __name__ == '__main__':
    main()
