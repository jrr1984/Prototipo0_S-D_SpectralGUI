import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg") #backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt

# import urllib
# import quandl
import json
import pandas as pd
import numpy as np

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

# def changeLightSource(toWhat,pn):


def popupmsg(msg):
    popup = tk.Tk()
    def leavemini():
        popup.destroy()

    popup.wm_title("!")
    label = ttk.Label(popup,text=msg,font = NORM_FONT)
    label.pack(side="top",fill="x",pady=10)
    B1 = ttk.Button(popup,text = "Ok", command = leavemini )
    B1.pack()
    popup.mainloop()


def animate(i):
    print("Hello World")
    # mydata = quandl.get("EOD/PAM", authtoken="GrWDhLRHX9UVSxW4t1qQ", start_date="1970-01-01", end_date="1970-01-01")
    # pullData = open("sampleData.txt","r").read()
    # dataList = pullData.split('\n')
    # xList = []
    # yList = []
    #
    # for eachline in dataList:
    #     if len(eachline)>1: #if empty line
    #         x,y = eachline.split(',')
    #         xList.append(int(x))
    #         yList.append((int(y)))
    #
    # a.clear()
    # a.plot(xList,yList)


#pretty stuff for plots:
#para poner la leyenda fuera y arriba del grafico
# legend(bbox_to_anchor=(0,1.02,1,.102),loc=3, ncol=2, borderaxespad=0)
class SpectralGui(tk.Tk):

    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Spectral GUI")
        tk.Tk.iconbitmap(self,'c:/users/juanr/downloads/logo_lec.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Save settings",command = lambda: popupmsg("Not supported yet"))
        filemenu.add_separator() #agrega una barra separadora entre las opciones
        filemenu.add_command(label = "Exit",command = quit)
        menubar.add_cascade(label = "File", menu = filemenu)

        # dataChoice = tk.Menu(menubar,tearoff=1)
        # dataChoice.add_command(label = "R-LED",command=lambda: changeLightSource("R-LED", "R-LED"))
        # dataChoice.add_command(label="G-LED", command=lambda: changeLightSource("G-LED", "G-LED"))
        # dataChoice.add_command(label="B-LED", command=lambda: changeLightSource("B-LED", "B-LED"))
        # dataChoice.add_command(label="NIR", command=lambda: changeLightSource("NIR", "NIR"))
        # dataChoice.add_command(label="Broadband", command=lambda: changeLightSource("Broadband", "Broadband"))
        # menubar.add_cascade(label="Source", menu=dataChoice)

        tk.Tk.config(self,menu = menubar)





        self.frames = {} #DICCIONARIO
        frame = SpectralPage(container,self)
        self.frames[SpectralPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(SpectralPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class SpectralPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        #label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)

        #graph
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        #navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) #para que este arriba la toolbar
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)






app = SpectralGui()
app.geometry("1920x1080")#size of the app
ani = animation.FuncAnimation(f,animate,interval=5000)
app.mainloop()