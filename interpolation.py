# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Venkatramanan Krishnamani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np

def get_indices(list, center):
    start =0
    end = 0
    if center < 3:
        start = 0
        end = 5
    elif center > len(list) - 3:
        start = len(list) - 5
        end = len(list)
    else:
        start = center - 2
        end = center + 3
    return (start, end)

def get_value(x, sol):
    sol = list(sol)
    sum = 0
    for k in sol:
        sum += k * x ** (len(sol) - sol.index(k) - 1)
    return sum

def interpolate(spectra, xvalue):
    """
    Polynomial interpolation at any point for a discrete input spectra.
    :param spectra: spectral file
    :param xvalue:
    :return:
    """
    xlist = np.array(spectra['x'])
    ylist = np.array(spectra['y'])
    (start_index, end_index) = get_indices(xlist, np.argmin(np.absolute(np.subtract(xlist, xvalue))))
    x_slice = list(xlist[start_index:end_index])
    ymat = list(ylist[start_index:end_index])
    xmat = np.ones((len(x_slice), len(x_slice)))
    for i in range(len(x_slice)):
        index = 0
        for j in x_slice:
            xmat[index, i] = j ** (len(x_slice)-i-1)
            index += 1
    solution = np.linalg.solve(xmat, ymat)
    return get_value(xvalue, solution)

def get_interpolated_value(spectra, xvalues):
    return_dict = {}
    for x in xvalues:
        value = 0.0
        if x in spectra['x']:
            x_index = spectra['x'].index(x)
            value = spectra['y'][x_index]
        else:
            value = interpolate(spectra, x)
        return_dict[x] = value
    return return_dict

def get_interpolated_val(spectra, xvalue):
    value = 0.0
    try:
        x_index = spectra['x'].index(xvalue)
        value = spectra['y'][x_index]
    except ValueError:
        value = interpolate(spectra, xvalue)
    return value
    