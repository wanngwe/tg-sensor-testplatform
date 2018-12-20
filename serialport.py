import serial
import numpy as np
import queue
global q
global og_value
global degree
databuf=np.array([],dtype='int16')
teststart_flag=0

q = queue.Queue(512)
f_degree=open("degree.txt",'w+')


def drawPic(data,data1,data2,data3):         
    #清空图像，以使得前后两次绘制的图像不会重叠  
    drawPic.f.clf()  
    drawPic.a=drawPic.f.add_subplot(211)
    drawPic.b=drawPic.f.add_subplot(212)  

    drawPic.canvas.draw()

    
class MyCom:
    def __init__(self, Port='COM4'):
        self.tg_serial                  = None
        self.alive                       = False
        self.port                        = Port
        self.onlinetxt                  =None
        self.offlinetxt                  =None
        self.c1                          =None
        self.c2                          =None
        self.c3                          =None
        self.dir                          =''

    def open(self):
        self.tg_serial = serial.Serial(self.port, 115200)
        self.onlinetxt                  =open('online_analysis.txt','w+', newline='')
        self.offlinetxt                  =open('offline_analysis.txt','w+', newline='')
        self.c1 =open('c1.txt', 'w+')
        self.c2 =open('c2.txt', 'w+')
        self.c3 =open('c3.txt', 'w+')
        self.alive = True
    def changedir(self, dir):
         self.dir=dir

    def reciveData(self):
        data = ''
        mode=0
        og_value=0
        degree=0
        data = data.encode('utf-8')
        rec_len = self.tg_serial.inWaiting()
        if rec_len:
            data = data + self.tg_serial.read(rec_len)
            low = data[::2]
            high = data[1::2]
            d = [(high[i] << 8)+low[i] for i in range(len(low))]
            for i in range(len(d)-1):
                print(d[0])
                if (d[i]==32767 and d[i+1]==32767):
                    mode =1
                    break
                if(d[i]==32766 and d[i+1]==32766):
                    mode =2
                    break
                if (d[i]==32765 and d[i+1]==32765):
                    mode =3
                    break
                if (d[i]==32764 and d[i+1]==32764):
                    mode =4
                    break
                if (d[i]==32763 and d[i+1]==32763):
                    mode =5
                    break                    
        if(mode ==1):
            og_value  =d[i+2]*20000+d[i+3]
            degree     =d[i+4]*20000+d[i+5]
            d = np.array(d, dtype='int32')
            d =d.reshape((int)(len(d)/8), 8)
            opticalEncoder =d[:,2]*20000+d[:,3]
            sensor_1        =d[:,4]*20000+d[:,5]
            sensor_2        =d[:,6]*20000+d[:,7]
            opticalEncoder=opticalEncoder.reshape((int)(len(d)),1)
            #opticalEncoder=opticalEncoder*0.36
           # opticalEncoder = np.array(opticalEncoder, dtype='uint32')
            sensor_1        =sensor_1.reshape((int)(len(d)),1)
            sensor_2        =sensor_2.reshape((int)(len(d)),1)
            C                  = np.hstack((opticalEncoder, sensor_1, sensor_2)) 
            for i in range((int)(len(d))):
                savestr=str(C[i, 0])+'\t'+str(C[i, 1])+'\t'+str(C[i, 2])+'\n'
                self.onlinetxt.write(savestr) 
        if(mode ==2):
            d = np.array(d, dtype='int16')
           # s1=d
            for i in range(len(d)):
                self.c1.write(str(d[i]))  
                self.c1.write("\n")
        if(mode ==3):
            
            d = np.array(d, dtype='int16')
            for i in range(len(d)):
                self.c2.write(str(d[i]))  
                self.c2.write("\n")
        if(mode ==4):                
            d = np.array(d, dtype='int16')              
            for i in range(len(d)):
                self.c3.write(str(d[i]))  
                self.c3.write("\n")
            
        if(mode ==5):
            print('offline')
            d = np.array(d, dtype='int16')
            for i in range((int)(len(d))):
                savestr=str(d[i])+'\n'
                self.offlinetxt.write(savestr) 
        if(mode ==3 or mode==4):
            return og_value,degree,True
        else:
            return og_value,degree,False
        
    def send(self,data):
        atCmdStr=data
        
        self.tg_serial.write(atCmdStr.encode('utf-8'))

    def stop(self):
        self.tg_serial.close()
        print("com3 has been closed!")
        self.onlinetxt.close()
        self.c1.close()
        self.c2.close()
        self.c3.close()
        


global rt
rt = MyCom()
# 调用串口，测试串口


def main():
    pass

# data process

if __name__ == '__main__': 
    main()
