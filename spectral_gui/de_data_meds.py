import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ciexyz import xyz_from_spectrum
from colormodels import irgb_from_xyz
plt.switch_backend('QT4Agg')

wavel_file = pd.read_csv('long_de_onda_1_tira.csv')
inten_file = pd.read_csv('inten_paso_500micrones.csv')
wavel_array = wavel_file.iloc[:,0:].values
inten_array = inten_file.iloc[:,0:].values

list_of_colors = []

for row in range(len(inten_array)):
    spectra = np.column_stack((wavel_array,inten_array[row,:]))
    xyz_color_vec = xyz_from_spectrum(spectra)
    # print(np.shape(spectrum))
    rgb_disp = irgb_from_xyz(xyz_color_vec)
    list_of_colors.append(rgb_disp)

fig = plt.figure()
rgb_matrix = np.asarray(list_of_colors)
Z1 = np.vstack([rgb_matrix[:,0], rgb_matrix[:,1], rgb_matrix[:,2]])
im = plt.imshow(np.dstack(Z1), interpolation='none', aspect='auto',extent=[0.0, 13.0, 0, 13.0])
plt.show()