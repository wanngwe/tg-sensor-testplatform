import threading
import time
import serial
import binascii
import numpy as np
import queue
import itertools
import matplotlib.pyplot as plt
import matplotlib  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
from matplotlib.figure import Figure 
import math 
global q
global teststart_flag
global databuf
import globalvar as gl
databuf=np.array([],dtype='int16')
teststart_flag=0

q = queue.Queue(512)
ff = open("model_Weight.txt", 'a')
gl._init()
gl.set_value('tg_value', '0')

def drawPic(data,data1,data2,data3):         
    #清空图像，以使得前后两次绘制的图像不会重叠  
    drawPic.f.clf()  
    drawPic.a=drawPic.f.add_subplot(211)
    drawPic.b=drawPic.f.add_subplot(212)  
         
    #在[0,100]范围内随机生成sampleCount个数据点  
    # x=np.random.randint(0,100,size=sampleCount)  
    # y=np.random.randint(0,100,size=sampleCount)  
    # color=['b','r','y','g']  
         
    #绘制这些随机点的散点图，颜色随机选取  
    # drawPic.a.scatter(x,y,s=3,color=color[np.random.randint(len(color))])  
    drawPic.a.set_title('sensor output: vef wave and travlling wave')
    drawPic.a.plot(data[:50],color='green')
    drawPic.a.plot(data1[:50],color='red')

    drawPic.b.set_title('calcuation result: phase diff')
    #drawPic.b.plot(data2,color='green')
    drawPic.b.plot(data3[:60],color='yellow')

    drawPic.canvas.draw()
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

    def SendDate(self, i_msg, send):
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
            pass
        return isOK

    def FirstReader(self):
        while self.alive:
            time.sleep(0.1)
            data = ''
            data = data.encode('utf-8')

            n = self.tg_serial.inWaiting()
            if n:
                data = data + self.tg_serial.read(n)
                # print(n)
                high = data[::2]
                low = data[1::2]
                d = [(high[i] << 8)+low[i] for i in range(len(low))]
                d = np.array(d, dtype='int16')
                global teststart_flag
                if teststart_flag:
                    q.put(d)
                    # for i in range(len(d)):
                    #     q.put(d[i])
                # while not q.empty():
                #     next_item = q.get()
                #     print(next_item)
                        # f.write(str(d[i]))  # 将字符串写入文件中
                        # f.write("\n")  # 换行

        self.waitEnd.set()
        self.alive = False

    def stop(self):
        self.alive = False
        self.thread_read.join()
        if self.tg_serial.isOpen():
            self.tg_serial.close()


global rt
global worker
rt = ComThread()


def openport():
  
    try:
        if rt.start():
            print(rt.tg_serial.name)
            # rt.waiting()
            pass
        else:
            pass
    except Exception as se:
        print(str(se))



def closeport():
    print('close')
    global rt
    global teststart_flag
    teststart_flag=0
    print(rt.tg_serial.name)
    rt.stop()
    ff.close()
def starttest():
    global q
    global teststart_flag
    teststart_flag=1
    ss=worker(q)
    ss.start() 
# 调用串口，测试串口


def main():
    rt = ComThread()
    global q
    ss=worker(q)
    ss.start() 
    try:
        if rt.start():
            # print(rt.tg_serial.name)
            rt.waiting()
            rt.stop()
        else:
            pass
    except Exception as se:
        print(str(se))

    if rt.alive:
        rt.stop()
    print('End OK')
    del rt


# data process
class worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            global databuf
            # print("thread%d %s: waiting for task" % (self.ident, self.name))
            try:
                data = q.get(block=True, timeout=20)  # 接收消息 
                databuf =np.append(databuf,data)
                startsample=np.argwhere(databuf==32767)
                startsample=startsample.tolist()
                startsample=list(itertools.chain.from_iterable(startsample))
                # print(np.size(databuf))
                # print(startsample)
            #databuf[:startsample[0]]
                length =len(startsample)
                if(length>=2):
                    fftbuf =databuf[:startsample[1]]
                    fftbuf1=fftbuf[1::2]
                    fftbuf2=fftbuf[2::2]
                    fftbuf1=fftbuf1-fftbuf1.mean()
                    fftbuf2=fftbuf2-fftbuf2.mean()

                    from scipy.signal import blackman
                    from scipy.fftpack import fft
                    print(len(fftbuf2))
                    w = blackman(512)
                    ywf1 = fft(fftbuf1[:512]*w)
                    ywf2 = fft(fftbuf2[:512]*w)
                    x1=math.atan2(ywf1[50].imag,ywf1[50].real)
                    x2=math.atan2(ywf2[50].imag,ywf2[50].real)
                    degree=(x1-x2)*180/np.pi
                    if(degree<0):
                        degree=360+degree                    
                    gl.set_value('tg_value', str(degree/72))


                    #print(len(fftbuf1))
                    #print(length)
                    # print((fftbuf1))
                    drawPic(fftbuf1,fftbuf2,np.abs(ywf1),np.abs(ywf2))
                    #do fft_calc to update gui windows
                    databuf=databuf[startsample[1]:]
                    print("i am working")  
            except queue.Empty:
                print("Nothing to do!i will go home!")
                self.thread_stop = True
                break
            
           

            # print("task recv:%s ,task No:%d" % (data[0], data[1]))
                        
            # print("work finished!")
            q.task_done()    # 完成一个任务
            res = q.qsize()  # 判断消息队列大小
            if res > 0:
                print("fuck!There are still %d tasks to do" % (res))

    def stop(self):
        self.thread_stop = True
 

if __name__ == '__main__':

    # 设置一个主函数，用来运行窗口，便于若其他地方下需要调用串口是可以直接调用main函数
    main()
    # closeport()
