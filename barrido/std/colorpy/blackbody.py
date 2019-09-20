'''
blackbody.py - Color of thermal blackbodies.

Description:

Calculate the spectrum of a thermal blackbody at an arbitrary temperature.

Constants:

PLANCK_CONSTANT   - Planck's constant, in J-sec
SPEED_OF_LIGHT    - Speed of light, in m/sec
BOLTZMAN_CONSTANT - Boltzman's constant, in J/K
SUN_TEMPERATURE   - Surface temperature of the Sun, in K

Functions:

blackbody_specific_intensity (wl_nm, T_K) -
    Get the monochromatic specific intensity for a blackbody -
        wl_nm = wavelength [nm]
        T_K   = temperature [K]
    This is the energy radiated per second per unit wavelength per unit solid angle.
    Reference - Shu, eq. 4.6, p. 78.

blackbody_spectrum (T_K) -
    Get the spectrum of a blackbody, as a numpy array.

blackbody_color (T_K) -
    Given a temperature (K), return the xyz color of a thermal blackbody.

Plots:

blackbody_patch_plot (T_list, title, filename) -
    Draw a patch plot of blackbody colors for the given temperature range.

blackbody_color_vs_temperature_plot (T_list, title, filename) -
    Draw a color vs temperature plot for the given temperature range.

blackbody_spectrum_plot (T_K) -
    Draw the spectrum of a blackbody at the given temperature.

References:

Frank H. Shu, The Physical Universe. An Introduction to Astronomy,
University Science Books, Mill Valley, California. 1982. ISBN 0-935702-05-9.

Charles Kittel and Herbert Kroemer, Thermal Physics, 2nd edition,
W. H. Freeman, New York, 1980. ISBN 0-7167-1088-9.

License:

Copyright (C) 2008 Mark Kness

Author - Mark Kness - mkness@alumni.utexas.net

This file is part of ColorPy.

ColorPy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

ColorPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with ColorPy.  If not, see <http://www.gnu.org/licenses/>.
'''
import math
import numpy
import pylab

import colormodels
import ciexyz
import plots

# Physical constants in mks units
PLANCK_CONSTANT   = 6.6237e-34      # J-sec
SPEED_OF_LIGHT    = 2.997925e+08    # m/sec
BOLTZMAN_CONSTANT = 1.3802e-23      # J/K
SUN_TEMPERATURE   = 5778.0          # K

def blackbody_specific_intensity (wl_nm, T_K):
    '''Get the monochromatic specific intensity for a blackbody -
        wl_nm = wavelength [nm]
        T_K   = temperature [K]
    This is the energy radiated per second per unit wavelength per unit solid angle.
    Reference - Shu, eq. 4.6, p. 78.'''
    # precalculations that could be made global
    a = (PLANCK_CONSTANT * SPEED_OF_LIGHT) / (BOLTZMAN_CONSTANT)
    b = (2.0 * PLANCK_CONSTANT * SPEED_OF_LIGHT * SPEED_OF_LIGHT)
    wl_m = wl_nm * 1.0e-9
    inv_exponent = (wl_m * T_K) / a
    # Very large exponents (small inv_exponent) result in nearly zero intensity.
    # Avoid the numeric troubles in this case and return zero intensity.
    if inv_exponent < 1.0 / 500.0:
        return 0.0
    exponent = 1.0 / inv_exponent
    specific_intensity = b / (math.pow (wl_m, 5) * (math.exp (exponent) - 1.0))
    return specific_intensity

def blackbody_spectrum (T_K):
    '''Get the spectrum of a blackbody, as a numpy array.'''
    spectrum = ciexyz.empty_spectrum()
    num_wl = spectrum.shape[0]
    for i in range (0, num_wl):
        # Intensity per unit wavelength.
        specific_intensity = blackbody_specific_intensity (spectrum [i][0], T_K)
        # Scale by size of wavelength interval.
        spectrum [i][1] = specific_intensity * ciexyz.delta_wl_nm * 1.0e-9
    return spectrum

