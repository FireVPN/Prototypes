from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import socket
import widget
import pickle


SERV_IP = "127.0.0.1"
SERV_PORT = 4567


class ControllerThread(QThread):
    def __init__(self, socket, name):
        """
        Make a new thread instance Controller.
        """
        QThread.__init__(self)
        self.SERV = (SERV_IP, SERV_PORT)
        self.socket = socket
        self.name = name

    def __del__(self):
        self.socket.sendto(('E'+';'+self.name).encode('utf-8'), self.SERV)
        self.wait()

    def connectToServer(self):
        try:
            self.socket.sendto(('L'+';'+self.name).encode('utf-8'), self.SERV)
        except:
            print ("Could not send login.")
            sys.exit(1)

    def connectToClient(self, partner):
        try:
            print ("send connection request to server")
            self.socket.sendto(('C'+';'+self.name + ';' +
                               partner)
                               .encode('utf-8'), self.SERV)
        except:
            print ("Could not send connect.")

    def testFW(self, heuristic, ip, port):
        """
        0: received
        1: received+1
        2: received+2
        3: server
        """
        if heuristic not in (0, 1, 2, 3):
            return
        if heuristic is 0:
            # try ip+port as received
            partner = (ip, port)
        elif heuristic is 1:
            # try ip+port+1 as received
            partner = (ip, port+1)
        elif heuristic is 2:
            # try ip+port-1 as received
            partner = (ip, port-1)
        elif heuristic is 3:
            # try ip+port as received
            partner = self.SERV
        print ("testFW:", partner)
        for i in range(0, 5, 1):
            self.socket.sendto(('X'+';'+self.name + ';')
                               .encode('utf-8'), partner)
        self.sleep(2)


class ClientSender(QThread):
    def __init__(self, socket, name, partner, text):
        QThread.__init__(self)
        self.socket = socket
        self.partner = partner
        self.name = name
        self.text = text
        print (self.text)

    def stop(self):
        self.terminate()

    def changeText(self, text):
        self.text = text

    def run(self):
        while True:
            self.socket.sendto(('M'+';'+self.name + ';' + self.text)
                               .encode('utf-8'), self.partner)
            self.sleep(2)


class ReceiverThread(QThread):
    def __init__(self, socket):
        """
        Make a new thread instance Receiver.
        """
        QThread.__init__(self)
        self.SERV = (SERV_IP, SERV_PORT)
        self.socket = socket
        self.socket.settimeout(1)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                host = addr[0]
                port = addr[1]
                receivedData = data.decode('utf-8').split(';')
                indicator = receivedData[0]

                if indicator is 'N':
                    print ("Nickname already present.")
                    self.emit(SIGNAL('showNamePresentDialog()'))
                elif indicator is 'R':
                    self.names = pickle.loads(receivedData[1]
                                              .encode('ISO-8859-1'))
                    self.emit(SIGNAL('add_names(PyQt_PyObject)'), self.names)
                elif indicator is 'C':
                    self.test = pickle.loads(receivedData[1]
                                             .encode('ISO-8859-1'))
                    print ("Partner received:", self.test[1], self.test[2])
                    self.sleep(5)
                    self.emit(SIGNAL('startTestingFW(PyQt_PyObject)'),
                              (self.test[1], self.test[2]))
                elif indicator is 'Q':
                    print ("got connection request from Server")
                    self.test = pickle.loads(receivedData[1]
                                             .encode('ISO-8859-1'))
                    self.emit(SIGNAL('showConnectionDialog(PyQt_PyObject)'),
                              (self.test[1], self.test[2]))
                elif indicator is 'M':
                    # Absicherung Überprüfen ob richtige IP nötig

                    self.emit(SIGNAL('cText(QString)'), receivedData[2])
                elif indicator is 'X':
                    # Absicherung Überprüfen ob richtige IP nötig
                    self.emit(SIGNAL('received(PyQt_PyObject)'),
                              (host, port))
                else:
                    print (indicator, receivedData[1])
            except socket.timeout:
                continue


class HeartbeatThread(QThread):
    def __init__(self, socket):
        """
        Make a new thread instance Hearbeater.
        """
        QThread.__init__(self)
        self.SERV = (SERV_IP, SERV_PORT)
        self.socket = socket

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.socket.sendto(('H'+';').encode('utf-8'), (SERV_IP, SERV_PORT))
            self.sleep(10)


