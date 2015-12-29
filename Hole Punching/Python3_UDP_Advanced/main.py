from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import socket
import widget
import pickle
import logging
import datetime


SERV_IP = "127.0.0.1"
SERV_PORT = 45678


class CThread(QThread):
    def __init__(self, socket, name):
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
            debug(self, "Login sent to Server")
        except:
            exception(self, "Could not send login")
            sys.exit(1)

    def connectToClient(self, partner):
        try:
            print ("send connection request to server")
            self.socket.sendto(('C'+';'+self.name + ';' +
                               partner)
                               .encode('utf-8'), self.SERV)
        except:
            print ("Could not send connect.")

    def agree(self, partner):
        print (partner)
        try:
            self.socket.sendto(('Y'+';'+self.name + ';' +
                               partner[0])
                               .encode('utf-8'), self.SERV)
        except:
            print ("Could not send connect.")

    def testFW(self, heuristic, ip, port):
        """
        0: received
        1: received+1
        2: received-1
        3: serveri
        """
        if heuristic not in (0, 1, 2, 3):
            return
        if heuristic is 0:
            partner = (ip, port)
        elif heuristic is 1:
            partner = (ip, port+1)
        elif heuristic is 2:
            partner = (ip, port-1)
        elif heuristic is 3:
            partner = self.SERV
        print ("sending X to ", partner)
        self.socket.sendto(('X'+';'+self.name + ';')
                           .encode('utf-8'), partner)



class ClientSender(QThread):
    def __init__(self, socket, name, partner, text):
        QThread.__init__(self)
        self.socket = socket
        self.partner = partner
        self.name = name
        self.text = text

    def stop(self):
        self.terminate()

    def changeText(self, text):
        self.text = text

    def run(self):
        while True:
            self.socket.sendto(('M'+';'+self.name + ';' + self.text)
                               .encode('utf-8'), self.partner)
            print ("sending ", self.text, "to", self.partner)
            self.sleep(2)


class RThread(QThread):
    def __init__(self, socket):
        QThread.__init__(self)
        self.SERV = (SERV_IP, SERV_PORT)
        self.socket = socket
        self.socket.settimeout(1)

    def __del__(self):
        self.wait()

    def run(self):
        answer = 0
        fw_test = 0
        timestamp = datetime.datetime.now()
        while True:
            try:
                if (answer == 0 and
                   (datetime.datetime.now()-timestamp).total_seconds() >= 3):
                    exception(self, "Server unreachable")
                    # Ugly exit
                    sys.exit(1)
                if (fw_test == 1 and
                   (datetime.datetime.now()-timestamp).total_seconds() >= 5):
                    # timeout for server connection
                   print ("gui")
                   self.emit(SIGNAL('testingFW(PyQt_PyObject)'), True)
                   fw_test = 0

                data, addr = self.socket.recvfrom(1024)
                host = addr[0]
                port = addr[1]
                receivedData = data.decode('utf-8').split(';')
                indicator = receivedData[0]

                if indicator is 'N':
                    answer = 1
                    self.emit(SIGNAL('showNamePresentDialog()'))
                elif indicator is 'R':
                    answer = 1
                    self.names = pickle.loads(receivedData[1]
                                              .encode('ISO-8859-1'))
                    self.emit(SIGNAL('add_names(PyQt_PyObject)'), self.names)
                elif indicator is 'C':
                    self.test = pickle.loads(receivedData[1]
                                             .encode('ISO-8859-1'))
                    print ("Partner received:", self.test[1], self.test[2])
                    self.emit(SIGNAL('cPartner(PyQt_PyObject)'), self.test)
                elif indicator is 'Q':
                    self.test = pickle.loads(receivedData[1]
                                             .encode('ISO-8859-1'))
                    debug(self, "Connection request from "+str(self.test))
                    self.emit(SIGNAL('showConnectionDialog(PyQt_PyObject)'),
                              (self.test[0], self.test[1], self.test[2]))
                elif indicator is 'S':
                    print ("S received")
                    timestamp = datetime.datetime.now()
                    fw_test = 1
                    self.emit(SIGNAL('testingFW(PyQt_PyObject)'), False)
                elif indicator is 'M':
                    # Absicherung Überprüfen ob richtige IP nötig
                    self.emit(SIGNAL('cText(QString)'), receivedData[2])
                elif indicator is 'X':
                    print ("X received from ", host, port)
                    # Absicherung Überprüfen ob richtige IP nötig
                    self.emit(SIGNAL('received(PyQt_PyObject)'),
                              (host, port))
                else:
                    print (indicator, receivedData[1])

            except socket.timeout:
                continue


