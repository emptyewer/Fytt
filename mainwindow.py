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

import Queue
import sys, os, threading
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import math
from scipy.optimize import curve_fit, OptimizeWarning, brute, fmin
from spectra import Spectra
from about import About_Dialog
from filelist import FileList_Window
from basisGui import BasisGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Fytt_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        '''

        Initialize global variables for this class and sets up UI elements in QT4.

        '''
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.spectra = Spectra()

        self.ref_plotData = pg.PlotDataItem()
        self.cy3_plotData = pg.PlotDataItem()
        self.cy5_plotData = pg.PlotDataItem()
        self.bkg_plotData = pg.PlotDataItem()
        self.cal_plotData = pg.PlotDataItem()
        self.res_plotData = pg.PlotDataItem()
        self.cy5_correction_plotData = pg.PlotDataItem()
        self.BasisDB = BasisGui()
        self.BasisDB.mainWindow = self
        # self.test_function()

    def reset_sliders(self):
        self.cy3_spin.setValue(self.cy3_slider.value() + self.cy3_spin.value())
        self.cy5_spin.setValue(self.cy5_slider.value() + self.cy5_spin.value())
        self.bkg_spin.setValue(self.bkg_slider.value() + self.bkg_spin.value())
        self.offset_spin.setValue(self.offset_slider.value() + self.offset_spin.value())
        self.cy3_slider.setValue(0.0)
        self.cy5_slider.setValue(0.0)
        self.bkg_slider.setValue(0.0)
        self.offset_slider.setValue(0.0)

    def plot_reference(self):
        # queue = Queue.Queue()
        if len(list(self.spectra.reference.keys())) > 0:
            ref_color = pg.mkPen({'color': 'FFCC00', 'width': 2})
            # t = threading.Thread(target=self.plot_graph_dictionary,
            #                 name='refplot',
            #                 args=[queue, self.spectra.reference, ref_color, 'Reference', self.ref_plotData, self.plot_widget])
            # t.start()
            # t.join()
            # self.ref_plotData = queue.get()
            self.ref_plotData = self.plot_graph_dictionary(self.spectra.reference, ref_color, 'Reference', self.ref_plotData, self.plot_widget)
            self.spectra.initialize()

    def plot_cy3(self):
        # queue = Queue.Queue()
        if len(list(self.spectra.cy3_basis_scaled['x'])) > 0:
            cy3_color = pg.mkPen({'color': 'F7846F', 'width': 2, 'style': QtCore.Qt.DotLine})
            # t = threading.Thread(target=self.plot_graph,
            #                 name='cy3plot',
            #                 args=[queue, self.spectra.cy3_basis_scaled, cy3_color, 'Donor', self.cy3_plotData, self.plot_widget])
            # t.start()
            # t.join()
            # self.cy3_plotData = queue.get()
            self.cy3_plotData = self.plot_graph(self.spectra.cy3_basis_scaled, cy3_color, 'Donor', self.cy3_plotData, self.plot_widget)

    def plot_cy5(self):
        # queue = Queue.Queue()
        if len(list(self.spectra.cy5_basis_scaled['x'])) > 0:
            cy5_color = pg.mkPen({'color': '88ABC2', 'width': 2, 'style': QtCore.Qt.DotLine})
            # t = threading.Thread(target=self.plot_graph,
            #                 name='cy5plot',
            #                 args=[queue, self.spectra.cy5_basis_scaled, cy5_color, 'Acceptor', self.cy5_plotData, self.plot_widget])
            # t.start()
            # t.join()
            # self.cy5_plotData = queue.get()
            self.cy5_plotData = self.plot_graph(self.spectra.cy5_basis_scaled, cy5_color, 'Acceptor', self.cy5_plotData, self.plot_widget)

    def plot_bkg(self):
        # queue = Queue.Queue()
        if len(list(self.spectra.bkg_basis_scaled['x'])) > 0:
            bkg_color = pg.mkPen({'color': '9B9E9C', 'width': 2, 'style': QtCore.Qt.DotLine})
            # t = threading.Thread(target=self.plot_graph,
            #                 name='bkgplot',
            #                 args=[queue, self.spectra.bkg_basis_scaled, bkg_color, 'Background', self.bkg_plotData, self.plot_widget])
            # t.start()
            # t.join()
            # self.bkg_plotData = queue.get()
            self.bkg_plotData = self.plot_graph(self.spectra.bkg_basis_scaled, bkg_color, 'Background', self.bkg_plotData, self.plot_widget)

    def plot_correction(self):
        # queue = Queue.Queue()
        if len(list(self.spectra.cy3_basis_scaled['x'])) > 0:
            corr_color = pg.mkPen({'color': 'FFFFFF', 'width': 1})
            # t = threading.Thread(target=self.plot_graph,
            #                 name='cy5_correctionplot',
            #                 args=[queue, self.spectra.cy5_correction, cy3_color, 'Donor', self.cy5_correction_plotData, self.plot_widget])
            # t.start()
            # t.join()
            # self.cy5_correction_plotData = queue.get()
            self.cy5_correction_plotData = self.plot_graph(self.spectra.cy5_correction, corr_color, 'Direct Emission', self.cy5_correction_plotData, self.plot_widget)

    def calculate_sum(self):
        self.spectra.calculate_spectral_sum()
        self.setFretValue()

    def calculate_residuals(self):
        self.spectra.calculate_residuals()

    def plot_sum(self):
        # queue = Queue.Queue()
        fit_color = pg.mkPen({'color': 'FF0080', 'width': 2})
        # t = threading.Thread(target=self.plot_graph_dictionary,
        #                     name='calplot',
        #                     args=[queue, self.spectra.calculated, fit_color, 'Calculated Fit', self.cal_plotData, self.plot_widget])
        # t.start()
        # t.join()
        # self.cal_plotData = queue.get()
        self.cal_plotData = self.plot_graph_dictionary(self.spectra.calculated, fit_color, 'Calculated Fit', self.cal_plotData, self.plot_widget)

    def plot_residual(self):
        # queue = Queue.Queue()
        self.err_lbl.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">%0.0f</span></p></body></html>" % self.spectra.error,  None))
        res_color = pg.mkPen({'color': '00DA3C', 'width': 2})
        # t = threading.Thread(target=self.plot_graph_dictionary,
        #                     name='dualplot',
        #                     args=[queue, self.spectra.residuals, res_color, 'Residuals', self.res_plotData, self.residual_widget])
        # t.start()
        # t.join()
        # self.res_plotData = queue.get()
        self.res_plotData = self.plot_graph_dictionary(self.spectra.residuals, res_color, 'Residuals', self.res_plotData, self.residual_widget)

    @QtCore.pyqtSlot()
    def plot_graph(self, data, params, name, plot, widget):
        plot.clear()
        return widget.plot(list(data['x']), list(data['y']), pen=params, antialias=True)

    @QtCore.pyqtSlot()
    def plot_graph_dictionary(self, dictionary, params, name, plot, widget):
        plot.clear()
        xvalues = []
        yvalues = []
        for key in sorted(dictionary.keys()):
            xvalues.append(key)
            yvalues.append(dictionary[key])
        return widget.plot(xvalues, yvalues, pen=params, antialias=True)
        # return widget.plot(list(dictionary.keys()), list(dictionary.values()), pen=params, antialias=True)

    def setFretValue(self):
        self.fret_lbl.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">%0.3f</span></p></body></html>" % self.spectra.fret,  None))

    def actionAboutFunction(self):
        about_dialog = About_Dialog()
        about_dialog.exec_()

    def regionChanged(self):
        (a, b) = self.region.getRegion()
        if a >= self.spectra.lowBound and b <= self.spectra.highBound and a != b:
            self.spectra.lowSelection, self.spectra.highSelection = self.region.getRegion()
            self.spectra.calculateRegionIndex(self.spectra.lowSelection, self.spectra.highSelection)

    def ref_clicked(self, btn):
        try:
            fD = QtGui.QFileDialog()
            fD.setFileMode(QtGui.QFileDialog.AnyFile)
            filename = fD.getOpenFileName(caption="Load Reference Spectra")
            if filename:
                self.spectra.referenceFileName = filename
                self.load_reference()
        except IOError:
            pass

    def load_reference(self, load=1):
        if load == 1:
            self.spectra.reference = self.spectra.read_spectra(self.spectra.referenceFileName, False)
            self.spectra.calculateRegionBounds()
            self.spectra.calculateRegionIndex(self.spectra.lowSelection, self.spectra.highSelection)
            self.spectra.initialize()

        # self.ref_filename_lbl.setText(os.path.basename(str(self.spectra.referenceFileName)))
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_reference()
        self.plot_sum()
        self.plot_residual()
        title = (self.spectra.referenceFileName[:40] + '.../' + os.path.basename(str(self.spectra.referenceFileName))) if len(self.spectra.referenceFileName) > 75 else self.spectra.referenceFileName
        self.plot_widget.plotItem.setTitle(title)
        self.region.setBounds([self.spectra.lowBound, self.spectra.highBound])
        self.region.setRegion([self.spectra.lowSelection, self.spectra.highSelection])
        self.cy3_btn.setEnabled(True)
        self.cy5_btn.setEnabled(True)
        self.bkg_btn.setEnabled(True)
        self.loadBasisSets_btn.setEnabled(True)

    def cy3_clicked(self, btn):
        try:
            fD = QtGui.QFileDialog()
            fD.setFileMode(QtGui.QFileDialog.AnyFile)
            filename = fD.getOpenFileName(caption="Load Donor Basis Spectra")
            if filename:
                self.spectra.cy3FileName = filename
                self.load_cy3()
        except IOError:
            pass

    def load_cy3(self, load=1):
        if load == 1:
            self.spectra.cy3_basis = self.spectra.read_spectra(self.spectra.cy3FileName)
            (self.spectra.cy3_basis_scaled, self.spectra.cy3_scaleFactor) = self.spectra.rescale_basis(self.spectra.reference, self.spectra.cy3_basis, self.spectra.getX_forYmax(self.spectra.cy3_basis))
        # self.cy3_filename_lbl.setText(os.path.basename(str(self.spectra.cy3FileName)))
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_cy3()
        self.plot_sum()
        self.plot_residual()
        self.autofit_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.offset_spin.setEnabled(True)
        self.offset_slider.setEnabled(True)
        self.cy3_spin.setValue(self.spectra.cy3_scaleFactor)
        self.cy3_spin.setEnabled(True)
        self.cy3_slider.setEnabled(True)
        self.donor_shift_cbx.setEnabled(True)
        self.donor_shift_spin.setEnabled(True)

    def cy5_clicked(self, btn):
        try:
            fD = QtGui.QFileDialog()
            fD.setFileMode(QtGui.QFileDialog.AnyFile)
            filename = fD.getOpenFileName(caption="Load Acceptor Basis Spectra")
            if filename:
                self.spectra.cy5FileName = filename
                self.load_cy5()
        except IOError:
            pass

    def load_cy5(self, load=1):
        if load == 1:
            self.spectra.cy5_basis = self.spectra.read_spectra(self.spectra.cy5FileName)
            (self.spectra.cy5_basis_scaled, self.spectra.cy5_scaleFactor) = self.spectra.rescale_basis(self.spectra.reference, self.spectra.cy5_basis, self.spectra.getX_forYmax(self.spectra.cy5_basis))
        # self.cy5_filename_lbl.setText(os.path.basename(str(self.spectra.cy5FileName)))
        self.cy5_spin.setValue(self.spectra.cy5_scaleFactor)
        self.cy5_spin.setEnabled(True)
        self.cy5_slider.setEnabled(True)
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_cy5()
        self.plot_sum()
        self.plot_residual()
        self.acceptor_shift_spin.setEnabled(True)
        self.acceptor_shift_cbx.setEnabled(True)

    def bkg_clicked(self, btn):
        try:
            fD = QtGui.QFileDialog()
            fD.setFileMode(QtGui.QFileDialog.AnyFile)
            filename = fD.getOpenFileName(caption="Load Background Basis Spectra")
            if filename:
                self.spectra.bkgFileName = filename
                self.load_bkg()
        except IOError:
            pass

    def load_bkg(self, load=1):
        if load == 1:
            self.spectra.bkg_basis = self.spectra.read_spectra(self.spectra.bkgFileName)
            (self.spectra.bkg_basis_scaled, self.spectra.bkg_scaleFactor) = self.spectra.rescale_basis(self.spectra.reference, self.spectra.bkg_basis, min(list(self.spectra.bkg_basis['x'])))
        # self.bkg_filename_lbl.setText(os.path.basename(str(self.spectra.bkgFileName)))
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_bkg()
        self.plot_sum()
        self.plot_residual()
        self.bkg_spin.setValue(self.spectra.bkg_scaleFactor)
        self.bkg_spin.setEnabled(True)
        self.bkg_slider.setEnabled(True)

    def directEmission_clicked(self):
        try:
            fD = QtGui.QFileDialog()
            fD.setFileMode(QtGui.QFileDialog.AnyFile)
            filename = fD.getOpenFileName(caption="Load Acceptor Direct Emission Basis Spectra")
            if filename:
                self.spectra.directEmission_fileName = filename
                self.load_directEmission()
        except IOError:
            pass

    def load_directEmission(self):
        self.spectra.directEmission = self.spectra.read_spectra(self.spectra.directEmission_fileName, flag=True)
        self.scale_directEmission()

    def scale_directEmission(self):
        self.spectra.cy5_correction = self.spectra.rescale_correction_basis(self.spectra.directEmission, self.spectra.cy5_basis)
        yvalues = []
        for yvalue in self.spectra.cy5_correction['y']:
            yvalues.append(self.spectra.correctionFactor * yvalue)
        self.spectra.cy5_correction['y'] = yvalues
        self.spectra.cy5_correction['x'] = self.spectra.cy5_basis_scaled['x']
        self.plot_correction()
        self.calculate_sum()
        self.plot_sum()

    def save_clicked(self, btn):
        fD = QtGui.QFileDialog()
        fD.setFileMode(QtGui.QFileDialog.AnyFile)
        filename = fD.getSaveFileName(caption="Save Calculated Spectra (do not enter extension)")
        params_filename = filename + '_fytt_params.dat'
        fh = open(params_filename, 'w')
        fh.write('%-21s : %.5f\n' % ('FRET', self.spectra.fret))
        fh.write('%-21s : %.5f\n' % ('Donor Multiplier', self.cy3_spin.value() + self.cy3_slider.value()))
        fh.write('%-21s : %.5f\n' % ('Donor Shift', self.spectra.cy3Shift))
        fh.write('%-21s : %.5f\n' % ('Acceptor Multiplier', self.cy5_spin.value() + self.cy5_slider.value()))
        fh.write('%-21s : %.5f\n' % ('Acceptor Shift', self.spectra.cy5Shift))
        fh.write('%-21s : %.5f\n' % ('Background Multiplier', self.bkg_spin.value() + self.bkg_slider.value()))
        fh.write('%-21s : %.5f\n' % ('Offset', self.offset_spin.value() + self.offset_slider.value()))
        fh.close()

        spectra_filename = filename + '_spectra.dat'
        self.spectra.save(spectra_filename)

    def cy3_valueChanged(self):
        for key in list(self.spectra.cy3_basis['x']):
            index = self.spectra.cy3_basis['x'].index(key)
            self.spectra.cy3_basis_scaled['y'][index] = self.spectra.cy3_basis['y'][index] * (self.cy3_spin.value() + self.cy3_slider.value())
        self.spectra.cy3_scaleFactor = self.cy3_spin.value() + self.cy3_slider.value()
        self.spectra.calculate_spectral_sum()
        self.setFretValue()
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_cy3()
        self.plot_sum()
        self.plot_residual()

    def cy5_valueChanged(self):
        for key in list(self.spectra.cy5_basis['x']):
            index = self.spectra.cy5_basis['x'].index(key)
            self.spectra.cy5_basis_scaled['y'][index] = self.spectra.cy5_basis['y'][index] * (self.cy5_spin.value() + self.cy5_slider.value())
        self.spectra.cy5_scaleFactor = self.cy5_spin.value() + self.cy5_slider.value()
        self.spectra.calculate_spectral_sum()
        self.setFretValue()
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_cy5()
        self.plot_sum()
        self.plot_residual()

    def bkg_valueChanged(self):
        for key in list(self.spectra.bkg_basis['x']):
            index = self.spectra.bkg_basis['x'].index(key)
            self.spectra.bkg_basis_scaled['y'][index] = self.spectra.bkg_basis['y'][index] * (self.bkg_spin.value()  + self.bkg_slider.value())
        self.spectra.bkg_scaleFactor = self.bkg_spin.value() + self.bkg_slider.value()
        self.spectra.calculate_spectral_sum()
        self.setFretValue()
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_bkg()
        self.plot_sum()
        self.plot_residual()

    def offset_valueChanged(self):
        self.spectra.calculate_spectral_sum()
        self.spectra.offset = self.offset_spin.value() + self.offset_slider.value()
        self.setFretValue()
        self.calculate_sum()
        self.calculate_residuals()
        self.plot_sum()
        self.plot_residual()

    def actionBatchFitFunction(self):
        self.filelist_window = FileList_Window()
        self.filelist_window.fileList_wgt.clear()
        self.filelist_window.loadFiles()
        self.filelist_window.show()
        self.filelist_window.fileList_wgt.currentItemChanged.connect(self.newSpectraSelected)
        self.filelist_window.fitall_btn.clicked.connect(self.fitAllSpectra)
        self.filelist_window.pushButton.clicked.connect(self.filelist_window.loadFiles)
        self.filelist_window.pushButton_3.clicked.connect(self.clearSpectraList)

    def clearSpectraList(self):
        self.spectra = Spectra()
        self.ref_plotData.clear()
        self.cy3_plotData.clear()
        self.cy5_plotData.clear()
        self.bkg_plotData.clear()
        self.cal_plotData.clear()
        self.res_plotData.clear()
        # self.ref_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.cy3_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.cy5_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.bkg_filename_lbl.setText(_translate("MainWindow", "...", None))
        self.filelist_window.spectraList = {}
        self.filelist_window.cy3_basis = {}
        self.filelist_window.cy5_basis = {}
        self.filelist_window.bkg_basis = {}
        self.filelist_window.cy3FileName = ''
        self.filelist_window.cy5FileName = ''
        self.filelist_window.bkgFileName = ''
        self.filelist_window.fileList_wgt.clear()


    def newSpectraSelected(self, currItem, prevItem):
        if currItem:
            self.reset_sliders()
            self.spectra = self.filelist_window.getSpectra(str(currItem.text()))
            self.load_reference(load=0)
            self.load_cy3(load=0)
            self.load_cy5(load=0)
            self.load_bkg(load=0)
            self.offset_spin.setValue(self.spectra.offset)

    def fitAllSpectra(self):
        spectralist = self.filelist_window.getAllSpectra()
        threads = []
        count = 1
        queue = Queue.Queue()
        for key in spectralist.keys():
            self.spectra = spectralist[key]
            self.load_reference(load=0)
            self.load_cy3(load=0)
            self.load_cy5(load=0)
            self.load_bkg(load=0)
            t = threading.Thread(target=self.autofit,
                            name=key,
                            args=[queue])
            t.start()
            t.join()
            popt = queue.get()
            self.setSpinValues(popt)
            self.plot_cy3()
            self.plot_cy5()
            self.plot_bkg()
            self.calculate_sum()
            self.calculate_residuals()
            self.plot_sum()
            self.plot_residual()

    def setSpinValues(self, popt):
        self.reset_sliders()
        self.cy3_spin.setValue(popt[0])
        self.cy5_spin.setValue(popt[1])
        self.bkg_spin.setValue(popt[2])
        self.spectra.cy3_scaleFactor = popt[0]
        self.spectra.cy5_scaleFactor = popt[1]
        self.spectra.bkg_scaleFactor = popt[2]

    def autofit_clicked(self):
        queue = Queue.Queue()
        t = threading.Thread(target=self.autofit,
                            name=self.spectra.referenceFileName,
                            args=[queue])
        t.start()
        t.join()
        popt = queue.get()
        self.setSpinValues(popt)
        self.plot_cy3()
        self.plot_cy5()
        self.plot_bkg()
        self.plot_sum()
        self.plot_residual()
        if not self.donor_shift_cbx.isChecked() or not self.acceptor_shift_cbx.isChecked():
            t = threading.Thread(target=self.autofit_shifts,
                                name=self.spectra.referenceFileName,
                                args=[])
            t.start()
            t.join()
            self.plot_cy3()
            self.plot_cy5()
            self.plot_sum()
            self.plot_residual()


    def autofit(self, queue):
        p0 = np.array([(self.cy3_spin.value() + self.cy3_slider.value()), (self.cy5_spin.value() + self.cy5_slider.value()), (self.bkg_spin.value() + self.bkg_slider.value()), (self.offset_spin.value() + self.offset_slider.value())])
        try:
            popt, pcov = curve_fit(self.fitting_function, np.array(list(self.spectra.reference.keys())[self.spectra.lowestSelectionIndex:self.spectra.highSelectionIndex]), np.array(list(self.spectra.reference.values())[self.spectra.lowestSelectionIndex:self.spectra.highSelectionIndex]), p0)
        except OptimizeWarning:
            pass
        queue.put(popt)

    def autofit_shifts(self):
        def shift_to_integer_multiples(xvalues, shift, assignment):
            spectra_shift = 0
            return_value = []
            if shift < 0:
                spectra_shift = math.floor(shift)
                return_value = list(np.array(xvalues) + math.floor(shift))
            else:
                spectra_shift = math.ceil(shift)
                return_value = list(np.array(xvalues) + math.ceil(shift))

            if assignment == 1:
                self.spectra.cy3Shift = spectra_shift
                self.donor_shift_spin.setValue(self.spectra.cy3Shift)
            elif assignment == 2:
                self.spectra.cy5Shift = spectra_shift
                self.acceptor_shift_spin.setValue(self.spectra.cy5Shift)
            return return_value

        xranges = ((-10,10), (-10,10))
        shift_fit = []
        shift_fit = brute(self.minimize_shifts_function, xranges, full_output=True, finish=fmin, Ns=10)

        if not self.donor_shift_cbx.isChecked():
            self.spectra.cy3_basis_scaled['x'] = shift_to_integer_multiples(self.spectra.cy3_basis_scaled['x'], shift_fit[0][0], 1)
        if not self.acceptor_shift_cbx.isChecked():
            self.spectra.cy5_basis_scaled['x'] = shift_to_integer_multiples(self.spectra.cy3_basis_scaled['x'], shift_fit[0][1], 2)
            self.spectra.cy5_correction['x'] = self.spectra.cy5_basis_scaled['x']


    def minimize_shifts_function(self, *params):
        shift1 = params[0][0]
        shift2 = params[0][1]
        if not self.donor_shift_cbx.isChecked():
            self.spectra.cy3_basis_scaled['x'] = list(np.array(self.spectra.cy3_basis['x']) + shift1)
        if not self.acceptor_shift_cbx.isChecked():
            self.spectra.cy5_basis_scaled['x'] = list(np.array(self.spectra.cy5_basis['x']) + shift2)
            self.spectra.cy5_correction['x'] = self.spectra.cy5_basis_scaled['x']
        self.spectra.calculate_spectral_sum()
        self.spectra.calculate_residuals()
        self.setFretValue()
        return self.spectra.error

    def fitting_function(self, x, alpha, beta, gamma, delta):
        if not self.cy3_ckbox.isChecked():
            for key in list(self.spectra.cy3_basis['x']):
                index = self.spectra.cy3_basis['x'].index(key)
                self.spectra.cy3_basis_scaled['y'][index] = self.spectra.cy3_basis['y'][index] * alpha
        if not self.cy5_ckbox.isChecked():
            for key in list(self.spectra.cy5_basis['x']):
                index = self.spectra.cy5_basis['x'].index(key)
                self.spectra.cy5_basis_scaled['y'][index] = self.spectra.cy5_basis['y'][index] * beta
        if not self.bkg_ckbox.isChecked():
            for key in list(self.spectra.bkg_basis['x']):
                index = self.spectra.bkg_basis['x'].index(key)
                if gamma < 0.0:
                    gamma = 0
                self.spectra.bkg_basis_scaled['y'][index] = self.spectra.bkg_basis['y'][index] * gamma
        if not self.offset_ckbox.isChecked():
            if delta <= 0:
                delta = 0
            self.offset_spin.setValue(delta)
            self.spectra.offset = delta

        self.spectra.calculate_spectral_sum()
        self.setFretValue()
        return np.array(map(lambda i: self.spectra.calculated[i], x))

    def donor_shift_valueChanged(self):
        self.donor_shift_cbx.setText(_translate("MainWindow", "Donor Shift (" + str(self.donor_shift_spin.value()) + ")", None))
        self.spectra.cy3_basis_scaled['x'] = list(np.array(self.spectra.cy3_basis['x']) + self.donor_shift_spin.value())
        self.spectra.calculate_spectral_sum()
        self.spectra.calculate_residuals()
        self.plot_cy3()
        self.plot_sum()
        self.plot_residual()
        self.setFretValue()

    def acceptor_shift_valueChanged(self):
        self.acceptor_shift_cbx.setText(_translate("MainWindow", "Acceptor Shift (" + str(self.acceptor_shift_spin.value()) + ")", None))
        self.spectra.cy5_basis_scaled['x'] = list(np.array(self.spectra.cy5_basis['x']) + self.acceptor_shift_spin.value())
        self.spectra.cy5_correction['x'] = self.spectra.cy5_basis_scaled['x']
        self.spectra.calculate_spectral_sum()
        self.spectra.calculate_residuals()
        self.plot_cy5()
        self.plot_correction()
        self.plot_sum()
        self.plot_residual()
        self.setFretValue()

    @QtCore.pyqtSlot()
    def sync_xranges(self):
        plot_range = self.plot_widget.plotItem.viewRange()
        self.residual_widget.plotItem.setXRange(plot_range[0][0], plot_range[0][1], padding=0.0, update=True)

    def openBasisSetDatabase(self):
        self.BasisDB.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 800))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 730, 1001, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.buttons_layout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.buttons_layout.setMargin(0)
        self.buttons_layout.setObjectName(_fromUtf8("buttons_layout"))
        self.ref_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ref_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 204, 0);"))
        self.ref_btn.setObjectName(_fromUtf8("ref_btn"))
        self.buttons_layout.addWidget(self.ref_btn)
        self.cy3_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cy3_btn.setStyleSheet(_fromUtf8("background-color: rgb(247, 132, 111);"))
        self.cy3_btn.setObjectName(_fromUtf8("cy3_btn"))
        self.buttons_layout.addWidget(self.cy3_btn)
        self.cy5_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cy5_btn.setStyleSheet(_fromUtf8("background-color: rgb(136, 171, 194);"))
        self.cy5_btn.setObjectName(_fromUtf8("cy5_btn"))
        self.buttons_layout.addWidget(self.cy5_btn)
        self.bkg_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.bkg_btn.setStyleSheet(_fromUtf8("background-color: rgb(200, 200, 200);"))
        self.bkg_btn.setObjectName(_fromUtf8("bkg_btn"))
        self.buttons_layout.addWidget(self.bkg_btn)
        self.direct_emission_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.direct_emission_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.direct_emission_btn.setObjectName(_fromUtf8("direct_emission_btn"))
        self.buttons_layout.addWidget(self.direct_emission_btn)
        self.loadBasisSets_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.loadBasisSets_btn.setStyleSheet(_fromUtf8("background-color: rgb(105, 214, 135);"))