class Client(QtGui.QWidget, widget.Ui_Widget):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        # Connect the Signal
        self.pushButton_3.clicked.connect(self.connectToClient)
        # for the Connect Button

        # disable buttons
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        # Name Dialog
        self.name = self.showNameDialog()

        # Server
        # global SERV_IP
        # SERV_IP = self.showServerDialog()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Could not set up socket.")
            sys.exit(1)

        # Controller
        self.controller = ControllerThread(self.sock, self.name)
        self.controller.connectToServer()
        self.connect(self.textBrowser_2,
                     SIGNAL("textChanged()"),
                     self.textChanged)

        # Receiver
        self.receiver = ReceiverThread(self.sock)
        self.connect(self.receiver,
                     SIGNAL("add_names(PyQt_PyObject)"),
                     self.add_names)
        self.connect(self.receiver, SIGNAL("showNamePresentDialog()"),
                     self.showNamePresentDialog)
        self.connect(self.receiver,
                     SIGNAL("showConnectionDialog(PyQt_PyObject)"),
                     self.showConnectionDialog)
        self.connect(self.receiver,
                     SIGNAL("received(PyQt_PyObject)"),
                     self.received)
        self.connect(self.receiver,
                     SIGNAL("startTestingFW(PyQt_PyObject)"),
                     self.startTestingFW)
        self.connect(self.receiver,
                     SIGNAL("cText(QString)"),
                     self.changeTextBrowser)
        self.receiver.start()
        # Heartbeater
        self.heartbeater = HeartbeatThread(self.sock)
        self.heartbeater.start()

        # ClientSender
        self.cs = None

    def newInit(self):
        # Name Dialog
        self.name = self.showNameDialog()

        # Controller
        self.controller = ControllerThread(self.sock, self.name)
        self.controller.connectToServer()

        # Receiver
        self.receiver = ReceiverThread(self.sock)
        self.connect(self.receiver,
                     SIGNAL("add_names(PyQt_PyObject)"),
                     self.add_names)
        self.connect(self.receiver, SIGNAL("showNamePresentDialog()"),
                     self.showNamePresentDialog)
        self.connect(self.receiver,
                     SIGNAL("showConnectionDialog(PyQt_PyObject)"),
                     self.showConnectionDialog)
        self.connect(self.receiver,
                     SIGNAL("startTestingFW(PyQt_PyObject)"),
                     self.startTestingFW)
        self.receiver.start()
        # Heartbeater
        self.heartbeater = HeartbeatThread(self.sock)
        self.heartbeater.start()

        # ClientSender
        self.cs = None

    def connectToClient(self):
        self.controller.connectToClient(self.comboBox.currentText())

    def add_names(self, names):
        self.comboBox.clear()
        if len(names) > 0:
            for n in names:
                self.comboBox.addItem(n)
            self.pushButton_3.setEnabled(True)
            self.comboBox.setEnabled(True)
        else:
            self.comboBox.addItem("Keine User online.")
            self.pushButton_3.setEnabled(False)
            self.comboBox.setEnabled(False)

    def showNameDialog(self):
        text, ok = QtGui.QInputDialog.getText(self,
                                              'UDP Hole Puncher NG',
                                              'Geben Sie einen Nicknamen ein:')
        if not ok:
            sys.exit()
        return text

    def showServerDialog(self):
        text, ok = QtGui.QInputDialog.getText(self,
                                              'UDP Hole Puncher NG',
                                              'Geben Sie den Server an:')
        if not ok:
            sys.exit()
        return text

    def showNamePresentDialog(self):
        reply = QtGui.QMessageBox.question(self, 'UDP Hole Puncher NG',
                                           'Der Nickname ist leider'
                                           ' schon vergeben! Wollen Sie einen'
                                           ' Neuen wählen oder Beenden?',
                                           'Neu',
                                           'Beenden')
        if reply == 0:
            self.newInit()
        else:
            self.controller.__del__()
            sys.exit()

    def showConnectionDialog(self, partner):
        msg = "Der Client " + partner[0]
        msg += " möchte eine Verbindung aufbauen. Akzeptieren?"
        reply = QtGui.QMessageBox.question(self, 'UDP Hole Puncher NG',
                                           msg,
                                           "Annehmen",
                                           "Ablehnen")

        if reply == 0:
            print ("Connection to client starts")
            self.startTestingFW(partner)
        else:
            print ("Verbindung wird abgebrochen")

    def startTestingFW(self, partner):
        print ("Verbindung zu", partner, "wird aufgebaut")
        for i in range(0, 3, 1):
            if self.cs is not None:
                print ("using:", self.cs.partner)
                break
            self.controller.testFW(i, partner[0], partner[1])
        self.pushButton_3.setEnabled(False)
        self.comboBox.setEnabled(False)

    def received(self, partner):
        if self.cs is None:
            print ("set up clientsender")
            self.cs = ClientSender(self.sock, self.name, partner,
                                   self.textBrowser_2.toPlainText())
            self.connect(self.textBrowser_3, SIGNAL("textChanged(QString)"),
                         self.cs.changeText)
            self.startConnectionToClient()

    def startConnectionToClient(self):
        self.cs.start()

    def textChanged(self):
        if self.cs is not None:
            self.cs.changeText(self.textBrowser_2.toPlainText())

    def changeTextBrowser(self, text):
        self.textBrowser_3.append(text)


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    app.setWindowIcon(QtGui.QIcon('icon.png'))  # Set Window Icon
    form = Client()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':
    main()  # run the main function
