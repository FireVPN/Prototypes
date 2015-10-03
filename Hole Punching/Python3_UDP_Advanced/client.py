from PyQt4 import QtCore, QtGui
import sys, socket, threading, time

SERV_IP = "127.0.0.1"
SERV_PORT = 4567

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class View(QtGui.QWidget):
    sigConnect = QtCore.pyqtSignal()
    sigDisconnect = QtCore.pyqtSignal()
    sigRefresh = QtCore.pyqtSignal()
    sigExit = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName(_fromUtf8("Widget"))
        Widget.resize(538, 301)
        self.verticalLayout = QtGui.QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButton_3 = QtGui.QPushButton(Widget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(Widget)
        self.pushButton_4.setEnabled(True)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.pushButton = QtGui.QPushButton(Widget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.textBrowser_2 = QtGui.QTextEdit(Widget)
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.gridLayout.addWidget(self.textBrowser_2, 1, 0, 1, 1)
        self.textBrowser_3 = QtGui.QTextBrowser(Widget)
        self.textBrowser_3.setObjectName(_fromUtf8("textBrowser_3"))
        self.gridLayout.addWidget(self.textBrowser_3, 1, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(Widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(_translate("Widget", "UDP Hole Puncher NG", None))
        self.pushButton_3.setText(_translate("Widget", "Connect", None))
        self.pushButton_4.setText(_translate("Widget", "Disconnect", None))
        self.pushButton.setText(_translate("Widget", "Refresh", None))
        self.pushButton_3.clicked.connect(lambda x: self.sigConnect.emit())
        self.pushButton_4.clicked.connect(lambda x: self.sigDisconnect.emit())
        self.pushButton.clicked.connect(lambda x: self.sigRefresh.emit())

    def showNameDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'UDP Hole Puncher NG',
            'Geben Sie einen Nicknamen ein:')

        if ok:
            return str(text)

class Heartbeater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Could not set up socket.")
            sys.exit(1)

    def run(self):
        while not self.event.is_set():
            self.sock.sendto(('H'+';').encode('utf-8'), (SERV_IP, SERV_PORT))
            self.event.wait(10)
            #print(time.time())

    def stop(self):
        self.event.set()


class Controller:
    def __init__(self, view, hb):
        #View and Heartbeater
        self.view = view
        self.hb = hb

        #Networking
        self.SERV = (SERV_IP, SERV_PORT)
        self.logins = set()

        # Connect all signals from view with according handlers
        self.view.sigConnect.connect(self.connect)
        self.view.sigDisconnect.connect(self.disconnect)
        self.view.sigRefresh.connect(self.refresh)
        self.view.sigExit.connect(self.exit)
        self.nickname = self.view.showNameDialog()
        print("Deine Nickname: ", self.nickname)

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Could not set up socket.")
            sys.exit(1)

        self.connectToServer()

    def connect(self):
        print("pushed connect-button")

    def connectToServer(self):
        try:
            self.sock.sendto(('L'+';'+self.nickname).encode('utf-8'), self.SERV)
            self.hb.start()
        except:
            print ("Could not send login.")
            self.exit()
            sys.exit(1)

    def disconnect(self):
        print("pushed disconnect-button")

    def refresh(self):
        print("pushed refresh-button")

    def exit(self):
        self.sock.sendto(('E'+';'+self.nickname).encode('utf-8'), self.SERV)
        self.hb.stop()
        self.sock.close()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    view = View()
    hb = Heartbeater()
    controller = Controller(view, hb)

    app.aboutToQuit.connect(view.sigExit)
    view.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

