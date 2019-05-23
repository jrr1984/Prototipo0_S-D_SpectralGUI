# -*- coding: utf-8 -*-
"""
Demonstrates common image analysis tools.

Many of the features demonstrated here are already provided by the ImageView
widget, but here we present a lower-level approach that provides finer control
over the user interface.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


# Interpret image data as row-major instead of col-major
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800,800)
cw = QtGui.QWidget()
mw.setCentralWidget(cw)
l = QtGui.QVBoxLayout()
cw.setLayout(l)

# A plot area (ViewBox + axes) for displaying the image
p1 = pg.PlotWidget()

x = np.arange(50,80,0.5)
y = np.arange(15,60,0.1)
z = np.arange(16,50,0.5)
data = np.random.normal(1,5,(len(z),len(x),len(y)))

imv = pg.ImageView()
imv.show()
imv.setImage(data,pos=(x.min(),y.min()),scale=(x[1]-x[0], y[1]-y[0]),xvals=z)
l.addWidget(imv)
g = pg.GridItem()
imv.addItem(g)

mw.show()
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
