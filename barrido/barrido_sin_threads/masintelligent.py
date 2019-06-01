import numpy as np
dx = 1
dy=1
x_array_scan = np.arange(0.0,dx*(10+1),dx)
y_array_scan = np.arange(0.0,dy*(10+1),dy)

x_positions = []
y_positions = []
success = False
state = 'Init'
y=0.0

while success == False:
    if state == 'Init':
        for i in x_array_scan:
            x_positions.append(i)
            y_positions.append(y)
        y += dy
        state = 'Reversed x'
    if state == 'Reversed x':
        for i in reversed(x_array_scan):
            x_positions.append(i)
            y_positions.append(y)

        if y == y_array_scan[-1]:
            success = True
            break
        y += dy
        state = 'Forward x'
    if state == 'Forward x':
        for i in x_array_scan:
            x_positions.append(i)
            y_positions.append(y)
        if y == y_array_scan[-1]:
            success = True
        y += dy
        state = 'Reversed x'


for i, j in zip(x_positions, y_positions):
    print(i,j)