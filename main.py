#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import serialport
import queue
import sys
import globalvar as gl
from serialport import drawPic


#===================================================================

# Create instance
matplotlib.use('TkAgg')
win = tk.Tk()


# Add a title
win.title("Time Grating test GUI")

# Disable resizing the GUI
win.resizable(800, 800)
win.geometry('800x800+500+100')

# Tab Control introduced here --------------------------------------
tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab
tabControl.add(tab1, text='Main GUI')      # Add the tab

tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='Settings')      # Make second tab visible

tab3 = ttk.Frame(tabControl)            # Add a third tab
tabControl.add(tab3, text='about')      # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------

#---------------Tab1控件介绍------------------#
# We are creating a container tab3 to hold all other widgets
monty = ttk.LabelFrame(tab1, text='传感器')
monty.grid(column=0, row=0, padx=18, pady=4)
drawPic.f = Figure(figsize=(8, 8), dpi=100)

drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=tab1)
drawPic.canvas.draw()
drawPic.canvas.get_tk_widget().grid(column=0, row=8, padx=8, pady=14)

# Changing our Label
ttk.Label(monty, text="时栅传感器:", font=("黑体", 24, "bold")
          ).grid(column=0, row=0, sticky='W')

# Adding a Textbox Entry widget
TG_degree_value = tk.StringVar()
TG_degree_value.set(gl.get_value('tg_degree_value'))
TG_min_value = tk.StringVar()
TG_min_value.set(gl.get_value('tg_min_value'))
TG_sec_value = tk.StringVar()
TG_sec_value.set(gl.get_value('tg_sec_value'))

TG_degree = ttk.Entry(monty, width=6, textvariable=TG_degree_value)
TG_degree.grid(column=1, row=0, sticky='W')
TG_degree['state'] = 'readonly'

ttk.Label(monty, text="°", font=("黑体", 30, "bold")
          ).grid(column=2, row=0, sticky='W')
TG_min = ttk.Entry(monty, width=6, textvariable=TG_min_value)
TG_min.grid(column=3, row=0, sticky='W')
TG_min['state'] = 'readonly'
ttk.Label(monty, text="′", font=("微软雅黑", 30, "bold")
          ).grid(column=4, row=0, sticky='W')
TG_sec = ttk.Entry(monty, width=6, textvariable=TG_sec_value)
TG_sec.grid(column=5, row=0, sticky='W')
TG_sec['state'] = 'readonly'
ttk.Label(monty, text="″", font=("宋体", 25, "bold")
          ).grid(column=6, row=0, sticky='W')

ttk.Button(monty, text="开始", width=1,
           command=serialport.starttest).grid(column=6, row=1)
ttk.Label(monty, text="光栅编码器:", font=("黑体", 24, "bold")
          ).grid(column=0, row=2, sticky='W')
OG_value = tk.StringVar()
OG_degree = ttk.Entry(monty, width=6, textvariable=OG_value)
OG_degree.grid(column=1, row=2, sticky='W')
OG_degree['state'] = 'readonly'
ttk.Label(monty, text="°", font=("黑体", 30, "bold")
          ).grid(column=2, row=2, sticky='W')
OG_min = ttk.Entry(monty, width=6, textvariable=OG_value)
OG_min.grid(column=3, row=2, sticky='W')
OG_min['state'] = 'readonly'
ttk.Label(monty, text="′", font=("微软雅黑", 30, "bold")
          ).grid(column=4, row=2, sticky='W')
OG_sec = ttk.Entry(monty, width=6, textvariable=OG_value)
OG_sec.grid(column=5, row=2, sticky='W')
OG_sec['state'] = 'readonly'
ttk.Label(monty, text="″", font=("宋体", 25, "bold")
          ).grid(column=6, row=2, sticky='W')

# Adding a Button


# 一次性控制各控件之间的距离
for child in monty.winfo_children():
    child.grid_configure(padx=3, pady=1)
