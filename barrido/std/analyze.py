import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('QT4Agg')

#wavel_file = np.loadtxt('long_de_onda.txt', delimiter=',')
#wavel = wavel_file[0,:]
#print(np.size(wavel))
wavel = pd.read_csv('long_de_onda_1_tira.csv')
print(type(wavel))
# print(wavel)
inten = pd.read_csv('inten.csv')
#print(inten)
for i in range(np.size(wavel)):
    plt.plot(wavel.iloc[:,0],inten.iloc[i])
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

# sp1 = np.array([wavel,inten.iloc[0]])
# print(len(sp1))
