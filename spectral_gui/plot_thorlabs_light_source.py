import pandas as pd
import numpy as np
from plots import wavelength_to_rgb
import matplotlib
import matplotlib.pyplot as plt
wavel_df = pd.read_pickle("wavel_df.pkl")
wavel_df = wavel_df.iloc[1:]
light_df = pd.read_csv("fuentethor.csv",header=None)
light_df = light_df.iloc[1:]

def normalize(arr):
    arr_min = arr.min()
    arr_max = arr.max()
    return arr/ arr_max

light_df = np.array(light_df)
light_df = normalize(light_df)
light_df = light_df.transpose()
light_df= light_df[0,:]

from scipy.signal import savgol_filter
yhat = savgol_filter(light_df, 55, 3)
wavel_df = wavel_df[0:3600]
yhat = yhat[0:3600]

plt.grid()
clim = (350, 780)
norm = plt.Normalize(*clim)
wl = np.arange(clim[0], clim[1] + 1, 2)
colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)
wavel_array = wavel_df.iloc[:, 0].values
wavelengths = wavel_array
spectrum = yhat
plt.plot(wavel_df, spectrum, color='darkred')
y = np.linspace(0, np.max(spectrum), 100)
X, Y = np.meshgrid(wavelengths, y)

extent = (np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

plt.imshow(X, clim=clim, extent=extent, cmap=spectralmap, aspect='auto')
plt.xlabel('Longitud de onda [nm]',fontsize=30)
plt.ylabel('Intensidad [a.u.]',fontsize=30)
plt.ylim(bottom=0)

plt.fill_between(wavelengths, spectrum ,np.max(spectrum), color='w')
plt.show()