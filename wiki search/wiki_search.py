from PyQt5 import QtCore, QtGui, QtWidgets
import sqlalchemy
import pandas as pd
import requests
from sqlalchemy import create_engine
from bs4 import BeautifulSoup



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(770, 745)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TextArea = QtWidgets.QTextEdit(self.centralwidget)
        self.TextArea.setGeometry(QtCore.QRect(20, 140, 731, 551))
        self.TextArea.setObjectName("TextArea")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 120, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.title = QtWidgets.QLineEdit(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(20, 90, 731, 20))
        self.title.setObjectName("title")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.connectstring = QtWidgets.QLineEdit(self.centralwidget)
        self.connectstring.setGeometry(QtCore.QRect(20, 40, 731, 20))
        self.connectstring.setObjectName("connectstring")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 700, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.InsertData = QtWidgets.QPushButton(self.centralwidget)
        self.InsertData.setGeometry(QtCore.QRect(290, 700, 75, 23))
        self.InsertData.setObjectName("InsertData")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 770, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def dbconnect(self):
        global engine
        engine = create_engine('sqlite:///data.db', echo=True)

    def adddata(self):
        global data
        data = """ """
        Title = self.title.text()
        url = self.connectstring.text()
        response = requests.get(url)
        #response = requests.get('https://en.wikipedia.org/wiki/Computer')
        html = response.content
        soup = BeautifulSoup(html,'html.parser')
        title = soup.title.get_text()
        x = soup.find_all('p')
        for i in x:
            data = data + i.get_text() + '\n'
        df = pd.DataFrame({'title':[Title],'content' : [data] })
        df.to_sql(con=engine, name='wiki', if_exists='append')
        g = [data][0]
        self.TextArea.setPlainText(g)


    def data(self):

        try:
            Title = self.title.text()
            query = "select * from wiki where title = "+ '\"'+Title+'\"'
            dd = pd.read_sql_query(query,engine)
            xy = dd['content']
            self.TextArea.setPlainText(xy[0])
        except:
            global data
            data = """ """
            Title = self.title.text()
            term = "https://en.wikipedia.org/wiki/"+Title
            response = requests.get(term)
                    #response = requests.get('https://en.wikipedia.org/wiki/Computer')
            html = response.content
            soup = BeautifulSoup(html,'html.parser')
            title = soup.title.get_text()
            x = soup.find_all('p')
            for i in x:
                data = data + i.get_text() + '\n'
                df = pd.DataFrame({'title':[Title],'content' : [data] })
            g = [data][0]
            self.TextArea.setPlainText(g)
            df.to_sql(con=engine, name='wiki', if_exists='append')



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Text to DB"))
        self.label.setText(_translate("MainWindow", "Text"))
        self.label_2.setText(_translate("MainWindow", "Title"))
        self.label_3.setText(_translate("MainWindow", "URL To Fetch"))
        self.pushButton.setText(_translate("MainWindow", "Fetch Data"))
        self.InsertData.setText(_translate("MainWindow","Add Data"))
        self.pushButton.clicked.connect(self.dbconnect)
        self.InsertData.clicked.connect(self.dbconnect)
        self.pushButton.clicked.connect(self.data)
        self.InsertData.clicked.connect(self.adddata)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
