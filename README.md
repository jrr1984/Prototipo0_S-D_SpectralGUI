# Prototipo0_S-D_SpectralGUI


Repositorio de loss programas utilizados en el Prototipo preliminar, de la sección 3.1, capítulo 3, Diseño, construcción y aplicación de un microespectrómetro, de la [Tesis de Licenciatura](https://github.com/jrr1984/master_thesis_scratch_and_dig/blob/master/tesis_tex/main.pdf).

1. [Desarrollo de un sistema automatizado de adquisición del espectro de transmisión de cada una de las bandas del filtro](https://github.com/jrr1984/Prototipo0\_S-D\_SpectralGUI/blob/master/barrido/std)
2. [Driver de control del espectrómetro CCS200/M del fabricante Thorlabs](https://github.com/jrr1984/Prototipo0_S-D_SpectralGUI/blob/master/syst/CCS200.py)
3. [Driver de control de los motores paso a paso ZST213B de Thorlabs, montados sobre una stage XYZ MT3/M de Thorlabs](https://github.com/jrr1984/Prototipo0_S-D_SpectralGUI/blob/master/barrido/std/thor_stepm.py)
4. [Interfaz gráfica de mapas multiespectrales, de transmisión y del chi cuadrado](https://github.com/jrr1984/Prototipo0_S-D_SpectralGUI/blob/master/spectral_gui/main.py)

![Interfaz gráfica cuyo \textit{imshow} tiene una paleta de colores del espectro visible, de acuerdo al espacio de color CIE XYZ](https://github.com/jrr1984/Prototipo0_S-D_SpectralGUI/blob/master/spectral_gui/guirgb.png)

5. [Algoritmo de detección y cuantificación de los defectos](https://github.com/jrr1984/defects_analysis/blob/master/defects_thresholding.py)
6. [Método alternativo para detectar agujeros (en desarrollo)](https://github.com/jrr1984/defects_analysis/blob/master/find_contours_holes_trial.py)
7. [Análisis cuantitativo de los defectos](https://github.com/jrr1984/defects_analysis/blob/master/Defects%20analysis.ipynb)
8. [Población de defectos en general](https://github.com/jrr1984/defects_analysis/blob/master/general_defects_population.ipynb)

[Dependencias del repositorio](https://github.com/jrr1984/Prototipo0_S-D_SpectralGUI/blob/master/dependencias.txt)
