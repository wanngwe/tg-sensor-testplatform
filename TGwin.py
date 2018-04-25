# -*- coding: utf-8 -*-

"""
Module implementing TGwin.
"""

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5 import QtCore, QtWidgets
from Ui_windos import Ui_Dialog

import globalvar as gl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

import matplotlib
global x
global showdegree
global calibration_value
global cali_flag
global degree
global degree1
cabliration_value=0.0
cali_flag=0
x=0
showdegree=[]
matplotlib.use("Qt5Agg")  # 声明使用QT

class Figure_Canvas(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键

    def __init__(self, parent=None, width=6, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)
        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        #self.axes1 = fig.add_subplot(212)
        self.axes.set_xlim(0, 100)
        self.axes.grid(True)
    def test(self, y):
        self.axes.plot(y, 'r')
        
class TGwin(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(TGwin, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.setInterval(500)
        
        self.timer.timeout.connect(self.timeout)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graphicsView = QtWidgets.QGraphicsView(self.online)
        self.graphicsView.setGeometry(QtCore.QRect(60, 260, 701, 292))
        self.graphicsView.setObjectName("graphicsView")
        self.dr = Figure_Canvas()
       #self.dr.test( 3)  # 画图
        
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(self.dr)
        self.graphicsView.setScene(graphicscene)
        self.graphicsView.show()
        
    def timeout(self):
        global degree
        global degree1
        global cabliration_value
        global cali_flag
        degree2=gl.get_db_handle()
        degree =float(degree2/1000)
        og_value=gl.get_mq_client()
        degree1=(og_value*0.0001);
        if(cali_flag):
            degree1=degree1-cabliration_value
            print(degree)
            

        #degree=degree2
        
        temp_d=int(degree)
        temp_m=((degree-temp_d)*60)
        temp_s=(temp_m-int(temp_m))*60
       

        temp_d1=int(degree1)                    
        temp_m1=((degree1-temp_d1)*60)
        temp_s1=(temp_m1-int(temp_m1))*60   
        self.lcdNumber.display(temp_d)
        self.lcdNumber_2.display(int(temp_m))
        self.lcdNumber_3.display(int(temp_s))
        
        self.lcdNumber_4.display(temp_d1)
        self.lcdNumber_5.display(int(temp_s1))
        
        #plot
        global showdegree
        showdegree.append(degree)

        
            
        self.dr.test(showdegree)
        self.dr.draw()
        if(len(showdegree)==100):
            showdegree.clear()
            self.dr.axes.clear()
            self.dr.axes.set_xlim(0, 100)
            self.dr.axes.grid(True)
    @pyqtSlot()
    def on_pushButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if(com.open()):
            self.timer.start()
            self.setWindowTitle('running')
        else:
            print('cant open')
    
    @pyqtSlot()
    def on_pushButton_2_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        com.stop()
        self.timer.stop()
        self.setWindowTitle('stopping')
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        global degree
        global degree1
        global cabliration_value
        global cali_flag
        cabliration_value=degree1-degree
        print(cabliration_value)
        cali_flag=1
    def on_pushButton_5_released(self):
        print("import")
        filename,  _ = QFileDialog.getOpenFileName(self, 'Open file',"./","Text Files (*.txt);;All Files (*)")
        if filename: 
            file = open(filename)  
            data = file.read()
            rows = data.split('\n')
            rows.pop()
            rows = list(map(int, rows))
            data=np.array(rows)
            x=data.reshape(int((len(data))/5),5)
            y1=x[:,2]
            y2=x[:,3]
            y=y1*20000+y2
            y=y*0.0001
            z=x[:,4]/1000
            error=y-z
            plt.subplot(221)
            plt.title(r'时栅角度曲线',fontproperties='SimHei',fontsize=20)
            plt.plot(z)
            plt.subplot(222)
            plt.title(r'光栅角度曲线',fontproperties='SimHei',fontsize=20)
            plt.plot(y, 'r')
            plt.subplot(223)
            plt.title(r'误差曲线',fontproperties='SimHei',fontsize=20)
            plt.plot(error, 'g')
            plt.show()
            
       

if __name__ == "__main__":
    import sys
    import serialport
    com=serialport.MyCom()
    app = QApplication(sys.argv)
    Dialog1 = TGwin()
    Dialog1.show()
    sys.exit(app.exec_())
