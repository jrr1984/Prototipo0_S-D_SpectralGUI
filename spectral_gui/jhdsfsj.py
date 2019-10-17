# from tkinter import *
#
# def motion(event):
#   print("Mouse position: (%s %s)" % (event.x, event.y))
#   return
#
# master = Tk()
# whatever_you_do = 'Whatever you do will be insignificant, but it is very important that you do it.\n(Mahatma Gandhi)'
# msg = Message(master, text = whatever_you_do)
# msg.config(bg='lightgreen', font=('times', 24, 'italic'))
# msg.bind('<Motion>',motion)
# msg.pack()
# mainloop()

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports

fig = plt.Figure()

x = np.arange(0, 2*np.pi, 0.01)        # x-array

def animate(i):
    line.set_ydata(np.sin(x+i/10.0))  # update the data
    return line,

root = Tk.Tk()

label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ax = fig.add_subplot(111)
line, = ax.plot(x, np.sin(x))
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)

Tk.mainloop()