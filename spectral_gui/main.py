import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg") #backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

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

#pretty stuff for plots:
#para poner la leyenda fuera y arriba del grafico
# legend(bbox_to_anchor=(0,1.02,1,.102),loc=3, ncol=2, borderaxespad=0)

class SpectralGui(tk.Tk):

    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Spectral GUI")
        tk.Tk.iconbitmap(self,'c:/users/juanr/downloads/logo_lec.ico')
        tk.Tk.state(self,'zoomed')

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
        fig, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

        # fig = Figure()
        # a = fig.add_subplot(111)

        wavel_file = pd.read_csv('long_de_onda_1_tira.csv')
        inten_file = pd.read_csv('inten_paso_500micrones.csv')
        RGB_file = pd.read_csv('RGB_colors.csv')
        R_array = RGB_file.iloc[:, 0].values
        G_array = RGB_file.iloc[:, 1].values
        B_array = RGB_file.iloc[:, 2].values

        Z1 = np.vstack([R_array, G_array, B_array])
        a0.imshow(np.dstack(Z1), interpolation='none', aspect='auto', extent=[0.0, 13.0, 0, 13.0])
        a0.set_ylabel('y [mm]')
        a0.set_xlabel('x [mm]')

        a1.set_ylabel('Intensity [a.u.]')
        a1.set_xlabel('Wavelength [nm]')
        fig.tight_layout()

        def motion(event):
            global ix
            ix = event.xdata
            # print(event.inaxes)
            if a0 == event.inaxes:
                print("Moving through X-Y plot")
                x, y = event.inaxes.transData.inverted().transform((event.x, event.y)) #transforma de coordenadas del Tkinker Canvas a coordenadas del matplotlib plot
                print("Mouse position: (%s %s)" % (x, y))
                a1.plot(wavel_file.iloc[:, 0], inten_file.iloc[0], '*')
                canvas.draw()

            else:
                a1.clear()
                a1.set_ylabel('Intensity [a.u.]')
                a1.set_xlabel('Wavelength [nm]')
                canvas.draw()
                print('Not there moron')
                return



        canvas = FigureCanvasTkAgg(fig,self)
        # canvas.draw()
        canvas.callbacks.connect('motion_notify_event', motion)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        #navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) #para que este arriba la toolbar
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)






app = SpectralGui()
#app.geometry("1920x1080")#size of the app
app.mainloop()