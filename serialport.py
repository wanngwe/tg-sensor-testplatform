import threading
import time
import serial
import binascii
import numpy as np
import Queue
f = open("model_Weight.txt",'a') 
class ComThread:
    def __init__(self, Port='COM3'):
        self.tg_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = Port
    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
        self.alive = False
        self.stop()

    def start(self):
        self.tg_serial = serial.Serial()
        self.tg_serial.port = self.port
        self.tg_serial.baudrate = 115200
        self.tg_serial.timeout = 2
        self.tg_serial.open()
        if self.tg_serial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True
            self.thread_read = None
            self.thread_read = threading.Thread(target=self.FirstReader)
            self.thread_read.setDaemon(1)
            self.thread_read.start()
            return True
        else:
            return False

    def SendDate(self,i_msg,send):
        lmsg = ''
        isOK = False
        if isinstance(i_msg):
            lmsg = i_msg.encode('gb18030')
        else:
            lmsg = i_msg
        try:
            # 发送数据到相应的处理组件
            self.l_serial.write(send)
        except Exception as ex:
            pass;
        return isOK

    def FirstReader(self):
        while self.alive:
            time.sleep(0.1)
            data = ''
            data = data.encode('utf-8')

            n = self.tg_serial.inWaiting()
            if n:
                 data = data + self.tg_serial.read(n)
                 print(n)
                 high=data[::2]
                 low =data[1::2]            
                 d=[(high[i]<<8)+low[i] for i in range(len(low))]
                 d=np.array(d,dtype='int16')
                 for i in range(len(d)):
                 	f.write(str(d[i]))            #将字符串写入文件中
                 	f.write("\n")                 #换行  
        
        self.waitEnd.set()
        self.alive = False

    def stop(self):
        self.alive = False
        self.thread_read.join()
        if self.tg_serial.isOpen():
            self.tg_serial.close()
global rt
rt=ComThread()
def openport():
	try:
		if rt.start():
			print(rt.tg_serial.name)
			#rt.waiting()
			pass
		else:
			pass
	except Exception as se:
		print(str(se))
def closeport():
	print('close' )
	global rt
	print(rt.tg_serial.name)
	rt.stop()
	f.close()

#调用串口，测试串口
def main():
    rt = ComThread()
    try:
        if  rt.start():
            #print(rt.tg_serial.name)
            rt.waiting()
            rt.stop()
        else:
            pass
    except Exception as se:
        print(str(se))

    if rt.alive:
        rt.stop()
    print ('End OK')
    del rt








# data process


if __name__ == '__main__':

    #设置一个主函数，用来运行窗口，便于若其他地方下需要调用串口是可以直接调用main函数
    main()
    #closeport()