# 单独控制个别控件之间的距离
#---------------Tab1控件介绍------------------#


#---------------Tab2控件介绍------------------#
# We are creating a container tab3 to hold all other widgets -- Tab2
serial_set = ttk.LabelFrame(tab2, text='serial-commnication settings')
serial_set.grid(column=0, row=0, padx=8, pady=8)


labelsFrame = ttk.LabelFrame(tab2, text=' 嵌套区域 ')
labelsFrame.grid(column=0, row=8, columnspan=4)

# Place labels into the container element - vertically
# Creating three cheser1ckbuttons
action = ttk.Button(serial_set, text="search serialport", width=15, command='')
action.grid(column=0, row=0, rowspan=2, ipady=7)
openserial = ttk.Button(serial_set, text="Open",
                        width=10, command=serialport.openport)
openserial.grid(column=0, row=3, rowspan=2, ipady=7)
closeserial = ttk.Button(serial_set, text="Close",
                         width=10, command=serialport.closeport)
closeserial.grid(column=0, row=5, rowspan=2, ipady=7)
info = ttk.LabelFrame(tab2, text='sample settings')
info.grid(column=0, row=3, padx=8, pady=8)
ttk.Label(info, text="采样率:4000HZ").grid(column=0, row=9, sticky='W')
ttk.Label(info, text="信号频率:400hz").grid(column=0, row=10, sticky='W')
ttk.Label(info, text="采样点数:512").grid(column=0, row=11, sticky='W')
confirm = ttk.Button(info, text="apply", width=15, command='')
confirm.grid(column=0, row=12, rowspan=2, ipady=7)


plot_set = ttk.LabelFrame(tab2, text='plot settings')
plot_set.grid(column=0, row=8, columnspan=4)
chVarUn = tk.IntVar()
check3 = tk.Checkbutton(plot_set, text="origin data", variable=chVarUn)
check3.deselect()
check3.grid(column=0, row=0, sticky=tk.W)
savefile = tk.IntVar()
check4 = tk.Checkbutton(plot_set, text="save file", variable=chVarUn)
check4.deselect()
check4.grid(column=0, row=2, sticky=tk.W)
savefile = tk.IntVar()
check5 = tk.Checkbutton(plot_set, text="fft-phase", variable=chVarUn)
check5.deselect()
check5.grid(column=0, row=3, sticky=tk.W)

# GUI Callback function


def checkCallback(*ignoredArgs):
    # only enable one checkbutton
    if chVarUn.get(): check3.configure(state='disabled')
    else:             check3.configure(state='normal')


# trace the state of the two checkbuttons  #？？
chVarUn.trace('w', lambda unused0, unused1, unused2: checkCallback())

# create three Radiobuttons using one variable
radVar = tk.IntVar()

# Selecting a non-existing index value for radVar
radVar.set(99)

# Creating all three Radiobutton widgets within one loop

style = ttk.Style()
style.configure("BW.TLabel", font=("Times", "10", 'bold'))

# Create a container to hold labels


#---------------Tab2控件介绍------------------#


#---------------Tab3控件介绍------------------#
tab3 = tk.Frame(tab3, bg='#AFEEEE')
tab3.pack()

#---------------Tab3控件介绍------------------#


#----------------菜单栏介绍-------------------#
# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit()


# win.iconbitmap(r'C:\Users\feng\Desktop\研.ico')
# Place cursor into name Entry
TG_degree.focus()
#======================
# Start GUI
#======================
import threading
global timer

def fun_timer():
	TG_degree_value.set(gl.get_value('tg_degree_value'))
	TG_min_value.set(gl.get_value('tg_min_value'))
	TG_sec_value.set(gl.get_value('tg_sec_value'))
	
	timer = threading.Timer(0.5, fun_timer)
	timer.start()
timer = threading.Timer(1, fun_timer)
timer.start()  
win.mainloop()  
