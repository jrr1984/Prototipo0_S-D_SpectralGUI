import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import numpy as np
long_de_onda = np.loadtxt('long_de_onda.txt',dtype=float,delimiter=',')
intensidad = np.loadtxt('intensidad.txt',dtype=float,delimiter=',')
#x, y, z = np.loadtxt('data.txt', unpack=True)
#N = int(len(z)**.5)
#z = z.reshape(N, N)
#plt.imshow(z+10, extent=(np.amin(x), np.amax(x), np.amin(y), np.amax(y)),
#        cmap=cm.hot, norm=LogNorm())
#plt.colorbar()
#plt.show()
plt.scatter(long_de_onda,intensidad)
plt.show()
print(np.size(long_de_onda))
print(np.size(intensidad))