#        self.loadBasisSets_btn.setMaximumSize(QtCore.QSize(50, 40))
        self.loadBasisSets_btn.setObjectName(_fromUtf8("loadBasisSets_btn"))
        self.buttons_layout.addWidget(self.loadBasisSets_btn)
        self.line_5 = QtGui.QFrame(self.horizontalLayoutWidget)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.buttons_layout.addWidget(self.line_5)
        self.save_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.buttons_layout.addWidget(self.save_btn)
        self.toolButton = QtGui.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.buttons_layout.addWidget(self.toolButton)
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(850, 10, 160, 645))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.multipliers_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.multipliers_layout.setMargin(0)
        self.multipliers_layout.setObjectName(_fromUtf8("multipliers_layout"))
        self.cy3_ckbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cy3_ckbox.setObjectName(_fromUtf8("cy3_ckbox"))
        self.multipliers_layout.addWidget(self.cy3_ckbox)
        self.cy3_spin = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.cy3_spin.setMinimum(-9999999999)
        self.cy3_spin.setMaximum(9999999999)
        self.cy3_spin.setSingleStep(1000)
        self.cy3_spin.setObjectName(_fromUtf8("cy3_spin"))
        self.multipliers_layout.addWidget(self.cy3_spin)
        self.cy3_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.cy3_slider.setMinimum(0)
        self.cy3_slider.setMaximum(1000)
        self.cy3_slider.setOrientation(QtCore.Qt.Horizontal)
        self.cy3_slider.setObjectName(_fromUtf8("cy3_slider"))
        self.multipliers_layout.addWidget(self.cy3_slider)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.multipliers_layout.addItem(spacerItem1)
        self.cy5_ckbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.cy5_ckbox.setObjectName(_fromUtf8("cy5_ckbox"))
        self.multipliers_layout.addWidget(self.cy5_ckbox)
        self.cy5_spin = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.cy5_spin.setMinimum(-9999999999)
        self.cy5_spin.setMaximum(9999999999)
        self.cy5_spin.setSingleStep(1000)
        self.cy5_spin.setObjectName(_fromUtf8("cy5_spin"))
        self.multipliers_layout.addWidget(self.cy5_spin)
        self.cy5_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.cy5_slider.setMinimum(0)
        self.cy5_slider.setMaximum(1000)
        self.cy5_slider.setOrientation(QtCore.Qt.Horizontal)
        self.cy5_slider.setObjectName(_fromUtf8("cy5_slider"))
        self.multipliers_layout.addWidget(self.cy5_slider)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.multipliers_layout.addItem(spacerItem2)
        self.bkg_ckbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.bkg_ckbox.setObjectName(_fromUtf8("bkg_ckbox"))
        self.multipliers_layout.addWidget(self.bkg_ckbox)
        self.bkg_spin = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.bkg_spin.setMinimum(0)
        self.bkg_spin.setMaximum(9999999999)
        self.bkg_spin.setSingleStep(1000)
        self.bkg_spin.setProperty("value", 1)
        self.bkg_spin.setObjectName(_fromUtf8("bkg_spin"))
        self.multipliers_layout.addWidget(self.bkg_spin)
        self.bkg_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.bkg_slider.setMinimum(0)
        self.bkg_slider.setMaximum(1000)
        self.bkg_slider.setOrientation(QtCore.Qt.Horizontal)
        self.bkg_slider.setObjectName(_fromUtf8("bkg_slider"))
        self.multipliers_layout.addWidget(self.bkg_slider)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.multipliers_layout.addItem(spacerItem3)
        self.offset_ckbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.offset_ckbox.setObjectName(_fromUtf8("offset_ckbox"))
        self.multipliers_layout.addWidget(self.offset_ckbox)
        self.offset_spin = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.offset_spin.setMinimum(0)
        self.offset_spin.setMaximum(9999999999)
        self.offset_spin.setSingleStep(1000)
        self.offset_spin.setObjectName(_fromUtf8("offset_spin"))
        self.multipliers_layout.addWidget(self.offset_spin)
        self.offset_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.offset_slider.setMinimum(0)
        self.offset_slider.setMaximum(1000)
        self.offset_slider.setOrientation(QtCore.Qt.Horizontal)
        self.offset_slider.setObjectName(_fromUtf8("offset_slider"))
        self.multipliers_layout.addWidget(self.offset_slider)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.multipliers_layout.addItem(spacerItem4)
        self.donor_shift_cbx = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.donor_shift_cbx.setObjectName(_fromUtf8("donor_shift_cbx"))
        self.multipliers_layout.addWidget(self.donor_shift_cbx)
        self.donor_shift_spin = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.donor_shift_spin.setObjectName(_fromUtf8("donor_shift_slider"))
        self.donor_shift_spin.setMinimum(-99)
        self.donor_shift_spin.setMaximum(100)
        self.multipliers_layout.addWidget(self.donor_shift_spin)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.multipliers_layout.addItem(spacerItem5)
        self.acceptor_shift_cbx = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.acceptor_shift_cbx.setObjectName(_fromUtf8("acceptor_shift_cbx"))
        self.multipliers_layout.addWidget(self.acceptor_shift_cbx)
        self.acceptor_shift_spin = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.acceptor_shift_spin.setObjectName(_fromUtf8("acceptor_shift_slider"))
        self.acceptor_shift_spin.setMinimum(-99)
        self.acceptor_shift_spin.setMaximum(100)
        self.multipliers_layout.addWidget(self.acceptor_shift_spin)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.multipliers_layout.addWidget(self.label_5)
        self.fret_lbl = QtGui.QLabel(self.verticalLayoutWidget)
        self.fret_lbl.setObjectName(_fromUtf8("fret_lbl"))
        self.multipliers_layout.addWidget(self.fret_lbl)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.multipliers_layout.addItem(spacerItem6)
        self.label_7 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.multipliers_layout.addWidget(self.label_7)
        self.err_lbl = QtGui.QLabel(self.verticalLayoutWidget)
        self.err_lbl.setObjectName(_fromUtf8("err_lbl"))
        self.multipliers_layout.addWidget(self.err_lbl)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 710, 1001, 20))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLine_layout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLine_layout.setMargin(0)
        self.horizontalLine_layout.setObjectName(_fromUtf8("horizontalLine_layout"))
        self.line = QtGui.QFrame(self.horizontalLayoutWidget_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLine_layout.addWidget(self.line)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(830, 10, 16, 701))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLine_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLine_layout.setMargin(0)
        self.verticalLine_layout.setObjectName(_fromUtf8("verticalLine_layout"))
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLine_layout.addWidget(self.line_2)
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 811, 461))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.plot_layout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.plot_layout.setMargin(0)
        self.plot_layout.setObjectName(_fromUtf8("plot_layout"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 480, 811, 221))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.residual_layout = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.residual_layout.setMargin(0)
        self.residual_layout.setObjectName(_fromUtf8("residual_layout"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(850, 660, 161, 41))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.autofitting_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.autofitting_layout.setMargin(0)
        self.autofitting_layout.setObjectName(_fromUtf8("autofitting_layout"))
        self.autofit_btn = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.autofit_btn.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);background-color: rgb(255, 0, 128);"))
        self.autofit_btn.setObjectName(_fromUtf8("autofit_btn"))
        self.autofitting_layout.addWidget(self.autofit_btn)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 765, 850, 27))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        # self.ref_filename_lbl = QtGui.QLabel(self.horizontalLayoutWidget_3)
        # self.ref_filename_lbl.setMaximumSize(QtCore.QSize(145, 16777215))
        # self.ref_filename_lbl.setText(_fromUtf8(""))
        # self.ref_filename_lbl.setTextFormat(QtCore.Qt.RichText)
        # self.ref_filename_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.ref_filename_lbl.setWordWrap(False)
        # self.ref_filename_lbl.setMargin(2)
        # self.ref_filename_lbl.setObjectName(_fromUtf8("ref_filename_lbl"))
        # self.horizontalLayout.addWidget(self.ref_filename_lbl)
        # self.cy3_filename_lbl = QtGui.QLabel(self.horizontalLayoutWidget_3)
        # self.cy3_filename_lbl.setMaximumSize(QtCore.QSize(145, 16777215))
        # self.cy3_filename_lbl.setText(_fromUtf8(""))
        # self.cy3_filename_lbl.setTextFormat(QtCore.Qt.RichText)
        # self.cy3_filename_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.cy3_filename_lbl.setWordWrap(False)
        # self.cy3_filename_lbl.setMargin(2)
        # self.cy3_filename_lbl.setObjectName(_fromUtf8("cy3_filename_lbl"))
        # self.horizontalLayout.addWidget(self.cy3_filename_lbl)
        # self.cy5_filename_lbl = QtGui.QLabel(self.horizontalLayoutWidget_3)
        # self.cy5_filename_lbl.setMaximumSize(QtCore.QSize(145, 16777215))
        # self.cy5_filename_lbl.setText(_fromUtf8(""))
        # self.cy5_filename_lbl.setTextFormat(QtCore.Qt.RichText)
        # self.cy5_filename_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.cy5_filename_lbl.setWordWrap(False)
        # self.cy5_filename_lbl.setMargin(2)
        # self.cy5_filename_lbl.setObjectName(_fromUtf8("cy5_filename_lbl"))
        # self.horizontalLayout.addWidget(self.cy5_filename_lbl)
        # self.bkg_filename_lbl = QtGui.QLabel(self.horizontalLayoutWidget_3)
        # self.bkg_filename_lbl.setMaximumSize(QtCore.QSize(145, 16777215))
        # self.bkg_filename_lbl.setText(_fromUtf8(""))
        # self.bkg_filename_lbl.setTextFormat(QtCore.Qt.RichText)
        # self.bkg_filename_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.bkg_filename_lbl.setWordWrap(False)
        # self.bkg_filename_lbl.setMargin(2)
        # self.bkg_filename_lbl.setObjectName(_fromUtf8("bkg_filename_lbl"))
        # self.horizontalLayout.addWidget(self.bkg_filename_lbl)
        # self.direct_emission_lbl = QtGui.QLabel(self.horizontalLayoutWidget_3)
        # self.direct_emission_lbl.setMaximumSize(QtCore.QSize(145, 16777215))
        # self.direct_emission_lbl.setTextFormat(QtCore.Qt.RichText)
        # self.direct_emission_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.direct_emission_lbl.setWordWrap(False)
        # self.direct_emission_lbl.setMargin(2)
        # self.direct_emission_lbl.setObjectName(_fromUtf8("direct_emission_lbl"))
        # self.horizontalLayout.addWidget(self.direct_emission_lbl)
        # self.database_lbl = QtGui.QLabel(self.horizontalLayoutWidget_3)
        # self.database_lbl.setMaximumSize(QtCore.QSize(145, 16777215))
        # self.database_lbl.setTextFormat(QtCore.Qt.RichText)
        # self.database_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.database_lbl.setWordWrap(False)
        # self.database_lbl.setMargin(2)
        # self.database_lbl.setObjectName(_fromUtf8("database_lbl"))
        # self.horizontalLayout.addWidget(self.database_lbl)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionBatch_Fit = QtGui.QAction(MainWindow)
        self.actionBatch_Fit.setObjectName(_fromUtf8("actionBatch_Fit"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionBatch_Fit)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        ### Add Spectra and Residual View
        self.plot_widget = pg.PlotWidget(title='Spectra View')
        self.plot_widget.plotItem.showGrid(True, True, alpha=0.2)
        #self.plot_widget.plotItem.showAxis('right', show=True)
        self.plot_widget.plotItem.setLabel('bottom', text='Wavelength')
        self.plot_widget.plotItem.setLabel('left', text='Fluorescence Count')
        self.plot_widget.plotItem.setMouseEnabled(x=False, y=False)
        self.plot_widget_viewbox = self.plot_widget.plotItem.getViewBox()
        self.plot_widget.plotItem.enableAutoRange(axis=self.plot_widget_viewbox.XYAxes)
        # self.plot_widget.addLegend(offset=(575,1))
        self.plot_layout.addWidget(self.plot_widget)

        self.residual_widget = pg.PlotWidget()
        self.residual_widget.plotItem.showGrid(True, True)
        self.residual_widget.plotItem.hideAxis('bottom')
        self.residual_widget.plotItem.addLine(y=0, pen='w')
        self.residual_widget.plotItem.setLabel('left', text='Residual')
        self.residual_widget.plotItem.setMouseEnabled(x=False, y=False)
        self.residual_widget_viewbox = self.plot_widget.plotItem.getViewBox()
        self.residual_widget.plotItem.enableAutoRange(axis=self.residual_widget_viewbox.XYAxes)
        self.residual_layout.addWidget(self.residual_widget)

        # Region selection in spectra view
        self.region = pg.LinearRegionItem()
        self.plot_widget.addItem(self.region, ignoreBounds=True)
        self.region.sigRegionChanged.connect(self.regionChanged)
        self.retranslateUi(MainWindow)

        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Fytt", "Fytt", None))
        self.ref_btn.setText(_translate("MainWindow", "Reference Spectra", None))
        self.cy3_btn.setText(_translate("MainWindow", "Donor Basis Set", None))
        self.cy5_btn.setText(_translate("MainWindow", "Acceptor Basis Set", None))
        self.bkg_btn.setText(_translate("MainWindow", "Background Basis Set", None))
        self.save_btn.setText(_translate("MainWindow", "Save Fytt...", None))
        self.toolButton.setText(_translate("MainWindow", "...", None))
        self.cy3_ckbox.setText(_translate("MainWindow", "Donor", None))
        self.cy5_ckbox.setText(_translate("MainWindow", "Acceptor", None))
        self.bkg_ckbox.setText(_translate("MainWindow", "Background", None))
        self.offset_ckbox.setText(_translate("MainWindow", "Offset", None))
        self.donor_shift_cbx.setText(_translate("MainWindow", "Donor Shift", None))
        self.acceptor_shift_cbx.setText(_translate("MainWindow", "Acceptor Shift", None))
        self.label_5.setText(_translate("MainWindow", "FRET Index", None))
        self.fret_lbl.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">0.0</span></p></body></html>", None))
        self.label_7.setText(_translate("MainWindow", "Mean Square Error", None))
        self.err_lbl.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">0.0</span></p></body></html>", None))
        self.autofit_btn.setText(_translate("MainWindow", "Fytt", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionBatch_Fit.setText(_translate("MainWindow", "Batch Fytt...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        # self.ref_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.cy3_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.cy5_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.bkg_filename_lbl.setText(_translate("MainWindow", "...", None))
        # self.direct_emission_lbl.setText(_translate("MainWindow", "...", None))
        # self.database_lbl.setText(_translate("MainWindow", "db", None))
        self.direct_emission_btn.setText(_translate("MainWindow", "Direct Emission", None))
        self.loadBasisSets_btn.setText(_translate("MainWindow", "Basis sets Database", None))

        font = QtGui.QFont()
        font.setPointSize(14)
        self.save_btn.setFont(font)


        self.cy3_ckbox.setToolTip(_translate("MainWindow", "<html><head/><body><p>Checked state constrains the donor linear scaling factor to the value (Coarse + Fine) set below.</p></body></html>", None))
        self.cy3_spin.setToolTip(_translate("MainWindow", "<html><head/><body><p>Coarse adjustment for donor linear scaling factor (Step Size: 1000).</p></body></html>", None))
        self.cy3_slider.setToolTip(_translate("MainWindow", "<html><head/><body><p>Fine adjustment for donor linear scaling factor (Step Size: 1).</p></body></html>", None))

        self.cy5_ckbox.setToolTip(_translate("MainWindow", "<html><head/><body><p>Checked state constrains the acceptor linear scaling factor to the value (Coarse + Fine) set below.</p></body></html>", None))
        self.cy5_spin.setToolTip(_translate("MainWindow", "<html><head/><body><p>Coarse adjustment for acceptor linear scaling factor (Step Size: 1000).</p></body></html>", None))
        self.cy5_slider.setToolTip(_translate("MainWindow", "<html><head/><body><p>Fine adjustment for acceptor linear scaling factor (Step Size: 1).</p></body></html>", None))

        self.bkg_ckbox.setToolTip(_translate("MainWindow", "<html><head/><body><p>Checked state constrains the background linear scaling factor to the value (Coarse + Fine) set below.</p></body></html>", None))
        self.bkg_spin.setToolTip(_translate("MainWindow", "<html><head/><body><p>Coarse adjustment for background linear scaling factor (Step Size: 1000).</p></body></html>", None))
        self.bkg_slider.setToolTip(_translate("MainWindow", "<html><head/><body><p>Fine adjustment for background linear scaling factor (Step Size: 1).</p></body></html>", None))

        self.offset_ckbox.setToolTip(_translate("MainWindow", "<html><head/><body><p>Checked state constrains the Y offset to a value (Coarse + Fine) set below. This is equivalent of signal with buffer only measurement.</p></body></html>", None))
        self.offset_spin.setToolTip(_translate("MainWindow", "<html><head/><body><p>Coarse adjustment for Y offset (Step Size: 1000).</p></body></html>", None))
        self.offset_slider.setToolTip(_translate("MainWindow", "<html><head/><body><p>Fine adjustment for Y offset (Step Size: 1).</p></body></html>", None))
        # self.direct_emission_lbl.setToolTip(_translate("MainWindow", "<html><head/><body><p>Correction Factor for direct emission of acceptor signal</p></body></html>", None))
        self.acceptor_shift_cbx.setChecked(True)
        self.donor_shift_cbx.setChecked(True)
        self.acceptor_shift_spin.setValue(0)
        self.donor_shift_spin.setValue(0)

        #Define Connections
        self.ref_btn.clicked.connect(self.ref_clicked)
        self.cy3_btn.clicked.connect(self.cy3_clicked)
        self.cy5_btn.clicked.connect(self.cy5_clicked)
        self.bkg_btn.clicked.connect(self.bkg_clicked)
        self.save_btn.clicked.connect(self.save_clicked)
        self.autofit_btn.clicked.connect(self.autofit_clicked)
        self.direct_emission_btn.clicked.connect(self.directEmission_clicked)

        self.cy3_btn.setEnabled(False)
        self.cy5_btn.setEnabled(False)
        self.bkg_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.direct_emission_btn.setEnabled(False)
        self.loadBasisSets_btn.setEnabled(False)
        self.autofit_btn.setEnabled(False)

        self.cy3_spin.setEnabled(False)
        self.cy5_spin.setEnabled(False)
        self.bkg_spin.setEnabled(False)
        self.offset_spin.setEnabled(False)

        self.cy3_slider.setEnabled(False)
        self.cy5_slider.setEnabled(False)
        self.bkg_slider.setEnabled(False)
        self.offset_slider.setEnabled(False)

        self.acceptor_shift_cbx.setEnabled(False)
        self.acceptor_shift_spin.setEnabled(False)
        self.donor_shift_cbx.setEnabled(False)
        self.donor_shift_spin.setEnabled(False)

        self.cy3_spin.valueChanged.connect(self.cy3_valueChanged)
        self.cy5_spin.valueChanged.connect(self.cy5_valueChanged)
        self.bkg_spin.valueChanged.connect(self.bkg_valueChanged)
        self.offset_spin.valueChanged.connect(self.offset_valueChanged)

        self.cy3_slider.valueChanged.connect(self.cy3_valueChanged)
        self.cy5_slider.valueChanged.connect(self.cy5_valueChanged)
        self.bkg_slider.valueChanged.connect(self.bkg_valueChanged)
        self.offset_slider.valueChanged.connect(self.offset_valueChanged)

        self.acceptor_shift_spin.valueChanged.connect(self.acceptor_shift_valueChanged)
        self.donor_shift_spin.valueChanged.connect(self.donor_shift_valueChanged)

        self.toolButton.clicked.connect(self.actionAboutFunction)
        self.actionAbout.triggered.connect(self.actionAboutFunction)
        self.actionBatch_Fit.triggered.connect(self.actionBatchFitFunction)
        self.plot_widget_viewbox.sigXRangeChanged.connect(self.sync_xranges)
        self.loadBasisSets_btn.clicked.connect(self.openBasisSetDatabase)

    # def test_function(self):
    #     self.spectra.reference = self.spectra.read_spectra('./basis_sets/reference.dat', False)
    #     self.plot_reference()
    #     self.plot_widget.plotItem.setTitle('./basis_sets/Reference.dat')
    #
    #     self.spectra.calculateRegionBounds()
    #     self.region.setBounds([self.spectra.lowBound, self.spectra.highBound])
    #     self.region.setRegion([self.spectra.lowSelection, self.spectra.highSelection])
    #     self.spectra.calculateRegionIndex(self.spectra.lowSelection, self.spectra.highSelection)
    #
    #     self.cy3_btn.setEnabled(True)
    #     self.cy5_btn.setEnabled(True)
    #     self.bkg_btn.setEnabled(True)
    #
    #     self.spectra.cy3_basis = self.spectra.read_spectra('./basis_sets/donor_basis.dat')
    #     (self.spectra.cy3_basis_scaled, scale_factor) = self.spectra.rescale_basis(self.spectra.reference, self.spectra.cy3_basis, self.spectra.getX_forYmax(self.spectra.cy3_basis))
    #     self.plot_cy3()
    #     self.autofit_btn.setEnabled(True)
    #     self.save_btn.setEnabled(True)
    #     self.offset_spin.setEnabled(True)
    #     self.offset_slider.setEnabled(True)
    #     self.cy3_spin.setValue(scale_factor)
    #     self.cy3_spin.setEnabled(True)
    #     self.cy3_slider.setEnabled(True)
    #
    #     self.spectra.cy5_basis = self.spectra.read_spectra('./basis_sets/acceptor_basis.dat')
    #     (self.spectra.cy5_basis_scaled, scale_factor) = self.spectra.rescale_basis(self.spectra.reference, self.spectra.cy5_basis, self.spectra.getX_forYmax(self.spectra.cy5_basis))
    #     self.cy5_spin.setValue(scale_factor)
    #     self.cy5_spin.setEnabled(True)
    #     self.cy5_slider.setEnabled(True)
    #     self.plot_cy5()
    #
    #     self.spectra.bkg_basis = self.spectra.read_spectra('./basis_sets/background_basis.dat')
    #     (self.spectra.bkg_basis_scaled, scale_factor) = self.spectra.rescale_basis(self.spectra.reference, self.spectra.bkg_basis, min(list(self.spectra.bkg_basis['x'])))
    #     self.plot_bkg()
    #     self.bkg_spin.setValue(scale_factor)
    #     self.bkg_spin.setEnabled(True)
    #     self.bkg_slider.setEnabled(True)
    #
    #     self.calculate_sum()
    #     self.calculate_residuals()
    #     self.plot_sum()
    #     self.plot_residual()
