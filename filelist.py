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

import re, os
from PyQt4 import QtCore, QtGui
from spectra import Spectra

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

class FileList_Window(QtGui.QDialog):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.spectraList = {}
        self.cy3_basis = {}
        self.cy5_basis = {}
        self.bkg_basis = {}
        self.cy3FileName = ''
        self.cy5FileName = ''
        self.bkgFileName = ''

    def loadFiles(self):
        filelist = []
        temp_spectra = Spectra()
        try:
            fD = QtGui.QFileDialog()
            fD.setFileMode(QtGui.QFileDialog.AnyFile)
            filename = fD.getOpenFileName(caption="Load list of spectra")
            if filename:
                fh = open(filename, 'r')
                for line in fh.readlines():
                    if re.match('^#', line):
                        if re.match('.+Acceptor', line):
                            self.cy5FileName = line.rstrip().split(':')[1].lstrip()
                            self.cy5_basis = temp_spectra.read_spectra(self.cy5FileName)
                        elif re.match('.+Donor', line):
                            self.cy3FileName = line.rstrip().split(':')[1].lstrip()
                            self.cy3_basis = temp_spectra.read_spectra(self.cy3FileName)
                        elif re.match('.+Background', line):
                            self.bkgFileName = line.rstrip().split(':')[1].lstrip()
                            self.bkg_basis = temp_spectra.read_spectra(self.bkgFileName)
                    else:
                        filelist.append(line.rstrip().lstrip())
                fh.close()
        except IOError:
            pass

        for name in filelist:
            item = QtGui.QListWidgetItem()
            item.setText(_translate("FileList", os.path.basename(name), None))
            self.fileList_wgt.addItem(item)
            spectra = Spectra()
            spectra.referenceFileName = name
            spectra.cy3FileName = self.cy3FileName
            spectra.cy5FileName = self.cy5FileName
            spectra.bkgFileName = self.bkgFileName
            spectra.cy3_basis = self.cy3_basis
            spectra.cy5_basis = self.cy5_basis
            spectra.bkg_basis = self.bkg_basis
            spectra.reference = spectra.read_spectra(name)
            (spectra.cy3_basis_scaled, spectra.cy3_scaleFactor) = spectra.rescale_basis(spectra.reference, spectra.cy3_basis, max(spectra.cy3_basis, key=spectra.cy3_basis.get))
            (spectra.cy5_basis_scaled, spectra.cy5_scaleFactor) = spectra.rescale_basis(spectra.reference, spectra.cy5_basis, max(spectra.cy5_basis, key=spectra.cy5_basis.get))
            (spectra.bkg_basis_scaled, spectra.bkg_scaleFactor) = spectra.rescale_basis(spectra.reference, spectra.bkg_basis, min(list(spectra.bkg_basis.keys())))
            spectra.calculate_spectral_sum()
            spectra.calculate_residuals()
            spectra.calculateRegionBounds()
            spectra.calculateRegionIndex(spectra.lowSelection, spectra.highSelection)
            self.spectraList[os.path.basename(name)] = spectra

    def setupUi(self, FileList):
        FileList.setObjectName(_fromUtf8("FileList"))
        FileList.resize(240, 550)
        FileList.setMinimumSize(QtCore.QSize(240, 550))
        FileList.setMaximumSize(QtCore.QSize(240, 550))
        self.horizontalLayoutWidget = QtGui.QWidget(FileList)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 500, 221, 30))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fitall_btn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.fitall_btn.setObjectName(_fromUtf8("fitall_btn"))
        self.horizontalLayout.addWidget(self.fitall_btn)
        self.verticalLayoutWidget = QtGui.QWidget(FileList)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 441))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fileList_wgt = QtGui.QListWidget(self.verticalLayoutWidget)
        self.fileList_wgt.setMinimumSize(QtCore.QSize(219, 439))
        self.fileList_wgt.setMaximumSize(QtCore.QSize(219, 439))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica Neue"))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.fileList_wgt.setFont(font)
        self.fileList_wgt.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fileList_wgt.setFrameShadow(QtGui.QFrame.Sunken)
        self.fileList_wgt.setLineWidth(2)
        self.fileList_wgt.setFlow(QtGui.QListView.TopToBottom)
        self.fileList_wgt.setSpacing(5)
        self.fileList_wgt.setViewMode(QtGui.QListView.ListMode)
        self.fileList_wgt.setObjectName(_fromUtf8("fileList_wgt"))
        self.verticalLayout.addWidget(self.fileList_wgt)

        self.verticalLayout.addWidget(self.fileList_wgt)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(FileList)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 460, 221, 30))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.retranslateUi(FileList)
        QtCore.QMetaObject.connectSlotsByName(FileList)

    def retranslateUi(self, FileList):
        FileList.setWindowTitle(_translate("FileList", "Reference Spectra List", None))
        self.fitall_btn.setText(_translate("FileList", "Fytt All", None))
        __sortingEnabled = self.fileList_wgt.isSortingEnabled()
        self.fileList_wgt.setSortingEnabled(False)
        self.pushButton.setText(_translate("FileList", "Add...", None))
        self.pushButton_3.setText(_translate("FileList", "Clear", None))
        self.fileList_wgt.setSortingEnabled(__sortingEnabled)

    def clearSpectra(self):
        self.spectraList = {}
        self.cy3_basis = {}
        self.cy5_basis = {}
        self.bkg_basis = {}
        self.cy3FileName = ''
        self.cy5FileName = ''
        self.bkgFileName = ''

    def getAllSpectra(self):
        # items = []
        # for index in xrange(self.fileList_wgt.count()):
        #      items.append(self.fileList_wgt.item(index))
        # labels = [str(i.text()) for i in items]
        return self.spectraList

    def getSpectra(self, name):
        return self.spectraList[name]
