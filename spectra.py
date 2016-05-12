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

from PyQt4 import QtCore, QtGui
import numpy as np
import re
import interpolation

class Spectra():
    def __init__(self):
        """
        Initialize variables to hold all the methods and parameters related to fitting. This includes all the basis sets,
        reference spectra, calculated spectra and residuals. These variables also hold values for fitting range, spectral
        shift etc. as well.
        """
        self.referenceFileName = ''
        self.cy3FileName = ''
        self.cy5FileName = ''
        self.bkgFileName = ''
        # Unmodified Cy3 basis set format:{x:[],y:[]}
        self.cy3_basis = {'x': [], 'y': []}
        # Scaled Cy3 basis set format:{x:[],y:[]}
        self.cy3_basis_scaled = {'x': [], 'y': []}
        # Unmodified Cy5 basis set format:{x:[],y:[]}
        self.cy5_basis = {'x': [], 'y': []}
        # Scaled Cy5 basis set format:{x:[],y:[]}
        self.cy5_basis_scaled = {'x': [], 'y': []}
        # Unmodified background basis format:{x:[],y:[]}
        self.bkg_basis = {'x': [], 'y': []}
        # Scaled background basis format:{x:[],y:[]}
        self.bkg_basis_scaled = {'x': [], 'y': []}
        # *** Add another basis of direct excitation. (Think about the way it will be implemented) ***
        self.cy3_scaleFactor = 1.0
        self.cy5_scaleFactor = 1.0
        self.bkg_scaleFactor = 1.0
        self.offset = 0.0
        # The reference spectra that is being fitted format:{x:[],y:[]}
        self.reference = {}
        # The calculated spectra of the fit obtained for the reference format:{}
        self.calculated = {}
        # Subtracted Reference - Calculated format:{}
        self.residuals = {}
        # Sum of squares of the residuals
        self.error = 0.0
        # Area(Cy5)/(Area(Cy5) + Area(Cy3))
        self.fret = 0.0
        # Lowest X Value (Bounds/Selection)
        self.lowBound = np.Inf
        self.lowSelection = 0
        self.lowSelectionIndex = 0
        # Highest X Value (Bounds/Selection)
        self.highBound = -np.Inf
        self.highSelection = 0
        self.highSelectionIndex = 0
        # Shifts
        self.cy3Shift = 0
        self.cy5Shift = 0
        self.correctionFactor = 0.0
        self.directEmission = {}
        self.directEmission_fileName = ''
        self.cy5_correction = {'x': [], 'y': []}

    def calculateRegionBounds(self):
        """
        This method calculates the lowest wavelength and the highest wavelength of the reference spectra.
        This values is used to define the selection range of the plot for fitting.
        Here the range for fitting is initialized to the entire spectral range as a default.
        """
        self.lowBound = np.Inf
        self.highBound = -np.Inf
        for key in self.reference.keys():
            # Update low and high values of X
            if key < self.lowBound:
                self.lowBound = key
            if key > self.highBound:
                self.highBound = key
        self.lowSelection = self.lowBound
        self.highSelection = self.lowSelection + (self.highBound - self.lowBound)

    def calculateRegionIndex(self, lowSel, highSel):
        """
        Calculated the indices for selection range. This index is required for some plotting functions.
        This function is almost always called after calculateRegionBounds method.
        :param lowSel:self.lowSelection
        :param highSel:self.highSelection
        :return:NULL
        """
        lowDiffList = list(map(lambda x: int(x - lowSel), sorted(self.reference.keys())))
        highDiffList = list(map(lambda x: int(x - highSel), sorted(self.reference.keys())))

        try:
            self.lowestSelectionIndex = lowDiffList.index(0)
        except ValueError:
            pass
        
        try:
            self.highSelectionIndex = highDiffList.index(0)
        except ValueError:
            pass

    def read_spectra(self, filename, flag=True):
        """
        Reads spectra that is provided in a two column format (Wavelength, Value) separated by spaces or comma or tabs.
        Ignores lines that start with letters.
        :param filename: name of the file that has the recorded spectra
        """
        fh = open(filename, 'r')
        if (flag):
            spectra = {'x': [], 'y': []}
            for line in fh.readlines():
                line = line.rstrip()
                if re.match('^[0-9]', line):
                    lineSplit = re.split("\s+|\t+|,", line)
                    xvalue = float(lineSplit[0])
                    yvalue = float(lineSplit[1])
                    spectra['x'].append(xvalue)
                    spectra['y'].append(yvalue)
            return spectra
        else:
            spectra = {}
            for line in fh.readlines():
                line = line.rstrip()
                if re.match('^[0-9]', line):
                    lineSplit = re.split("\s+|\t+|,", line)
                    xvalue = float(lineSplit[0])
                    yvalue = float(lineSplit[1])
                    spectra[xvalue] = yvalue
            return spectra

    def initialize(self):
        if len(self.cy3_basis['x']) == 0:
            self.initializeSpectra(self.reference, self.cy3_basis, self.cy3_basis_scaled)
        if len(self.cy5_basis['x']) == 0:
            self.initializeSpectra(self.reference, self.cy5_basis, self.cy5_basis_scaled)
        if len(self.bkg_basis['x']) == 0:
            self.initializeSpectra(self.reference, self.bkg_basis, self.bkg_basis_scaled)
        if len(self.cy5_correction['x']) == 0:
            self.initializeSpectra(self.reference, self.cy5_correction, self.cy5_correction)
        if len(self.calculated.keys()) == 0:
            for key in self.reference.keys():
                self.calculated[key] = 0.0

    def initializeSpectra(self, ref, spec, spec_scaled):
        for key in ref.keys():
            spec['x'].append(key)
            spec['y'].append(0.0)
            spec_scaled['x'].append(key)
            spec_scaled['y'].append(0.0)

    def calculate_spectral_sum(self, area=True, offset_spin_value=0, offset_slider_value=0):
        """
        Calculates the sum of acceptor, donor and background from the scaled basis spectra.
        The offset is calculated as a sum of offset_slider and offset_slider values.
        In addition FRET efficiency is also calculated as given by [A_acceptor]/[A_acceptor + A_donor]
        where A is area under the corresponding spectra.
        All calculated parameters and spectra are stored in the class variables and nothing is returned.
        :param offset_spin_value:The offset value from the spinbox
        :param offset_slider_value:Th offset value from the slider
        :return:NULL
        """
        keys = list(self.calculated.keys())
        cy3_interpolated = interpolation.get_interpolated_value(self.cy3_basis_scaled, keys)
        cy5_interpolated = interpolation.get_interpolated_value(self.cy5_basis_scaled, keys)
        bkg_interpolated = interpolation.get_interpolated_value(self.bkg_basis_scaled, keys)
        cy5_corrected_interpolated = interpolation.get_interpolated_value(self.cy5_correction, keys)

        for key in keys:
            self.calculated[key] = cy3_interpolated[key] + \
                                   cy5_interpolated[key] + \
                                   bkg_interpolated[key] + \
                                   self.offset + \
                                   cy5_corrected_interpolated[key]

        if area == True:
            cy3_sum = 0.0
            for key in list(self.reference.keys()):
                cy3_sum += cy3_interpolated[key]
            cy5_sum = 0.0
            for key in list(self.reference.keys()):
                cy5_sum += cy5_interpolated[key]
            if (cy3_sum + cy5_sum) > 0:
                self.fret = cy5_sum/(cy3_sum + cy5_sum)
        else:
            self.fret = np.max(cy5_interpolated.values())/(np.max(cy3_interpolated.values()) +
                                                           np.max(cy5_interpolated.values()))

    def calculate_residuals(self):
        """
        Residual spectra as defined as the difference between Reference and Calculated spectra is computed in this method.
        In addition, mean square error is also calculated.
        NOTE to SELF: this error value cannot to cross reference, it does not give an intuition for how bad the fit is.
        Think about normalizing this error for each spectra (Maybe divide by the area under the reference spectra?!)
        :return:NULL
        """
        for key in list(self.reference.keys()):
            a = self.reference[key]
            b = self.calculated[key] if key in self.calculated else 0.0
            self.residuals[key] = a - b
            self.error += (a - b) ** 2/a
        self.error = self.error/(len(self.reference.values()) -  5)

    def return_yvalue(self, dictionary, x):
        return dictionary['y'][dictionary['x'].index(x)]

    def return_xvalue(self, dictionary, y):
        return dictionary['x'][dictionary['y'].index(y)]

    def getX_forYmax(self, dictionary):
        return dictionary['x'][dictionary['y'].index(max(dictionary['y']))]

    def getY_forXmax(self, dictionary):
        return dictionary['y'][dictionary['x'].index(max(dictionary['x']))]

    def rescale_basis(self, ref, base, wavelength):
        """
        Initializes the acceptor, donor and background basis to help fitting.
        :param ref:
        :param base:
        :param wavelength:
        :return:
        """
        scale_factor = ref[wavelength]/self.return_yvalue(base, wavelength)
        # spin.setValue(scale_factor)
        # spin.setEnabled(True)
        # slider.setEnabled(True)
        scaled_base = {'x': [], 'y': []}
        for key in list(base['x']):
            scaled_base['x'].append(key)
            scaled_base['y'].append(self.return_yvalue(base, key) * scale_factor)
        return (scaled_base, scale_factor)

    def rescale_correction_basis(self, ref, base):
        """
        Initializes the acceptor, donor and background basis to help fitting.
        :param ref:
        :param base:
        :return:
        """
        wavelength = self.getX_forYmax(ref)
        scale_factor = self.return_yvalue(ref, wavelength)/self.return_yvalue(base, wavelength)
        scaled_base = {'x': [], 'y': []}
        for key in list(base['x']):
            scaled_base['x'].append(key)
            scaled_base['y'].append(self.return_yvalue(base, key) * scale_factor)
        return scaled_base

    def append_array(self, outarray, inarray):
        for key in inarray:
            outarray.append([key])
        return outarray

    def save(self, filename):
        """
        Saves all the spectra, including the input spectra along with acceptor, donor, background, calculated spectra
        to a single comma separated file.
        :param filename: the name of the output file (obtained from a save Qt dialog)
        :return:NULL
        """
        fh = open(filename, 'w')
        fh.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ('Wavelength', 'Reference', 'Donor', 'Acceptor', 'Direct Emission Correction', 'Background', 'Fit', 'Donor + Acceptor', 'Residuals'))
        keys = self.makeUniqueKeyArray()
        for key in keys:
            ref = self.reference[key] if key in self.reference.keys() else ' '
            cy3 = self.cy3_basis_scaled['y'][self.cy3_basis_scaled['x'].index(key)] if key in self.cy3_basis_scaled['x'] else ' '
            cy5 = self.cy5_basis_scaled['y'][self.cy5_basis_scaled['x'].index(key)] if key in self.cy5_basis_scaled['x'] else ' '
            cy5_correction = self.cy5_correction['y'][self.cy5_correction['x'].index(key)] if key in self.cy5_correction['x'] else ' '
            bkg = self.bkg_basis_scaled['y'][self.bkg_basis_scaled['x'].index(key)] if key in self.bkg_basis_scaled['x'] else ' '
            calc = self.calculated[key] if key in self.calculated.keys() else ' '
            resi = self.residuals[key] if key in self.residuals.keys() else ' '
            cy3cy5 = cy3 if type(cy3) is not str else 0.0 + cy5 if type(cy5) is not str else 0.0
            fh.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(key, ref, cy3, cy5, cy5_correction, bkg, calc, cy3cy5, resi))
        fh.close()

    def makeUniqueKeyArray(self):
        keys = []
        keys = self.append_array(keys, self.reference.keys())
        keys = self.append_array(keys, self.cy3_basis_scaled['x'])
        keys = self.append_array(keys, self.cy5_basis_scaled['x'])
        keys = self.append_array(keys, self.bkg_basis_scaled['x'])
        keys = np.array(keys)
        keys = np.unique(keys)
        return keys