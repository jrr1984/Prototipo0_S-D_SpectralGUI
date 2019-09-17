import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

wavel_file = np.loadtxt('long_de_onda.txt', delimiter=',')
wavel = wavel_file[0,:]
#print(np.size(wavel))
inten = pd.read_csv('inten.csv')
print(inten)
for i in range(len(wavel)):
    plt.plot(wavel,inten[i,:])
    plt.show