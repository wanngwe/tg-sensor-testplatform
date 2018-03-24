#======================  
# imports  
#======================  
import tkinter as tk  
from tkinter import ttk  
from tkinter import scrolledtext  
from tkinter import Menu  
from tkinter import Spinbox  

import serialport 
import queue 


#===================================================================             
  
# Create instance  
win = tk.Tk()     
  
# Add a title         
win.title("Time Grating test GUI")  
  
# Disable resizing the GUI  
win.resizable(800,400)
win.geometry('500x500+500+100')  
  
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
monty.grid(column=0, row=0, padx=8, pady=4)  
  
# Modified Button Click Function  
def clickMe():  
    action.configure(text='Hello\n ' + name.get())  
    action.configure(state='disabled')    # Disable the Button Widget  
  
# Changing our Label  
ttk.Label(monty, text="时栅传感器:").grid(column=0, row=0, sticky='W')  
  
# Adding a Textbox Entry widget  
name = tk.StringVar()  
TG_degree = ttk.Entry(monty, width=12, textvariable=name)  
TG_degree.grid(column=0, row=1, sticky='W') 

ttk.Label(monty, text="光栅编码器:").grid(column=0, row=2, sticky='W')  
OG_degree = tk.StringVar()  
OG_label = ttk.Entry(monty, width=12, textvariable=OG_degree)  
OG_label.grid(column=0, row=3, sticky='W')   
# Adding a Button  
action = ttk.Button(monty,text="开始测试",width=10,command=serialport.starttest)     
action.grid(column=2,row=1,rowspan=2,ipady=7)    
  

    
 
    
# 一次性控制各控件之间的距离  
for child in monty.winfo_children():   
    child.grid_configure(padx=3,pady=1)  
# 单独控制个别控件之间的距离  
action.grid(column=2,row=1,rowspan=2,padx=6)  
#---------------Tab1控件介绍------------------#  
  
  
#---------------Tab2控件介绍------------------#  
# We are creating a container tab3 to hold all other widgets -- Tab2  
serial_set = ttk.LabelFrame(tab2, text='serial-commnication settings')  
serial_set.grid(column=0, row=0, padx=8, pady=8) 


labelsFrame = ttk.LabelFrame(tab2, text=' 嵌套区域 ')  
labelsFrame.grid(column=0, row=8,columnspan=4)  
   
# Place labels into the container element - vertically   
# Creating three cheser1ckbuttons  
action = ttk.Button(serial_set,text="search serialport",width=15,command='')     
action.grid(column=0,row=0,rowspan=2,ipady=7) 
openserial = ttk.Button(serial_set,text="Open",width=10,command=serialport.openport)     
openserial.grid(column=0,row=3,rowspan=2,ipady=7)
closeserial = ttk.Button(serial_set,text="Close",width=10,command=serialport.closeport)     
closeserial.grid(column=0,row=5,rowspan=2,ipady=7)  
                 
# Adding a Combobox  
# book = tk.StringVar()  
# bookChosen = ttk.Combobox(serial_set, width=12, textvariable=book)
# plist=getports()
# portlist=[]
# for i in range(0,len(plist)):
#     portlist.append((plist[i])[0])
# bookChosen['values']=tuple(list(bookChosen['values'])+portlist)
# bookChosen.grid(column=0, row=2)  
# bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标  
# bookChosen.config(state='readonly')  #设为只读模式    

plot_set = ttk.LabelFrame(tab2, text='plot settings')  
plot_set.grid(column=10, row=8, columnspan=4)                       
chVarUn = tk.IntVar()  
check3 = tk.Checkbutton(plot_set, text="origin data", variable=chVarUn)  
check3.deselect()  
check3.grid(column=2, row=0, sticky=tk.W) 
savefile = tk.IntVar()  
check4 = tk.Checkbutton(plot_set, text="save file", variable=chVarUn)  
check4.deselect()  
check4.grid(column=3, row=2, sticky=tk.W) 
savefile = tk.IntVar()  
check5 = tk.Checkbutton(plot_set, text="fft-phase", variable=chVarUn)  
check5.deselect()  
check5.grid(column=3, row=3, sticky=tk.W)                   
  
# GUI Callback function   
def checkCallback(*ignoredArgs):  
    # only enable one checkbutton  
    if chVarUn.get(): check3.configure(state='disabled')  
    else:             check3.configure(state='normal')  
  
# trace the state of the two checkbuttons  #？？  
chVarUn.trace('w', lambda unused0, unused1, unused2 : checkCallback())      
    
# create three Radiobuttons using one variable  
radVar = tk.IntVar()  
  
# Selecting a non-existing index value for radVar  
radVar.set(99)      
  
# Creating all three Radiobutton widgets within one loop  

style = ttk.Style()  
style.configure("BW.TLabel", font=("Times", "10",'bold'))  
  
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
#win.iconbitmap(r'C:\Users\feng\Desktop\研.ico')    
# Place cursor into name Entry  
TG_degree.focus()        
#======================  
# Start GUI  
#======================  
win.mainloop()  