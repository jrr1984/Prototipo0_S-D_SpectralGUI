import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plots import wavelength_to_rgb
import line_profiler
import atexit
profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)
import matplotlib.animation as animation

opt = 1

def changeSpectradisp(option):
    global opt
    opt = option

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

wavel_df = pd.read_pickle('wavel_df.pkl')
inten_df = pd.read_pickle('inten_fin.pkl')
light_df = pd.read_pickle('light_df.pkl')
RGB_pkl_df = pd.read_pickle('RGB_fin.pkl')
RGB_mean_df = pd.read_pickle('chibandas.pkl')

wavel_array = wavel_df.iloc[:, 0].values

xy_pos_df = pd.read_pickle('xy_poss.pkl')

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

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

normalization = False

def norm(booleanish):
    global normalization
    normalization = booleanish
    return normalization

im_change = False
im_option = 1

def imshow_choice(booleanish,opt):
    global im_change
    global im_option
    im_option = opt
    im_change = booleanish
    return im_change,im_option


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

        spectraChoice = tk.Menu(menubar,tearoff=0)

        spectraChoice.add_command(label="Fast&Simple Spectra",
                                  command= lambda: changeSpectradisp(0))
        spectraChoice.add_separator()
        spectraChoice.add_command(label="Fancy Spectra",
                                  command=lambda: changeSpectradisp(1))
        spectraChoice.add_separator()
        spectraChoice.add_command(label="Click On Demand",
                                  command=lambda: changeSpectradisp(2))
        spectraChoice.add_separator()
        menubar.add_cascade(label= "Spectra subplot",menu=spectraChoice)

        fastAndSimpChoice = tk.Menu(spectraChoice, tearoff=0)
        fastAndSimpChoice.add_command(label="Normalized",
                                      command=lambda: norm(True))
        fastAndSimpChoice.add_separator()
        fastAndSimpChoice.add_command(label="Not Normalized",
                                      command=lambda: norm(False))
        spectraChoice.add_cascade(label="Choose Spectra", menu=fastAndSimpChoice)

        dataSetMenu = tk.Menu(menubar, tearoff=0)
        dataSetMenu.add_command(label="Quartz-Tungsten", command=lambda: popupmsg("Not supported yet."))
        dataSetMenu.add_separator()
        dataSetMenu.add_command(label="NIR Source", command=lambda: popupmsg("Not supported yet."))
        dataSetMenu.add_separator()
        dataSetMenu.add_command(label="R LED", command=lambda: popupmsg("Not supported yet."))
        dataSetMenu.add_separator()
        dataSetMenu.add_command(label="G LED", command=lambda: popupmsg("Not supported yet."))
        dataSetMenu.add_separator()
        dataSetMenu.add_command(label="B LED", command=lambda: popupmsg("Not supported yet."))
        menubar.add_cascade(label="Light Source Datasets", menu=dataSetMenu)


        imshowChoice = tk.Menu(menubar,tearoff=0)

        imshowChoice.add_command(label="RGB",
                                  command= lambda: imshow_choice(True,0))
        imshowChoice.add_separator()
        imshowChoice.add_command(label="CHI SQUARE",
                                  command=lambda: imshow_choice(True,1))
        menubar.add_cascade(label= "Imshow Options",menu=imshowChoice)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Contact us", command=lambda: popupmsg("      JRR, HG & LEC \n juanreto@gmail.com"))
        menubar.add_cascade(label="Help", menu=helpmenu)




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
    # @profile
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.fig, (self.a0, self.a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2.5, 1]})
        if not im_option:
            RGB_df = RGB_pkl_df
            R_array = RGB_df.iloc[:, 0].values
            G_array = RGB_df.iloc[:, 1].values
            B_array = RGB_df.iloc[:, 2].values
            R = R_array.reshape(492, 260)
            G = G_array.reshape(492, 260)
            B = B_array.reshape(492, 260)
            img = np.empty((492, 260, 3), dtype=np.uint8)
            img[:, :, 0] = R
            img[:, :, 1] = G
            img[:, :, 2] = B
            self.a0.imshow(img, interpolation='none', aspect='auto', origin='lower', extent=[0.0, 13000.0, 0, 24500.0])
        else:
            RGB_df = RGB_mean_df
            chi_array = RGB_df.iloc[:].values
            chi_sq = chi_array.reshape(492, 260)
            clim = (0,.5)
            self.a0.imshow(chi_sq,clim = clim, interpolation='none', aspect='auto', origin='lower',
                            extent=[0.0, 13000.0, 0, 24500.0])



        self.a0.set_ylabel('y [\u03bcm]')
        self.a0.set_xlabel('x [\u03bcm]')

        self.a1.set_ylabel('Intensity [a.u.]')
        self.a1.set_xlabel('Wavelength [nm]')
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.ani = animation.FuncAnimation(self.fig,self.animate,interval=100)

    # @profile
    def motion(self,event):
        x_move = event.xdata
        y_move = event.ydata
        if opt == 0 or opt == 1:

            if self.a0 == event.inaxes:
                x_lst = find_nearest(xy_pos_df.iloc[:,0],x_move)
                y_lst = find_nearest(xy_pos_df.iloc[:,1], y_move)
                mouse_pos = xy_pos_df[(xy_pos_df.iloc[:, 0] == x_lst) & (xy_pos_df.iloc[:, 1] == y_lst)].index.tolist()
                self.a1.clear()
                self.a1.set_ylabel('Intensity [a.u.]')
                self.a1.set_xlabel('Wavelength [nm]')
                if len(mouse_pos) == 0:
                    pass
                else:
                    if normalization:
                        tmp = 1/light_df.iloc[:]
                        tmp[light_df.iloc[:]<0.1] = 0
                        inten_norm = (inten_df.iloc[mouse_pos, :] * tmp).abs()
                        # print(inten_norm)
                        if opt == 0:
                            self.a1.plot(wavel_df.iloc[:, 0], inten_norm.transpose(), '*')
                        elif opt == 1:
                            clim = (350, 780)
                            norm = plt.Normalize(*clim)
                            wl = np.arange(clim[0], clim[1] + 1, 2)
                            colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
                            spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)
                            mouse_pos = mouse_pos[0]
                            wavelengths = wavel_array
                            spectrum = np.transpose(inten_norm)
                            # print(spectrum)
                            self.a1.plot(wavel_array, spectrum, color='darkred')
                            # print(np.max(spectrum))
                            y = np.linspace(0, np.max(spectrum), 100)
                            X, Y = np.meshgrid(wavelengths, y)

                            extent = (np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

                            plt.imshow(X, clim=clim, extent=extent, cmap=spectralmap, aspect='auto')
                            plt.xlabel('Wavelength [nm]')
                            plt.ylabel('Intensity [a.u.]')

                            plt.fill_between(wavelengths, spectrum ,np.max(spectrum), color='w')

                    if not normalization:
                        if opt == 0:
                            self.a1.plot(wavel_df.iloc[:, 0], inten_df.iloc[mouse_pos, :].transpose(), '*')
                        elif opt == 1:
                            clim = (350, 780)
                            norm = plt.Normalize(*clim)
                            wl = np.arange(clim[0], clim[1] + 1, 2)
                            colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
                            spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)
                            mouse_pos = mouse_pos[0]
                            wavelengths = wavel_array
                            spectrum = np.transpose(inten_df.iloc[mouse_pos, :])
                            self.a1.plot(wavel_array, spectrum, color='darkred')
                            y = np.linspace(0, np.max(spectrum), 100)
                            X, Y = np.meshgrid(wavelengths, y)

                            extent = (np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

                            plt.imshow(X, clim=clim, extent=extent, cmap=spectralmap, aspect='auto')
                            plt.xlabel('Wavelength [nm]')
                            plt.ylabel('Intensity [a.u.]')

                            plt.fill_between(wavelengths, spectrum, np.max(spectrum), color='w')

            else:
                self.a1.clear()
                self.a1.set_ylabel('Intensity [a.u.]')
                self.a1.set_xlabel('Wavelength [nm]')
                return
    # @profile
    def on_click(self, event):
        if self.a0 == event.inaxes:
            x_click = event.xdata
            y_click = event.ydata
            if opt == 2:
                self.a1.clear()
                x_lst = find_nearest(xy_pos_df.iloc[:, 0], x_click)
                y_lst = find_nearest(xy_pos_df.iloc[:, 1], y_click)
                mouse_pos = xy_pos_df[(xy_pos_df.iloc[:, 0] == x_lst) & (xy_pos_df.iloc[:, 1] == y_lst)].index.tolist()

                if normalization:
                    tmp = 1 / light_df.iloc[:]
                    tmp[light_df.iloc[:] < 0.1] = 0
                    inten_norm = (inten_df.iloc[mouse_pos, :] * tmp).abs()
                    self.a1.plot(wavel_df.iloc[:, 0], inten_norm.transpose(), '*')
                else:
                    self.a1.plot(wavel_df.iloc[:, 0], inten_df.iloc[mouse_pos, :].transpose(), '*')

    @profile
    def imshow_call(self,im_option):
        global im_change
        im_change = False
        if not im_option:
            RGB_df = RGB_pkl_df
            R_array = RGB_df.iloc[:, 0].values
            G_array = RGB_df.iloc[:, 1].values
            B_array = RGB_df.iloc[:, 2].values
            R = R_array.reshape(492, 260)
            G = G_array.reshape(492, 260)
            B = B_array.reshape(492, 260)
            img = np.empty((492, 260, 3), dtype=np.uint8)
            img[:, :, 0] = R
            img[:, :, 1] = G
            img[:, :, 2] = B
            self.a0.imshow(img, interpolation='none', aspect='auto', origin='lower', extent=[0.0, 13000.0, 0, 24500.0])

        else:
            RGB_df = RGB_mean_df
            chi_array = RGB_df.iloc[:].values
            chi_sq = chi_array.reshape(492, 260)
            clim = (0,.5)
            self.a0.imshow(chi_sq, clim =clim,interpolation='none', aspect='auto', origin='lower',
                                extent=[0.0, 13000.0, 0, 24500.0])


    @profile
    def animate(self,interval):
        if opt != 2:
            self.canvas.callbacks.connect('motion_notify_event',self.motion)
        if opt == 2:
            self.canvas.mpl_connect('button_press_event', self.on_click)
        if im_change:
            self.imshow_call(im_option)
        self.canvas.draw()


app = SpectralGui()
app.mainloop()
