# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from scipy import optimize
import time
from Ui_windos import Ui_Dialog

showdegree=[]
OGselect=False
TGselect=False
def fmax(x,a,b,c):
    return a*np.sin(x*0.06285*2+b)+c
class Figure_Canvas(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键
    def __init__(self, parent=None, width=8, height=4, dpi=300):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)
        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        #self.axes1 = fig.add_subplot(212)
        self.axes.set_xlim(0, 100)
        self.axes.grid(True)
    def test(self, y):
        self.axes.plot(y, 'r')

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        
        #设置定时器接收数据
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        
        #设置波形显示画布
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        #将画布嵌入到freq
        self.graphicsView = QtWidgets.QGraphicsView(self.freq)
        self.graphicsView.setGeometry(QtCore.QRect(30, 260, 751, 402))
        self.graphicsView.setObjectName("graphicsView")
        self.dr = Figure_Canvas()
       #self.dr.test( 3)  # 画图
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(self.dr)
        self.graphicsView.setScene(graphicscene)
        self.graphicsView.show()
    def timeout(self):
        
        ret=com.reciveData()
        print(ret)
        sensor=ret[1]/10
        optical_encoder=ret[0]*0.36
        self.dgreedislay(sensor,optical_encoder)
    @pyqtSlot()
    def dgreedislay(self, degree, degree1):
        temp_d=int(degree/3600)
        temp_m=int((degree%3600)/60)        
        temp_s=((degree%3600)%60)       
        temp_d1=int(degree1/3600) 
        temp_m1=int((degree1%3600)/60)       
        temp_s1=((degree1%3600)%60)  
        self.lcdNumber.display(temp_d)
        self.lcdNumber_2.display(int(temp_m))
        self.lcdNumber_3.display(int(temp_s))        
        self.lcdNumber_4.display(temp_d1)
        self.lcdNumber_5.display(int(temp_m1))
        self.lcdNumber_6.display(int(temp_s1))
        showdegree.append(degree-degree1)
        self.dr.test(showdegree)
        self.dr.draw()
        if(len(showdegree)==100):
            showdegree.clear()
            self.dr.axes.clear()
            self.dr.axes.set_xlim(0, 100)
            self.dr.axes.grid(True)
    def on_FFTButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    @pyqtSlot()
    def on_start_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print('hello')
        com.open()
        com.send('a2')
        self.timer.start()    
    @pyqtSlot()
    def on_closeee_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        com.send('a4')
        com.stop()
        self.timer.stop()    
    @pyqtSlot()
    def on_stabilityButton_released(self):
        """
        Slot documentation goes here.
        """
        print('hello')
        com.open()
        com.send('a2')
        self.timer.start()
        time.sleep(5)
        com.send('a4')
        com.stop()
        self.timer.stop()
        
        # TODO: not implemented yet
    @pyqtSlot()
    def on_ImportButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        data=[]
        filename, filetype=QFileDialog.getOpenFileName(self, "选择文件","./")
        print(filename)
        with open(filename) as f:
            for  line in f:
                data.append(line.rstrip())
#        print(data[2:10000:6])
#        low = data[2::6]
#        high = data[3::6]
#        og=high*20000+low
#        low = data[2::6]
#        high = data[3::6]
#        tg=high*20000+low   
#        plt.plot(og[:6000],'r')
#        plt.show()
  
       
        
        
    @pyqtSlot()
    def on_SampleButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        com.open()
        com.send('a1')
        self.timer.start()
        self.setWindowTitle('running')
    
    
    @pyqtSlot()
    #下发停止命令
    def on_StopButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        com.send('a4')
        com.stop()
        self.timer.stop()
        self.setWindowTitle('stopping')
    @pyqtSlot()
    #下发校准命令
    def on_CabButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        global OGselect, TGselect
        data1=[]
        data2=[]
        data3=[]
        
        com.open()
        if(OGselect):
            com.send('a6')
            print('send a6')
        if(TGselect):
            com.send('a3')
            print('send a3')
        #QMessageBox.information()
        time_start=0
        time_end=0
        timelaps=0
        time_start=time.time()
        self.setWindowTitle('cabliration.......')
        while (1):           
            ret=com.reciveData()
            time_end=time.time()
            timelaps=time_end-time_start
            time.sleep(0.5)
            print(timelaps)
            print(ret)
            if(ret[2]==True or timelaps>10):
                break;
        if(ret[2]==True):
            self.setWindowTitle('cabliration has done.......')
            com.stop()
            with open('c1.txt') as f:
                for  line in f:
                    data1.append(line.rstrip())
            for index,item in enumerate(data1):
                data1[index]=int(item)


            induce=data1[7::2]
            with open('c2.txt') as f:
                for  line in f:
                    data2.append(line.rstrip())
            for index,item in enumerate(data2):
                data2[index]=int(item)


            induce2=data2[7::2]
            x1=np.arange(0,128,1)
            induce=np.array(induce)
            induce2=np.array(induce2)
            fita, fitb =optimize.curve_fit(fmax,x1,(induce[:128]+induce2[:128])/2,[1,1,1])
            com.open()
            com.send('aa'+str(fita[0]))
            com.send('ab'+str(fita[1]))
            com.send('ac'+str(fita[2]))
            while (1):           
                ret=com.reciveData()
                if(ret[2]==True):
                    break
            com.stop()
            with open('c3.txt') as f:
                for  line in f:
                    data3.append(line.rstrip())
            for index,item in enumerate(data3):
                data3[index]=int(item)   
            comp=data3[2::1]
            print(comp)
            print("ssss")
            plt.plot(comp[:127])
            
            plt.plot(induce2,'r')
            plt.plot(induce,'g')
            
            plt.plot((induce+induce2)/2)
          #  plt.plot(x1,fmax(x1,fita[0],fita[1],fita[2]))
         #   plt.plot(x1,fmax(x1,fita[0],fita[1]%6.28,fita[2]))
            plt.show()
 
            com.stop()
            self.ampEdit.setText(str(fita[0]))
            self.phaseEdit.setText(str(fita[1]%6.28))
            self.offsetEdit.setText(str(fita[2]))
            QMessageBox.information(self, "Tips", "calibration OK!!!", QMessageBox.Yes)
    
        else:
            com.stop()
            QMessageBox.information(self, "Tips", "calibration faiure!!!", QMessageBox.Yes)
    
    @pyqtSlot()
    def on_SetDirButton_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        dir=QFileDialog.getExistingDirectory(self, "选择文件","./")
        print(dir)
        com.changedir(dir)
    @pyqtSlot(bool)
    def on_radioButton_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        print('1')

        global TGselect
        TGselect=checked
        print(TGselect)
    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, checked):
        """
        Slot documentation goes here.        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        print('2')
        global OGselect
        OGselect=checked
        print(OGselect)       
if __name__ == "__main__":
    import sys
    import serialport
    com=serialport.MyCom()
   
    app = QApplication(sys.argv)
    Dialog1 = Dialog()
    Dialog1.show()
    sys.exit(app.exec_())
