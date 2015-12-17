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
import sqlite3 as lite
import numpy as np
import cPickle as pickle
import sys, re
import pyqtgraph as pg
from basis import Basis
import interpolation
from insertdb import DB_Dialog
import functools

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

class BasisGui(QtGui.QDialog):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        if sys.platform == 'darwin':
            self.db_path = "db/fytt_db.sqlite3"
        elif sys.platform == 'linux2' or sys.platform == 'linux':
             self.db_path = "fytt_db.sqlite3"
        elif sys.platform == 'win32':
             self.db_path = "fytt_db.sqlite3"
        
        self.db_handle = lite.connect(self.db_path, isolation_level=None)
        self.db_cursor = self.db_handle.cursor()
        self.setupBasisSets()
        self.setupLamps()
        self.donorSelection = []
        self.acceptorSelection = []
        self.backgroundSelection = []
        self.lampSelection = 0
        self.basis_sets = Basis()
        self.donorExPlot = pg.PlotDataItem()
        self.acceptorExPlot = pg.PlotDataItem()
        self.donorEmPlot = pg.PlotDataItem()
        self.acceptorEmPlot = pg.PlotDataItem()
        self.backgroundPlot = pg.PlotDataItem()
        self.acceptorPlotLine = pg.InfiniteLine()
        self.donorPlotLine = pg.InfiniteLine()
        self.mainWindow = ''
        self.manualCorrectionCheckState()

    def setupBasisSets(self):
        self.model_donor = QtGui.QStandardItemModel()
        self.model_acceptor = QtGui.QStandardItemModel()
        self.model_background = QtGui.QStandardItemModel()
        self.db_cursor.execute("SELECT * FROM attributes WHERE type=?", ('m',))
        attribute_rows = self.db_cursor.fetchall()
        self.db_cursor.execute("SELECT * FROM backgrounds")
        background_rows = self.db_cursor.fetchall()
        for row in attribute_rows:
            if not re.match('^\s+', row[2]):
                name = ''
                if not row[4] == '':
                    name = QtGui.QStandardItem("{0} in {1}".format(row[2], row[4])) if not re.match('pH', row[4]) else QtGui.QStandardItem("{0} at {1}".format(row[2], row[4]))
                    name.setToolTip('{0} ({1}) in {2}'.format(row[1], row[2], row[4]))
                else:
                    name = QtGui.QStandardItem("{0}".format(row[2]))
                    name.setToolTip('{0} ({1})'.format(row[1], row[2]))
                name.setData(row[1])
                name.setEditable(False)
                self.model_donor.invisibleRootItem().appendRow([name])
                if not row[4] == '':
                    name = QtGui.QStandardItem("{0} in {1}".format(row[2], row[4])) if not re.match('pH', row[4]) else QtGui.QStandardItem("{0} at {1}".format(row[2], row[4]))
                    name.setToolTip('{0} ({1}) in {2}'.format(row[1], row[2], row[4]))
                else:
                    name = QtGui.QStandardItem("{0}".format(row[2]))
                    name.setToolTip('{0} ({1})'.format(row[1], row[2]))
                name.setData(row[1])
                name.setEditable(False)
                self.model_acceptor.invisibleRootItem().appendRow([name])

        for row in background_rows:
            name = QtGui.QStandardItem("{0} in {1}".format(row[2], row[3])) if not re.match('pH', row[3]) else QtGui.QStandardItem("{0} at {1}".format(row[2], row[3]))
            name.setToolTip('{0} ({1}) in {2}'.format(row[1], row[2], row[3]))
            name.setData(row[0])
            self.model_background.invisibleRootItem().appendRow([name])

        self.proxy_donor = QtGui.QSortFilterProxyModel(self)
        self.proxy_acceptor = QtGui.QSortFilterProxyModel(self)
        self.proxy_background = QtGui.QSortFilterProxyModel(self)
        self.proxy_donor.setSourceModel(self.model_donor)
        self.proxy_acceptor.setSourceModel(self.model_acceptor)
        self.proxy_background.setSourceModel(self.model_background)
        self.donor_list.setModel(self.proxy_donor)
        self.acceptor_list.setModel(self.proxy_acceptor)
        self.background_list.setModel(self.proxy_background)

        self.donor_list.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.donor_list.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.donorSelectionModel = self.donor_list.selectionModel()
        self.connect(self.donorSelectionModel, QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.donorSelected)

        self.acceptor_list.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.acceptor_list.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.acceptorSelectionModel = self.acceptor_list.selectionModel()
        self.connect(self.acceptorSelectionModel, QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.acceptorSelected)

        self.background_list.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.background_list.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.backgroundSelectionModel = self.background_list.selectionModel()
        self.connect(self.backgroundSelectionModel, QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.backgroundSelected)

    def setupLamps(self):
        self.db_cursor.execute("SELECT * FROM lamps")
        self.lamp_data = []
        self.lamp_data = self.db_cursor.fetchall()
        self.lamp_box.clear()
        for row in self.lamp_data:
            self.lamp_box.addItem("{0}".format(row[1]))
        self.lamp_box.currentIndexChanged.connect(self.lampselectionChanged)

    def lampselectionChanged(self, index):
        self.lampSelection = index
        self.basis_sets.lamp['x'] = pickle.loads(str(self.lamp_data[index][2]))
        self.basis_sets.lamp['y'] = pickle.loads(str(self.lamp_data[index][3]))
        self.calculateLampIntRatio()

    def calculateLampIntRatio(self):
        if len(self.basis_sets.lamp['x']) > 0 and self.donorExcitation_spin.value() > 1.0 and self.acceptorExcitation_spin.value() > 1.0:
            left = self.slitWidth_spin.value()/2 * -1
            right = self.slitWidth_spin.value()/2
            valueAtDonorEx = interpolation.get_interpolated_val(self.basis_sets.lamp, self.donorExcitation_spin.value()) + interpolation.get_interpolated_val(self.basis_sets.lamp, self.donorExcitation_spin.value() + left) + interpolation.get_interpolated_val(self.basis_sets.lamp, self.donorExcitation_spin.value() + right)
            valueAtAcceptorEx = interpolation.get_interpolated_val(self.basis_sets.lamp, self.acceptorExcitation_spin.value()) + interpolation.get_interpolated_val(self.basis_sets.lamp, self.acceptorExcitation_spin.value() + left) + interpolation.get_interpolated_val(self.basis_sets.lamp, self.acceptorExcitation_spin.value() + right)
            self.basis_sets.lampIntensityRatio = valueAtDonorEx/valueAtAcceptorEx
            self.calculateDirectExcitation()

    def donorSelected(self, selected, deselected):
        selected = self.proxy_donor.mapSelectionToSource(selected)
        selected_name = self.model_donor.item(selected.indexes()[0].row()).data().toString()
        self.donorSelection = []
        try:
            self.db_cursor.execute("SELECT * FROM spectra WHERE name=? AND type=?", (str(selected_name),'x',))
            db_row = self.db_cursor.fetchall()
            self.donorSelection.append(db_row[0][0])
            xvalues = pickle.loads(str(db_row[0][3]))
            yvalues = pickle.loads(str(db_row[0][4]))
            lambda_max = xvalues[np.argmax(np.array(yvalues))]
            self.basis_sets.setDonorEx(xvalues, yvalues)
            self.donorExcitation_spin.setValue(xvalues[np.argmax(np.array(yvalues))])
            self.plotDonor(lambda_max)
            self.calculateLampIntRatio()
        except IndexError:
            pass

        try:
            self.db_cursor.execute("SELECT * FROM spectra WHERE name=? AND type=?", (str(selected_name),'m',))
            db_row = self.db_cursor.fetchall()
            self.donorSelection.append(db_row[0][0])
            xvalues = pickle.loads(str(db_row[0][3]))
            yvalues = pickle.loads(str(db_row[0][4]))
            self.basis_sets.setDonorEm(xvalues, yvalues, str(db_row[0][1]))
            self.plotDonorEmission()
        except IndexError:
            pass


    def acceptorSelected(self, selected, deselected):
        selected = self.proxy_acceptor.mapSelectionToSource(selected)
        selected_name = self.model_acceptor.item(selected.indexes()[0].row()).data().toString()
        self.acceptorSelection = []
        try:
            self.db_cursor.execute("SELECT * FROM spectra WHERE name=? AND type=?", (str(selected_name),'x',))
            db_row = self.db_cursor.fetchall()
            self.acceptorSelection.append(db_row[0][0])
            xvalues = pickle.loads(str(db_row[0][3]))
            yvalues = pickle.loads(str(db_row[0][4]))
            lambda_max = xvalues[np.argmax(np.array(yvalues))]
            self.basis_sets.setAcceptorEx(xvalues, yvalues)
            self.acceptorExcitation_spin.setValue(lambda_max)
            self.plotAcceptor(lambda_max)
            self.calculateLampIntRatio()
        except IndexError:
            pass

        try:
            self.db_cursor.execute("SELECT * FROM spectra WHERE name=? AND type=?", (str(selected_name),'m',))
            db_row = self.db_cursor.fetchall()
            self.acceptorSelection.append(db_row[0][0])
            xvalues = pickle.loads(str(db_row[0][3]))
            yvalues = pickle.loads(str(db_row[0][4]))
            self.basis_sets.setAcceptorEm(xvalues, yvalues, str(db_row[0][1]))
            self.plotAcceptorEmission()
        except IndexError:
            pass

    def backgroundSelected(self, selected, deselected):
        selected = self.proxy_background.mapSelectionToSource(selected)
        selected_index = self.model_background.item(selected.indexes()[0].row()).data().toInt()[0]
        self.backgroundSelection = []
        try:
            self.db_cursor.execute("SELECT * FROM spectra WHERE id=?", (selected_index,))
            db_row = self.db_cursor.fetchall()
            self.backgroundSelection.append(db_row[0][0])
            xvalues = pickle.loads(str(db_row[0][3]))
            yvalues = pickle.loads(str(db_row[0][4]))
            self.basis_sets.setBackground(xvalues, yvalues, str(db_row[0][1]))
            self.plotBackground()
        except IndexError:
            pass

    def sendBasisSetsToMainWindow(self):
        self.mainWindow.donor_shift_spin.setValue(0.0)
        self.mainWindow.acceptor_shift_spin.setValue(0.0)
        self.mainWindow.spectra.cy3_basis = self.basis_sets.donorEmission
        self.mainWindow.spectra.cy3FileName = self.basis_sets.donorName
        (self.mainWindow.spectra.cy3_basis_scaled, self.mainWindow.spectra.cy3_scaleFactor) = self.mainWindow.spectra.rescale_basis(self.mainWindow.spectra.reference, self.mainWindow.spectra.cy3_basis, self.mainWindow.spectra.getX_forYmax(self.mainWindow.spectra.cy3_basis))
        self.mainWindow.load_cy3(load=0)
        self.mainWindow.spectra.cy5_basis = self.basis_sets.acceptorEmission
        self.mainWindow.spectra.cy5FileName = self.basis_sets.acceptorName
        (self.mainWindow.spectra.cy5_basis_scaled, self.mainWindow.spectra.cy5_scaleFactor) = self.mainWindow.spectra.rescale_basis(self.mainWindow.spectra.reference, self.mainWindow.spectra.cy5_basis, self.mainWindow.spectra.getX_forYmax(self.mainWindow.spectra.cy5_basis))
        self.mainWindow.load_cy5(load=0)
        self.mainWindow.spectra.bkg_basis = self.basis_sets.background
        self.mainWindow.spectra.bkgFileName = self.basis_sets.backgroundName
        (self.mainWindow.spectra.bkg_basis_scaled, self.mainWindow.spectra.bkg_scaleFactor) = self.mainWindow.spectra.rescale_basis(self.mainWindow.spectra.reference, self.mainWindow.spectra.bkg_basis, self.mainWindow.spectra.getX_forYmax(self.mainWindow.spectra.bkg_basis))
        self.mainWindow.load_bkg(load=0)
        self.mainWindow.spectra.cy5_correction['x'] = self.basis_sets.acceptorEmission['x']
        self.mainWindow.spectra.cy5_correction['y'] = list(np.zeros(len(self.basis_sets.acceptorEmission['x'])))

    def sendDirectExcitationtoMainWindow(self):
        self.mainWindow.spectra.correctionFactor = self.basis_sets.correctionFactor
        self.mainWindow.label_5.setText(_translate("MainWindow", "FRET Efficiency", None))
        self.mainWindow.direct_emission_btn.setEnabled(True)
        self.mainWindow.direct_emission_lbl.setText(_translate("MainWindow", "Corr. Factor : %.2f" % self.basis_sets.correctionFactor, None))
        if len(self.mainWindow.spectra.directEmission.keys()) == 0:
            self.mainWindow.directEmission_clicked()
        else:
            self.mainWindow.scale_directEmission()

    def calculateDirectExcitation(self):
        if self.acceptorExcitation_spin.value() > 1.0 and self.donorExcitation_spin.value() > 1.0 and self.basis_sets.lampIntensityRatio > 0.0:
            left = self.slitWidth_spin.value() * -1 / 2
            right = self.slitWidth_spin.value()/2
            numerator = interpolation.get_interpolated_val(self.basis_sets.acceptorExcitation, self.donorExcitation_spin.value()) + interpolation.get_interpolated_val(self.basis_sets.acceptorExcitation, self.donorExcitation_spin.value() + left) + interpolation.get_interpolated_val(self.basis_sets.acceptorExcitation, self.donorExcitation_spin.value() + right)
            denominator = interpolation.get_interpolated_val(self.basis_sets.acceptorExcitation, self.acceptorExcitation_spin.value()) + interpolation.get_interpolated_val(self.basis_sets.acceptorExcitation, self.acceptorExcitation_spin.value() + left) + interpolation.get_interpolated_val(self.basis_sets.acceptorExcitation, self.acceptorExcitation_spin.value() + right)
            self.basis_sets.correctionFactor = 1/self.basis_sets.lampIntensityRatio * (numerator/denominator)
            self.outputCorrectionFactor()

    def outputCorrectionFactor(self):
        self.setDirectExcitation_btn.setText(_translate("BasisGui", "Set Emission Correction Factor (%.2f)" % self.basis_sets.correctionFactor, None))

    def deleteSpectraFromDatabase(self, className):
        if className == 'd':
            for i in self.donorSelection:
                self.db_cursor.execute("DELETE FROM attributes WHERE id=?", (i,))
                self.db_cursor.execute("DELETE FROM spectra WHERE id=?", (i,))
            self.donorSelection = []
            self.donorEmPlot.clear()
            self.donorExPlot.clear()
            self.setupBasisSets()
        elif className == 'a':
            for i in self.acceptorSelection:
                self.db_cursor.execute("DELETE FROM attributes WHERE id=?", (i,))
                self.db_cursor.execute("DELETE FROM spectra WHERE id=?", (i,))
            self.acceptorSelection = []
            self.acceptorExPlot.clear()
            self.acceptorEmPlot.clear()
            self.setupBasisSets()
        elif className == 'b':
            for i in self.backgroundSelection:
                self.db_cursor.execute("DELETE FROM backgrounds WHERE id=?", (i,))
                self.db_cursor.execute("DELETE FROM spectra WHERE id=?", (i,))
            self.backgroundPlot.clear()
            self.setupBasisSets()
        elif className == 'l':
            self.db_cursor.execute("DELETE FROM lamps WHERE id=?", (self.lampSelection,))
            self.setupLamps()
        self.db_handle.commit()

    def loadSpectraIntoDatabase(self, className):
        print "Loading Spectra Into Database"
        db_dialog = DB_Dialog(className)
        returnVal = db_dialog.exec_()
        self.setupBasisSets()
        self.setupLamps()

    @QtCore.pyqtSlot()
    def plotBackground(self):
        background_color = pg.mkPen({'color': '999999', 'width': 2, 'style': QtCore.Qt.DotLine})
        self.backgroundPlot.clear()
        yvalues = list(np.divide(self.basis_sets.background['y'], np.max(np.array(self.basis_sets.background['y']))))
        self.backgroundPlot = self.preview_widget.plot(list(self.basis_sets.background['x']), yvalues, pen=background_color, antialias=True)

    @QtCore.pyqtSlot()
    def plotDonor(self, lmax):
        donor_color = pg.mkPen({'color': '31C9E8', 'width': 2})
        self.donorExPlot.clear()
        if self.donorPlotLine.value() == 0:
            donor_linecolor = pg.mkPen({'color': '31C9E8', 'width': 2, 'style': QtCore.Qt.DotLine})
            self.donorPlotLine = self.preview_widget.addLine(x=lmax, pen=donor_linecolor)
        else:
            self.donorPlotLine.setValue(lmax)
        yvalues = list(np.divide(self.basis_sets.donorExcitation['y'], np.max(np.array(self.basis_sets.donorExcitation['y']))))
        self.donorExPlot = self.preview_widget.plot(list(self.basis_sets.donorExcitation['x']), yvalues, pen=donor_color, antialias=True)

    @QtCore.pyqtSlot()
    def plotDonorEmission(self):
        donor_color = pg.mkPen({'color': '31C9E8', 'width': 2, 'style': QtCore.Qt.DashLine})
        self.donorEmPlot.clear()
        yvalues = list(np.divide(self.basis_sets.donorEmission['y'], np.max(np.array(self.basis_sets.donorEmission['y']))))
        self.donorEmPlot = self.preview_widget.plot(list(self.basis_sets.donorEmission['x']), yvalues, pen=donor_color, antialias=True)

    @QtCore.pyqtSlot()
    def plotAcceptor(self, lmax):
        acceptor_color = pg.mkPen({'color': 'E85031', 'width': 2})
        self.acceptorExPlot.clear()
        if self.acceptorPlotLine.value() == 0:
            acceptor_linecolor = pg.mkPen({'color': 'E85031', 'width': 2, 'style': QtCore.Qt.DotLine})
            self.acceptorPlotLine = self.preview_widget.addLine(x=lmax, pen=acceptor_linecolor)
        else:
            self.acceptorPlotLine.setValue(lmax)
        yvalues = list(np.divide(self.basis_sets.acceptorExcitation['y'], np.max(np.array(self.basis_sets.acceptorExcitation['y']))))
        self.acceptorExPlot = self.preview_widget.plot(list(self.basis_sets.acceptorExcitation['x']), yvalues, pen=acceptor_color, antialias=True)

    @QtCore.pyqtSlot()
    def plotAcceptorEmission(self):
        acceptor_color = pg.mkPen({'color': 'E85031', 'width': 2, 'style': QtCore.Qt.DashLine})
        self.acceptorEmPlot.clear()
        yvalues = list(np.divide(self.basis_sets.acceptorEmission['y'], np.max(np.array(self.basis_sets.acceptorEmission['y']))))
        self.acceptorEmPlot = self.preview_widget.plot(list(self.basis_sets.acceptorEmission['x']), yvalues, pen=acceptor_color, antialias=True)

    @QtCore.pyqtSlot()
    def acceptorExcitationChanged(self):
        if self.acceptorPlotLine.value() == 0:
            acceptor_linecolor = pg.mkPen({'color': 'E85031', 'width': 2, 'style': QtCore.Qt.DotLine})
            self.acceptorPlotLine = self.preview_widget.addLine(x=self.acceptorExcitation_spin.value(), pen=acceptor_linecolor)
        else:
            self.acceptorPlotLine.setValue(self.acceptorExcitation_spin.value())
        self.calculateDirectExcitation()

    @QtCore.pyqtSlot()
    def donorExcitationChanged(self):
        if self.donorPlotLine.value() == 0:
            donor_linecolor = pg.mkPen({'color': '31C9E8', 'width': 2, 'style': QtCore.Qt.DotLine})
            self.donorPlotLine = self.preview_widget.addLine(x=self.donorExcitation_spin.value(), pen=donor_linecolor)
        else:
            self.donorPlotLine.setValue(self.donorExcitation_spin.value())
        self.calculateDirectExcitation()

    def setupUi(self, BasisGui):
        BasisGui.setObjectName(_fromUtf8("BasisGui"))
        BasisGui.resize(800, 770)
        BasisGui.setMinimumSize(QtCore.QSize(800, 770))
        BasisGui.setMaximumSize(QtCore.QSize(800, 770))
        BasisGui.setMouseTracking(False)
        self.layoutWidget = QtGui.QWidget(BasisGui)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 330, 761, 23))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.namesLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.namesLayout.setMargin(0)
        self.namesLayout.setObjectName(_fromUtf8("namesLayout"))
        self.donor_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.donor_lbl.setFont(font)
        self.donor_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.donor_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.donor_lbl.setObjectName(_fromUtf8("donor_lbl"))
        self.namesLayout.addWidget(self.donor_lbl)
        self.acceptor_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.acceptor_lbl.setFont(font)
        self.acceptor_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.acceptor_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acceptor_lbl.setObjectName(_fromUtf8("acceptor_lbl"))
        self.namesLayout.addWidget(self.acceptor_lbl)
        self.background_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.background_lbl.setFont(font)
        self.background_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.background_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.background_lbl.setObjectName(_fromUtf8("background_lbl"))
        self.namesLayout.addWidget(self.background_lbl)
        self.horizontalLayoutWidget = QtGui.QWidget(BasisGui)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 629, 741, 20))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_1 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_1.setMargin(0)
        self.horizontalLayout_1.setObjectName(_fromUtf8("horizontalLayout_1"))
        self.line = QtGui.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_1.addWidget(self.line)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(BasisGui)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 700, 741, 16))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.line_2 = QtGui.QFrame(self.horizontalLayoutWidget_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_2.addWidget(self.line_2)
        self.layoutWidget1 = QtGui.QWidget(BasisGui)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 668, 761, 33))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.wavelengthLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.wavelengthLayout.setMargin(0)
        self.wavelengthLayout.setObjectName(_fromUtf8("wavelengthLayout"))
        self.donorExcitation_spin = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.donorExcitation_spin.setMinimum(1.0)
        self.donorExcitation_spin.setMaximum(1400.0)
        self.donorExcitation_spin.setObjectName(_fromUtf8("donorExcitation_spin"))
        self.wavelengthLayout.addWidget(self.donorExcitation_spin)
        self.line_3 = QtGui.QFrame(self.layoutWidget1)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.wavelengthLayout.addWidget(self.line_3)
        self.acceptorExcitation_spin = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.acceptorExcitation_spin.setMinimum(1.0)
        self.acceptorExcitation_spin.setMaximum(1400.0)
        self.acceptorExcitation_spin.setObjectName(_fromUtf8("acceptorExcitation_spin"))
        self.wavelengthLayout.addWidget(self.acceptorExcitation_spin)
        self.line_4 = QtGui.QFrame(self.layoutWidget1)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.wavelengthLayout.addWidget(self.line_4)
        self.slitWidth_spin = QtGui.QSpinBox(self.layoutWidget1)
        self.slitWidth_spin.setMinimum(2)
        self.slitWidth_spin.setMaximum(10)
        self.slitWidth_spin.setObjectName(_fromUtf8("spinBox"))
        self.wavelengthLayout.addWidget(self.slitWidth_spin)
        self.layoutWidget2 = QtGui.QWidget(BasisGui)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 390, 761, 151))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.tablesLayout = QtGui.QHBoxLayout(self.layoutWidget2)
        self.tablesLayout.setMargin(0)
        self.tablesLayout.setObjectName(_fromUtf8("tablesLayout"))
        self.donor_list = QtGui.QTableView(self.layoutWidget2)
        self.donor_list.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.donor_list.setShowGrid(True)
        self.donor_list.setWordWrap(True)
        self.donor_list.verticalHeader().setVisible(False)
        self.donor_list.horizontalHeader().setVisible(False)
        self.donor_list.setObjectName(_fromUtf8("donor_list"))
        self.tablesLayout.addWidget(self.donor_list)
        self.acceptor_list = QtGui.QTableView(self.layoutWidget2)
        self.acceptor_list.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.acceptor_list.setShowGrid(True)
        self.acceptor_list.setWordWrap(True)
        self.acceptor_list.verticalHeader().setVisible(False)
        self.acceptor_list.horizontalHeader().setVisible(False)
        self.acceptor_list.setObjectName(_fromUtf8("acceptor_list"))
        self.tablesLayout.addWidget(self.acceptor_list)
        self.background_list = QtGui.QTableView(self.layoutWidget2)
        self.background_list.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.background_list.setShowGrid(True)
        self.background_list.setWordWrap(True)
        self.background_list.verticalHeader().setVisible(False)
        self.background_list.horizontalHeader().setVisible(False)
        self.background_list.setObjectName(_fromUtf8("background_list"))
        self.tablesLayout.addWidget(self.background_list)
        self.layoutWidget3 = QtGui.QWidget(BasisGui)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 648, 761, 23))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.wavelengthLabelLayout = QtGui.QHBoxLayout(self.layoutWidget3)
        self.wavelengthLabelLayout.setMargin(0)
        self.wavelengthLabelLayout.setObjectName(_fromUtf8("wavelengthLabelLayout"))
        self.donorEx_lbl = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.donorEx_lbl.setFont(font)
        self.donorEx_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.donorEx_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.donorEx_lbl.setObjectName(_fromUtf8("donorEx_lbl"))
        self.wavelengthLabelLayout.addWidget(self.donorEx_lbl)
        self.acceptorEx_lbl = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.acceptorEx_lbl.setFont(font)
        self.acceptorEx_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.acceptorEx_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acceptorEx_lbl.setObjectName(_fromUtf8("acceptorEx_lbl"))
        self.wavelengthLabelLayout.addWidget(self.acceptorEx_lbl)
        self.slitWidth_lbl = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.slitWidth_lbl.setFont(font)
        self.slitWidth_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.slitWidth_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.slitWidth_lbl.setObjectName(_fromUtf8("slitWidth_lbl"))
        self.wavelengthLabelLayout.addWidget(self.slitWidth_lbl)
        self.layoutWidget4 = QtGui.QWidget(BasisGui)
        self.layoutWidget4.setGeometry(QtCore.QRect(20, 598, 761, 33))
        self.layoutWidget4.setObjectName(_fromUtf8("layoutWidget4"))
        self.loadLayout = QtGui.QHBoxLayout(self.layoutWidget4)
        self.loadLayout.setMargin(0)
        self.loadLayout.setObjectName(_fromUtf8("loadLayout"))
        self.correctionFactor_cbx = QtGui.QCheckBox(self.layoutWidget4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.correctionFactor_cbx.setFont(font)
        self.correctionFactor_cbx.setObjectName(_fromUtf8("correctionFactor_cbx"))
        self.loadLayout.addWidget(self.correctionFactor_cbx)
        self.correctionFactor_spin = QtGui.QDoubleSpinBox(self.layoutWidget4)
        self.correctionFactor_spin.setMinimum(0.00)
        self.correctionFactor_spin.setMaximum(1.00)
        self.correctionFactor_spin.setSingleStep(0.01)
        self.correctionFactor_spin.setObjectName(_fromUtf8("correctionFactor_spin"))
        self.loadLayout.addWidget(self.correctionFactor_spin)
        self.line_5 = QtGui.QFrame(self.layoutWidget4)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.loadLayout.addWidget(self.line_5)
        self.lamp_lbl = QtGui.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lamp_lbl.setFont(font)
        self.lamp_lbl.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lamp_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lamp_lbl.setObjectName(_fromUtf8("lamp_lbl"))
        self.loadLayout.addWidget(self.lamp_lbl)
        self.lamp_box = QtGui.QComboBox(self.layoutWidget4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lamp_box.sizePolicy().hasHeightForWidth())
        self.lamp_box.setSizePolicy(sizePolicy)
        self.lamp_box.setMinimumSize(QtCore.QSize(200, 0))
        self.lamp_box.setObjectName(_fromUtf8("lamp_box"))
        self.loadLayout.addWidget(self.lamp_box)
        self.addLamp = QtGui.QToolButton(self.layoutWidget4)
        self.addLamp.setObjectName(_fromUtf8("addLamp"))
        self.loadLayout.addWidget(self.addLamp)
        self.deleteLamp = QtGui.QToolButton(self.layoutWidget4)
        self.deleteLamp.setObjectName(_fromUtf8("deleteLamp"))
        self.loadLayout.addWidget(self.deleteLamp)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(BasisGui)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 578, 741, 20))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.line_7 = QtGui.QFrame(self.horizontalLayoutWidget_3)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.horizontalLayout_3.addWidget(self.line_7)
        self.layoutWidget5 = QtGui.QWidget(BasisGui)
        self.layoutWidget5.setGeometry(QtCore.QRect(20, 356, 761, 33))
        self.layoutWidget5.setObjectName(_fromUtf8("layoutWidget5"))
        self.filterLayout = QtGui.QHBoxLayout(self.layoutWidget5)
        self.filterLayout.setMargin(0)
        self.filterLayout.setObjectName(_fromUtf8("filterLayout"))
        self.donor_filter = QtGui.QLineEdit(self.layoutWidget5)
        self.donor_filter.setMinimumSize(QtCore.QSize(226, 0))
        self.donor_filter.setToolTip(_fromUtf8(""))
        self.donor_filter.setText(_fromUtf8(""))
        self.donor_filter.setObjectName(_fromUtf8("donor_filter"))
        self.filterLayout.addWidget(self.donor_filter)
        self.acceptor_filter = QtGui.QLineEdit(self.layoutWidget5)
        self.acceptor_filter.setMinimumSize(QtCore.QSize(226, 0))
        self.acceptor_filter.setObjectName(_fromUtf8("acceptor_filter"))
        self.filterLayout.addWidget(self.acceptor_filter)
        self.background_filter = QtGui.QLineEdit(self.layoutWidget5)
        self.background_filter.setMinimumSize(QtCore.QSize(226, 0))
        self.background_filter.setObjectName(_fromUtf8("background_filter"))
        self.filterLayout.addWidget(self.background_filter)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(BasisGui)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(19, 19, 761, 301))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.previewLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.previewLayout.setMargin(0)
        self.previewLayout.setObjectName(_fromUtf8("previewLayout"))
        self.preview_widget = pg.PlotWidget(title='Preview')
        self.preview_widget.plotItem.showGrid(True, True, alpha=0.2)
        self.preview_widget.plotItem.showAxis('right', show=True)
        self.preview_widget.plotItem.setLabel('bottom', text='Wavelength')
        self.preview_widget.plotItem.setLabel('left', text='Normalized Fluorescence')
        self.preview_widget.plotItem.setMouseEnabled(x=False, y=False)
        self.preview_widget_viewbox = self.preview_widget.plotItem.getViewBox()
        self.preview_widget.plotItem.enableAutoRange(axis=self.preview_widget_viewbox.XYAxes)
        self.previewLayout.addWidget(self.preview_widget)
        self.gridLayoutWidget = QtGui.QWidget(BasisGui)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 540, 761, 31))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.deleteAcceptor = QtGui.QToolButton(self.gridLayoutWidget)
        self.deleteAcceptor.setObjectName(_fromUtf8("deleteAcceptor"))
        self.gridLayout.addWidget(self.deleteAcceptor, 0, 4, 1, 1)
        self.deleteBackground = QtGui.QToolButton(self.gridLayoutWidget)
        self.deleteBackground.setObjectName(_fromUtf8("deleteBackground"))
        self.gridLayout.addWidget(self.deleteBackground, 0, 7, 1, 1)
        self.addAcceptor = QtGui.QToolButton(self.gridLayoutWidget)
        self.addAcceptor.setObjectName(_fromUtf8("addAcceptor"))
        self.gridLayout.addWidget(self.addAcceptor, 0, 3, 1, 1)
        self.deleteDonor = QtGui.QToolButton(self.gridLayoutWidget)
        self.deleteDonor.setObjectName(_fromUtf8("deleteDonor"))
        self.gridLayout.addWidget(self.deleteDonor, 0, 1, 1, 1)
        self.addDonor = QtGui.QToolButton(self.gridLayoutWidget)
        self.addDonor.setObjectName(_fromUtf8("addDonor"))
        self.gridLayout.addWidget(self.addDonor, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.addBackground = QtGui.QToolButton(self.gridLayoutWidget)
        self.addBackground.setObjectName(_fromUtf8("addBackground"))
        self.gridLayout.addWidget(self.addBackground, 0, 6, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.horizontalLayoutWidget_5 = QtGui.QWidget(BasisGui)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(20, 720, 761, 44))
        self.horizontalLayoutWidget_5.setObjectName(_fromUtf8("horizontalLayoutWidget_5"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.setDirectExcitation_btn = QtGui.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setDirectExcitation_btn.setFont(font)
        self.setDirectExcitation_btn.setObjectName(_fromUtf8("setDirectExcitation_btn"))
        self.horizontalLayout.addWidget(self.setDirectExcitation_btn)
        self.sendBasisSetsToMain_btn = QtGui.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sendBasisSetsToMain_btn.setFont(font)
        self.sendBasisSetsToMain_btn.setObjectName(_fromUtf8("sendBasisSetsToMain_btn"))
        self.horizontalLayout.addWidget(self.sendBasisSetsToMain_btn)
        self.retranslateUi(BasisGui)
        QtCore.QMetaObject.connectSlotsByName(BasisGui)

    def retranslateUi(self, BasisGui):
        BasisGui.setWindowTitle(_translate("BasisGui", "Choose Basis Sets", None))
        self.donor_lbl.setText(_translate("BasisGui", "Donor Basis Sets", None))
        self.acceptor_lbl.setText(_translate("BasisGui", "Acceptor Basis Sets", None))
        self.background_lbl.setText(_translate("BasisGui", "Background Basis Sets", None))
        self.donorExcitation_spin.setToolTip(_translate("BasisGui", "Excitation wavelength for donor emission", None))
        self.acceptorExcitation_spin.setToolTip(_translate("BasisGui", "Excitation wavelength for collecting only the acceptor spectra", None))
        self.slitWidth_spin.setToolTip(_translate("BasisGui", "Slit Width for the measurement", None))
        self.donor_list.setToolTip(_translate("BasisGui", "List of Donor basis sets. Select a donor to load the corresponding basis set for fitting", None))
        self.acceptor_list.setToolTip(_translate("BasisGui", "List of acceptor basis sets. Select an acceptor to load the corresponding basis set for fitting", None))
        self.background_list.setToolTip(_translate("BasisGui", "List of background basis sets. Select a background to load the corresponding basis set for fitting", None))
        self.donorEx_lbl.setText(_translate("BasisGui", "Donor Excitation", None))
        self.acceptorEx_lbl.setText(_translate("BasisGui", "Acceptor Excitation", None))
        self.slitWidth_lbl.setText(_translate("BasisGui", "Slit Width", None))
        self.correctionFactor_cbx.setText(_translate("BasisGui", "Manual Correction Factor", None))
        self.lamp_lbl.setText(_translate("BasisGui", "Choose Lamp Spectra", None))
        self.lamp_box.setToolTip(_translate("BasisGui", "Select the lamp used for collecting fluorescence spectra", None))
        self.addLamp.setText(_translate("BasisGui", "+", None))
        self.deleteLamp.setText(_translate("BasisGui", "-", None))
        self.donor_filter.setPlaceholderText(_translate("BasisGui", " Filter Donor Basis Sets", None))
        self.acceptor_filter.setPlaceholderText(_translate("BasisGui", " Filter Acceptor Basis Sets", None))
        self.background_filter.setPlaceholderText(_translate("BasisGui", " Filter Background Basis Sets", None))
        self.deleteAcceptor.setText(_translate("BasisGui", "-", None))
        self.deleteBackground.setText(_translate("BasisGui", "-", None))
        self.addAcceptor.setText(_translate("BasisGui", "+", None))
        self.deleteDonor.setText(_translate("BasisGui", "-", None))
        self.addDonor.setText(_translate("BasisGui", "+", None))
        self.addBackground.setText(_translate("BasisGui", "+", None))
        self.setDirectExcitation_btn.setToolTip(_translate("BasisGui", "Set the calculated direct emission correction factor into the fitting window", None))
        self.setDirectExcitation_btn.setText(_translate("BasisGui", "Set Emission Correction Factor (0.00)", None))
        self.sendBasisSetsToMain_btn.setText(_translate("BasisGui", "Send Basis Sets to Fytt", None))

        self.donor_filter.textChanged.connect(self.on_donorfilter_textChanged)
        self.acceptor_filter.textChanged.connect(self.on_acceptorfilter_textChanged)
        self.background_filter.textChanged.connect(self.on_backgroundfilter_textChanged)
        self.donorExcitation_spin.valueChanged.connect(self.donorExcitationChanged)
        self.acceptorExcitation_spin.valueChanged.connect(self.acceptorExcitationChanged)
        self.addDonor.clicked.connect(functools.partial(self.loadSpectraIntoDatabase, 's'))
        self.addAcceptor.clicked.connect(functools.partial(self.loadSpectraIntoDatabase, 's'))
        self.addBackground.clicked.connect(functools.partial(self.loadSpectraIntoDatabase, 'b'))
        self.addLamp.clicked.connect(functools.partial(self.loadSpectraIntoDatabase, 'l'))
        self.deleteDonor.clicked.connect(functools.partial(self.deleteSpectraFromDatabase, 'd'))
        self.deleteAcceptor.clicked.connect(functools.partial(self.deleteSpectraFromDatabase, 'a'))
        self.deleteBackground.clicked.connect(functools.partial(self.deleteSpectraFromDatabase, 'b'))
        self.deleteLamp.clicked.connect(functools.partial(self.deleteSpectraFromDatabase, 'l'))
        self.sendBasisSetsToMain_btn.clicked.connect(self.sendBasisSetsToMainWindow)
        self.setDirectExcitation_btn.clicked.connect(self.sendDirectExcitationtoMainWindow)
        self.slitWidth_spin.valueChanged.connect(self.slitValueChanged)
        self.correctionFactor_cbx.clicked.connect(self.manualCorrectionCheckState)
        self.correctionFactor_spin.valueChanged.connect(self.setManualCorrectionFactor)
        self.correctionFactor_cbx.setChecked(True)
        self.correctionFactor_spin.setEnabled(False)

    def slitValueChanged(self):
        self.calculateLampIntRatio()

    def manualCorrectionCheckState(self):
        if self.correctionFactor_cbx.isChecked():
            self.correctionFactor_spin.setEnabled(True)
            self.changeStateForManual(False)
            self.basis_sets.correctionFactor = self.correctionFactor_spin.value()
            self.outputCorrectionFactor()
        else:
            self.correctionFactor_spin.setEnabled(False)
            self.changeStateForManual(True)
            self.calculateLampIntRatio()

    def setManualCorrectionFactor(self):
        self.basis_sets.correctionFactor = self.correctionFactor_spin.value()
        self.outputCorrectionFactor()

    def changeStateForManual(self, state):
        self.lamp_box.setEnabled(state)
        self.lamp_lbl.setEnabled(state)
        self.donorExcitation_spin.setEnabled(state)
        self.acceptorExcitation_spin.setEnabled(state)
        self.slitWidth_spin.setEnabled(state)
        self.donorEx_lbl.setEnabled(state)
        self.acceptorEx_lbl.setEnabled(state)
        self.slitWidth_lbl.setEnabled(state)
        self.addLamp.setEnabled(state)
        self.deleteLamp.setEnabled(state)

    @QtCore.pyqtSlot(str)
    def on_donorfilter_textChanged(self, text):
        search = QtCore.QRegExp(    text,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )
        self.proxy_donor.setFilterRegExp(search)

    @QtCore.pyqtSlot(str)
    def on_acceptorfilter_textChanged(self, text):
        search = QtCore.QRegExp(    text,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )
        self.proxy_acceptor.setFilterRegExp(search)

    @QtCore.pyqtSlot(str)
    def on_backgroundfilter_textChanged(self, text):
        search = QtCore.QRegExp(    text,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )
        self.proxy_background.setFilterRegExp(search)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = BasisGui()
    mainWin.show()
    sys.exit(app.exec_())
