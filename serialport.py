import threading
import time
import serial
import numpy as np
import queue
import matplotlib.pyplot as plt
import matplotlib  
global q
global teststart_flag
global databuf
import globalvar as gl
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
         
    #在[0,100]范围内随机生成sampleCount个数据点  
    # x=np.random.randint(0,100,size=sampleCount)  
    # y=np.random.randint(0,100,size=sampleCount)  
    # color=['b','r','y','g']  
         
    #绘制这些随机点的散点图，颜色随机选取  
    # drawPic.a.scatter(x,y,s=3,color=color[np.random.randint(len(color))])  
    drawPic.a.set_title('sensor output: vef wave and travlling wave')
    drawPic.a.plot(data[:150],color='green')
    drawPic.a.plot(data1[:150],color='red')

    drawPic.b.set_title('calcuation result: phase diff')
    #drawPic.b.plot(data2,color='green')
    drawPic.b.plot(data3[:60],color='yellow')

    drawPic.canvas.draw()
class MyCom:
    def __init__(self, Port='COM3'):
        self.tg_serial                  = None
        self.alive                       = False
        self.waitEnd                   = None
        self.port                        = Port
        self.onlinetxt                  =None

    def open(self):
        self.tg_serial = serial.Serial(self.port, 115200)
        self.onlinetxt                  =open("online_analysis.txt", 'w+')
       # self.tg_serial.open()
        if self.tg_serial.isOpen():
            print(self.tg_serial.name)
            self.alive = True
            self.thread_read = None
            self.thread_read = threading.Thread(target=self.reciveData)
            self.thread_read.setDaemon(1)
            self.thread_read.start()
            return True
        else:
            return False

    def reciveData(self):
        while self.alive:
            time.sleep(0.1)
            data = ''
            data = data.encode('utf-8')
            rec_len = self.tg_serial.inWaiting()
            print(rec_len)
            if rec_len:
                data = data + self.tg_serial.read(rec_len)
                low = data[::2]
                high = data[1::2]
                d = [(high[i] << 8)+low[i] for i in range(len(low))]
                for i in range(len(d)-1):
                    if (d[i]==32767 and d[i+1]==32767):
                        break
                
                
                og_value=d[i+2]*20000+d[i+3]
                degree=d[i+4];
                gl.set_db_handle(degree)
                gl.set_mq_client((og_value))
                d = np.array(d, dtype='int16')
                for i in range(len(d)):
                    self.onlinetxt.write(str(d[i]))  # 将字符串写入文件中
                    self.onlinetxt.write("\n")  # 换行
        self.alive = False

    def stop(self):
        self.alive = False
        self.thread_read.join()
        
        if self.tg_serial.isOpen():
            print("com3 has been closed!")
            self.tg_serial.close()
        self.onlinetxt.close()
        


global rt
rt = MyCom()





# 调用串口，测试串口


def main():
    com=MyCom()
    try:
        if com.open():
            print(com.tg_serial.name)
            com.stop()
        else:
            pass
    except Exception as se:
        print(str(se))
    if com.alive:
        com.stop()
    del com

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
                databuf =databuf.tolist()
                #print(databuf)
                for i in range(len(databuf)-1):
                    if (databuf[i]==32767 and databuf[i+1]==32767):
                        break
                startsample=i
                # print(startsample)
                if startsample<200:
                    databuf=databuf[startsample+2:]
                   # print('next time')
                else:
                    #print(databuf[:startsample+2])
                    fftbuf =databuf[:startsample]
                                       
                  
                   # print(og_value)
                    # print(fftbuf[0])
                    # print(fftbuf[1])
                  

                    # fftbuf1=fftbuf1-fftbuf1.mean()
                    # fftbuf2=fftbuf2-fftbuf2.mean()
                    #print('fftbuf1len=%d'%len(fftbuf1))
                   # print('fftbuf2len=%d'%len(fftbuf2))
              
                  
                 
                    # x1=0
                    # x2=2
            
                    # f_degree.write(str(degree))
                    # f_degree.write('\n');




                        #print(len(fftbuf1))
                        #print(length)
                        # print((fftbuf1))
                    # drawPic(fftbuf1,fftbuf2,np.abs(ywf1),np.abs(ywf2))
                    #do fft_calc to update gui windows
                    databuf=databuf[startsample+2:]
                   # print("i am working")  
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
    main()
