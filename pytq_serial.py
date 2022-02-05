from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer


app = QtWidgets.QApplication([])
ui = uic.loadUi("comport.ui")
ui.setWindowTitle("PyQt5 Serial Test")


## Used Serial port
serial = QSerialPort()
## Used Timer
timer = QTimer()


###############
## variables ##
###############
connection_state = None
baudrate = 115200


###############
## Fucntions ##
###############
## COM port listing
def search_comport():
    comport_list = []
    list = QSerialPortInfo().availablePorts()

    ## combobox list 중복추가 방지
    ui.comboBox_comlist.clear()

    for i in list:
        comport_list.append(i.portName())
        
    # add comport list to combobox
    ui.comboBox_comlist.addItems(comport_list)
    # for debug
    print("COM port List: " + str(comport_list))

## COM port open
def comport_connect():
    try:
        ## com port connect to selected list # MS-Windows
        global baudrate
        serial.setBaudRate(baudrate)
        serial.setPortName(ui.comboBox_comlist.currentText())
        ## for Debug
        print("baudrate : ", baudrate)

        global connection_state # Used global variable
        if connection_state == True: 
            ui.status_label2.setText("comport already connect")
            ## for debug
            print("comport already connect")  
            ## timer start
            timer.setInterval(3000)
            timer.start()
        else:
            connection_state = serial.open(QIODevice.ReadWrite)  
            if connection_state:
                ui.status_label1.setText("Connect")
                ## for debug
                print("connect", ui.comboBox_comlist.currentText(), connection_state, serial)
                                          
    except Exception as e:
        print(e)

## COM port close
def comport_disconnect(self):
    ## disconnect com port
    global connection_state # Used global variable
    connection_state = serial.close()    
    
    ui.status_label1.setText("Disconnect")
    ui.status_label2.setText("-")    
    ## for debug
    print("disconnect", ui.comboBox_comlist.currentText(), connection_state, serial)

## serial trasmmit
def tx_send():
    global connection_state # Used global variable
    if connection_state == True:        
        data = ui.textEdit_tx.toPlainText()
        # data = ui.lineEdit_tx.text()
        data += '\r'
        print(data)

        ## Serial data Write
        serial.write(str(data).encode())#, encoding='ascii'))
        # serial.writeData(bytes(data, encoding='ascii'))

        # ui.textEdit_tx.clear()
        
        ## for debug
        print("tx send")
        print(bytes(data, encoding='ascii'))        
    else:
        ui.status_label2.setText("comport Not open!!!")
        ## for debug
        print("comport Not open!!!")
        ## timer start
        timer.setInterval(3000)
        timer.start()

## serial receive
def rx_rcv():
    # rx = serial.readLine()
    rx = serial.readAll()
    ui.textEdit_rx.insertPlainText(str(rx, 'utf-8', 'replace'))
    # ui.textEdit_rx.setText(rx_data.decode()[:len(rx_data)])
    # ui.textEdit_rx.append("{}".format(rx))

    ## for Debug
    rx_data = str(rx, 'utf-8')#.rstrip(b'\r')#.strip()#
    print("rx_data--\n", rx_data)

## receive view clear
def rx_clear():
    ui.textEdit_rx.clear()

## if timeout, timer stop
def timeout():
    ui.status_label2.setText("-")
    timer.stop()


###################
## Event connect ##
###################
timer.timeout.connect(timeout)
serial.readyRead.connect(rx_rcv)
ui.pushButton_search.clicked.connect(search_comport)
ui.pushButton_connect.clicked.connect(comport_connect)
ui.pushButton_disconnect.clicked.connect(comport_disconnect)
ui.pushButton_send.clicked.connect(tx_send)
ui.pushButton_clear.clicked.connect(rx_clear)


ui.show()
app.exec()