class HeartbeatThread(QThread):
    def __init__(self, socket):
        QThread.__init__(self)
        self.SERV = (SERV_IP, SERV_PORT)
        self.socket = socket

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.socket.sendto(('H'+';').encode('utf-8'), (SERV_IP, SERV_PORT))
            self.sleep(10)


class ClientGui(QtGui.QWidget, widget.Ui_Widget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Logging
        filename = "logs/udpHP_"+datetime.datetime.now().strftime("%y-%m-%d-%H-%M")+".log"
        logging.basicConfig(filename=filename, level=logging.DEBUG)

        # disable buttons
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        # connect buttons
        self.pushButton_3.clicked.connect(self.connectToClient)
        self.pushButton_4.clicked.connect(self.connectToClient)
        debug(self, "Initial setup completed")

        # Name Dialog
        self.name = self.showNameDialog()
        debug(self, "Name: "+self.name)
        # Server Dialog
        global SERV_IP
        SERV_IP = self.showServerDialog()
        debug(self, "Server: "+SERV_IP)

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            exception(self, "Socket setup failed")
            sys.exit(1)
        debug(self, "Socket setup completed")

        # Controller
        self.controller = CThread(self.sock, self.name)
        debug(self, "ControllerThread setup completed")
        self.controller.connectToServer()
        self.connect(self.textBrowser_2,
                     SIGNAL("textChanged()"),
                     self.textChanged)

        # Receiver
        self.receiver = RThread(self.sock)
        debug(self, "ReceiverThread setup completed")
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
                     SIGNAL("testingFW(PyQt_PyObject)"),
                     self.testFW)
        self.connect(self.receiver,
                     SIGNAL("cText(QString)"),
                     self.changeTextBrowser)
        self.connect(self.receiver,
                     SIGNAL("cPartner(PyQt_PyObject)"),
                     self.changePartner)
        self.receiver.start()

        # Heartbeater
        self.heartbeater = HeartbeatThread(self.sock)
        debug(self, "HeartbeatThread setup completed")
        self.heartbeater.start()
        debug(self, "Heartbeater started")

        # ClientSender
        self.cs = None

        #Partner
        self.partner = None

    def newInit(self):
        # Name Dialog
        self.name = self.showNameDialog()

        # Server Dialog
        global SERV_IP
        SERV_IP = self.showServerDialog()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            sys.exit(1)

        # Controller
        self.controller = CThread(self.sock, self.name)
        self.controller.connectToServer()
        self.connect(self.textBrowser_2,
                     SIGNAL("textChanged()"),
                     self.textChanged)

        # Receiver
        self.receiver = RThread(self.sock)
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
                     SIGNAL("testingFW(PyQt_PyObject)"),
                     self.testFW)
        self.connect(self.receiver,
                     SIGNAL("cText(QString)"),
                     self.changeTextBrowser)
        self.connect(self.receiver,
                     SIGNAL("cPartner(PyQt_PyObject)"),
                     self.changePartner)
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
            debug(self, "Agreed to client connection")
            self.partner = partner
            self.controller.agree(partner)
        else:
            debug(self, "Client connection refused")

    def testFW(self, tested):
        if self.partner is None:
            return
        if self.cs is not None:
            self.pushButton_3.setEnabled(False)
            self.comboBox.setEnabled(False)
            return

        debug(self, "Connecting to "+str(self.partner))
        if not tested:
            for j in range(0, 2, 1):
                for i in range(0, 5, 1):
                    # if self.cs is not None:
                    #     print ("using:", self.cs.partner)
                    #     break
                    self.controller.testFW(j, self.partner[1], self.partner[2])
        else:
            self.controller.testFW(3, self.partner[1], self.partner[2])


    def received(self, partner):
        if self.cs is None:
            self.pushButton_3.setEnabled(False)
            self.comboBox.setEnabled(False)
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

    def changePartner(self, partner):
        self.partner = partner


def debug(obj, msg):
    logging.debug(('{0} \u0009 {1} \u0009 {2}').format(datetime.datetime.now(), type(obj).__name__, msg))

def exception(obj, msg):
    logging.error(('{0} \u0009 {1} \u0009 {2}').format(datetime.datetime.now(), type(obj).__name__, msg))
    logging.debug(('{0} \u0009 {1} \u0009 {2}').format(datetime.datetime.now(), type(obj).__name__, "Exiting..."))

def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    app.setWindowIcon(QtGui.QIcon('icon.png'))  # Set Window Icon
    app.setStyle('cleanlook')
    form = ClientGui()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':
    main()  # run the main function