def blackbody_color (T_K):
    '''Given a temperature (K), return the xyz color of a thermal blackbody.'''
    spectrum = blackbody_spectrum (T_K)
    xyz = ciexyz.xyz_from_spectrum (spectrum)
    return xyz

#
# Figures
#

def blackbody_patch_plot (T_list, title, filename):
    '''Draw a patch plot of blackbody colors for the given temperature range.'''
    xyz_colors = []
    color_names = []
    for Ti in T_list:
        xyz = blackbody_color (Ti)
        xyz_colors.append (xyz)
        name = '%g K' % (Ti)
        color_names.append (name)
    plots.xyz_patch_plot (xyz_colors, color_names, title, filename)

def blackbody_color_vs_temperature_plot (T_list, title, filename):
    '''Draw a color vs temperature plot for the given temperature range.'''
    num_T = len (T_list)
    rgb_list = numpy.empty ((num_T, 3))
    for i in range (0, num_T):
        T_i = T_list [i]
        xyz = blackbody_color (T_i)
        rgb_list [i] = colormodels.rgb_from_xyz (xyz)
    # Note that b and g become negative for low T.
    # MatPlotLib skips those on the semilog plot.
    plots.color_vs_param_plot (
        T_list,
        rgb_list,
        title,
        filename,
        plotfunc = pylab.semilogy,
        tight = True,
        xlabel = r'Temperature (K)',
        ylabel = r'RGB Color')

def blackbody_spectrum_plot (T_K):
    '''Draw the spectrum of a blackbody at the given temperature.'''
    spectrum = blackbody_spectrum (T_K)
    title    = 'Blackbody Spectrum - T %d K' % (round (T_K))
    filename = 'BlackbodySpectrum-%dK' % (round (T_K))
    plots.spectrum_plot (
        spectrum,
        title,
        filename,
        xlabel = 'Wavelength (nm)',
        ylabel = 'Specific Intensity')
        #ylabel = 'Intensity ($W/m^2$)')   # with LaTex symbols, the axis text gets too big...

# Create sample figures

def figures ():
    '''Create some blackbody plots.'''
    # Some patch plots.
    T_norm = plots.log_interpolate ( 1200.0, 20000.0, 48)
    T_hot  = plots.log_interpolate (10000.0, 40000.0, 24)
    T_cool = plots.log_interpolate (  950.0,  1200.0, 24)
    blackbody_patch_plot (T_norm, 'Blackbody Colors',      'Blackbody-Patch')
    blackbody_patch_plot (T_hot,  'Hot Blackbody Colors',  'Blackbody-HotPatch')
    blackbody_patch_plot (T_cool, 'Cool Blackbody Colors', 'Blackbody-CoolPatch')

    # Color vs temperature.
    T_norm = numpy.linspace( 1200.0, 16000.0, 300)
    T_hot  = numpy.linspace(10000.0, 40000.0, 300)
    T_cool = numpy.linspace(  950.0,  1200.0, 300)
    blackbody_color_vs_temperature_plot (T_norm, 'Blackbody Colors',      'Blackbody-Colors')
    blackbody_color_vs_temperature_plot (T_hot,  'Hot Blackbody Colors',  'Blackbody-HotColors')
    blackbody_color_vs_temperature_plot (T_cool, 'Cool Blackbody Colors', 'Blackbody-CoolColors')

    # Spectrum for some specific temperatures.
    blackbody_spectrum_plot (2000.0)
    blackbody_spectrum_plot (3000.0)           # Proxima Centauri.
    blackbody_spectrum_plot (SUN_TEMPERATURE)  # Sun.
    blackbody_spectrum_plot (11000.0)          # Rigel.
    blackbody_spectrum_plot (15000.0)


if __name__ == '__main__':
    figures()
