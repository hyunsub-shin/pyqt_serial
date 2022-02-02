import sys #, UI
from PyQt5.QtWidgets import *
from PyQt5 import uic

import serial
import serial.tools.list_ports as sp

from_class = uic.loadUiType("comport.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Puture Hansub")
        ## variables
        self.connection = False

        ## pushButton func
        self.pushButton_search.clicked.connect(self.serch_comport)
        self.pushButton_connect.clicked.connect(self.comport_connect)
        self.pushButton_disconnect.clicked.connect(self.comport_disconnect)
        self.pushButton_send.clicked.connect(self.tx_send)
        
    ## com port searching and list func
    def serch_comport(self):
        list = sp.comports()
        comport_list = []

        ## combobox list 중복추가 방지
        self.comboBox_comlist.clear()

        for i in list:
            comport_list.append(i.device)

        ## for debug -- print list
        print("COM port List: " + str(comport_list))
        ## com port list add to combobox
        self.comboBox_comlist.addItems(comport_list)

    ## com port connection func
    def comport_connect(self):
        try:
            ## com port connect to selected list # MS-Windows
            self.seri = serial.Serial(self.comboBox_comlist.currentText(), 115200, timeout=1)
            self.connection = True
            ## for debug -- print return value
            print("connect", self.comboBox_comlist.currentText(), self.connection, self.seri)
        except Exception as e:
            print(e)

    ## com port disconnection func
    def comport_disconnect(self):
        ## disconnect com port
        self.seri.close()
        self.connection = False
        ## for debug
        print("disconnect", self.comboBox_comlist.currentText(), self.connection, self.seri)

    ## TX button func
    def tx_send(self):
        ## for debug
        print("tx send")
        data = self.textEdit_tx.toPlainText()
        ## for debug -- print data
        print(data)
        self.seri.write(bytes(data, encoding='ascii'))


app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec()