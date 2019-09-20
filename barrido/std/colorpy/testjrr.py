from colorpy import ciexyz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('QT4Agg')

wavel_file = np.loadtxt('long_de_onda.txt', delimiter=',')
wavel = wavel_file[0,:]
#print(np.size(wavel))
inten = pd.read_csv('inten.csv')
#print(inten)
# for i in range(np.size(wavel)):
#     plt.plot(wavel,inten.iloc[i])
#     figManager = plt.get_current_fig_manager()
#     figManager.window.showMaximized()
#     plt.show()

sp1 = [[wavel],[inten.iloc[0]]]
print(len(sp1))
print(np.size(sp1[0]))
print(np.size(sp1[1]))

ciexyz.xyz_from_spectrum(sp1)