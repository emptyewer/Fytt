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
from spectra import Spectra
import sqlite3 as lite
import cPickle as pickle
import functools
import numpy as np
import sys, os

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

class DB_Dialog(QtGui.QDialog):
    def __init__(self, className):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.basisClass = className
        self.name = ''
        self.acronym = ''
        self.envornment = ''
        self.type = ''
        self.ExXvalues = []
        self.ExYvalues = []
        self.EmXvalues = []
        self.EmYvalues = []
        self.spectra = Spectra()
        self.enableDisableBasisType(self.basisClass)

    def chooseFileClicked(self, ex):
        fD = QtGui.QFileDialog()
        fD.setFileMode(QtGui.QFileDialog.AnyFile)
        filename = fD.getOpenFileName(caption="Choose File...")
        contents = self.spectra.read_spectra(filename, flag=True)
        if ex == True:
            # self.exFilePath.setText(filename)
            self.ExXvalues = contents['x']
            self.ExYvalues = list(np.divide(np.array(contents['y']), np.sum(np.array(contents['y']))))
        else:
            self.emFilePath.setText(filename)
            self.EmXvalues = contents['x']
            self.EmYvalues = list(np.divide(np.array(contents['y']), np.sum(np.array(contents['y']))))

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 322)
        Dialog.setMinimumSize(QtCore.QSize(640, 322))
        Dialog.setMaximumSize(QtCore.QSize(640, 322))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 190, 581, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        # self.exFile_lbl = QtGui.QLabel(self.horizontalLayoutWidget)
        # self.exFile_lbl.setObjectName(_fromUtf8("exFile_lbl"))
        # self.horizontalLayout.addWidget(self.exFile_lbl)
        # spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem)
        # self.exFilePath = QtGui.QLineEdit(self.horizontalLayoutWidget)
        # self.exFilePath.setMinimumSize(QtCore.QSize(330, 0))
        # self.exFilePath.setObjectName(_fromUtf8("exFilePath"))
        # self.horizontalLayout.addWidget(self.exFilePath)
        # self.exLoadButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        # self.exLoadButton.setObjectName(_fromUtf8("exLoadButton"))
        # self.horizontalLayout.addWidget(self.exLoadButton)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 601, 181))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayoutWidget = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 70, 561, 101))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.short_name = QtGui.QLineEdit(self.gridLayoutWidget)
        self.short_name.setObjectName(_fromUtf8("short_name"))
        self.gridLayout.addWidget(self.short_name, 0, 1, 1, 1)
        self.short_lbl = QtGui.QLabel(self.gridLayoutWidget)
        self.short_lbl.setObjectName(_fromUtf8("short_lbl"))
        self.gridLayout.addWidget(self.short_lbl, 0, 0, 1, 1)
        self.long_lbl = QtGui.QLabel(self.gridLayoutWidget)
        self.long_lbl.setObjectName(_fromUtf8("long_lbl"))
        self.gridLayout.addWidget(self.long_lbl, 1, 0, 1, 1)
        self.long_name = QtGui.QLineEdit(self.gridLayoutWidget)
        self.long_name.setObjectName(_fromUtf8("long_name"))
        self.gridLayout.addWidget(self.long_name, 1, 1, 1, 1)
        self.environment_lbl = QtGui.QLabel(self.gridLayoutWidget)
        self.environment_lbl.setObjectName(_fromUtf8("environment_lbl"))
        self.gridLayout.addWidget(self.environment_lbl, 2, 0, 1, 1)
        self.environment = QtGui.QLineEdit(self.gridLayoutWidget)
        self.environment.setObjectName(_fromUtf8("environment"))
        self.gridLayout.addWidget(self.environment, 2, 1, 1, 1)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 29, 561, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.exem_radio = QtGui.QRadioButton(self.horizontalLayoutWidget_2)
        self.exem_radio.setObjectName(_fromUtf8("exem_radio"))
        self.horizontalLayout_2.addWidget(self.exem_radio)
        self.background_radio = QtGui.QRadioButton(self.horizontalLayoutWidget_2)
        self.background_radio.setObjectName(_fromUtf8("background_radio"))
        self.horizontalLayout_2.addWidget(self.background_radio)
        # self.lamp_radio = QtGui.QRadioButton(self.horizontalLayoutWidget_2)
        # self.lamp_radio.setObjectName(_fromUtf8("lamp_radio"))
        # self.horizontalLayout_2.addWidget(self.lamp_radio)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 230, 581, 41))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.emFile_lbl = QtGui.QLabel(self.horizontalLayoutWidget_4)
        self.emFile_lbl.setObjectName(_fromUtf8("emFile_lbl"))
        self.horizontalLayout_4.addWidget(self.emFile_lbl)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.emFilePath = QtGui.QLineEdit(self.horizontalLayoutWidget_4)
        self.emFilePath.setMinimumSize(QtCore.QSize(330, 0))
        self.emFilePath.setObjectName(_fromUtf8("emFilePath"))
        self.horizontalLayout_4.addWidget(self.emFilePath)
        self.emLoadButton = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.emLoadButton.setObjectName(_fromUtf8("emLoadButton"))
        self.horizontalLayout_4.addWidget(self.emLoadButton)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 280, 611, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.exem_radio, self.background_radio)
        # Dialog.setTabOrder(self.background_radio, self.lamp_radio)
        # Dialog.setTabOrder(self.lamp_radio, self.short_name)
        Dialog.setTabOrder(self.short_name, self.long_name)
        Dialog.setTabOrder(self.long_name, self.environment)
        # Dialog.setTabOrder(self.environment, self.exFilePath)
        # Dialog.setTabOrder(self.exFilePath, self.exLoadButton)
        # Dialog.setTabOrder(self.exLoadButton, self.emFilePath)
        Dialog.setTabOrder(self.emFilePath, self.emLoadButton)
        Dialog.setTabOrder(self.emLoadButton, self.buttonBox)
        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Insert Spectra to Database", None))
        # self.exFile_lbl.setText(_translate("Dialog", "Excitation Spectrum", None))
        # self.exLoadButton.setText(_translate("Dialog", "Choose...", None))
        self.groupBox.setTitle(_translate("Dialog", "Basis Set Type", None))
        self.short_lbl.setText(_translate("Dialog", "Short Name", None))
        self.long_lbl.setText(_translate("Dialog", "Long Name", None))
        self.environment_lbl.setText(_translate("Dialog", "Environment", None))
        self.exem_radio.setText(_translate("Dialog", "Donor/Acceptor", None))
        self.background_radio.setText(_translate("Dialog", "Background", None))
        # self.lamp_radio.setText(_translate("Dialog", "Lamp", None))
        self.emFile_lbl.setText(_translate("Dialog", "Emission Spectrum", None))
        self.emLoadButton.setText(_translate("Dialog", "Choose...", None))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(14)
        self.emLoadButton.setFont(font)

        # self.exLoadButton.clicked.connect(functools.partial(self.chooseFileClicked, True))
        self.emLoadButton.clicked.connect(functools.partial(self.chooseFileClicked, False))
        self.exem_radio.clicked.connect(self.spectraClassClicked)
        self.background_radio.clicked.connect(self.spectraClassClicked)
        # self.lamp_radio.clicked.connect(self.spectraClassClicked)

    def spectraClassClicked(self):
        if self.exem_radio.isChecked():
            self.basisClass = 's'
        elif self.background_radio.isChecked():
            self.basisClass = 'b'
        # elif self.lamp_radio.isChecked():
        #     self.basisClass = 'l'
        self.enableDisableBasisType(self.basisClass)

    def enableDisableBasisType(self, choice):
        if choice == 'b':
            if not self.background_radio.isChecked():
                self.background_radio.setChecked(True)
            self.long_name.setEnabled(True)
            self.long_lbl.setEnabled(True)
            self.environment.setEnabled(True)
            self.environment_lbl.setEnabled(True)
            # self.exFile_lbl.setText('Background Spectrum')
        # elif choice == 'l':
        #     # if not self.lamp_radio.isChecked():
        #     #     self.lamp_radio.setChecked(True)
        #     self.long_name.setEnabled(False)
        #     self.long_lbl.setEnabled(False)
        #     self.environment.setEnabled(False)
        #     self.environment_lbl.setEnabled(False)
        #     # self.exFile_lbl.setText('Lamp Spectrum')
        elif choice == 's':
            if not self.exem_radio.isChecked():
                self.exem_radio.setChecked(True)
            self.long_name.setEnabled(True)
            self.long_lbl.setEnabled(True)
            self.environment.setEnabled(True)
            self.environment_lbl.setEnabled(True)
            # self.exFile_lbl.setText('Excitation Spectrum')

    def checkFields(self):
        returnValue = True
        if self.basisClass == 'b':
            if str(self.short_name.text()) == '' or str(self.long_name.text()) == '' or str(self.environment.text()) == '':
                returnValue = False
                QtGui.QMessageBox.about(self, "Warning!", "Please verify that all the input fields are vaild.")
        elif self.basisClass == 's':
            if str(self.short_name.text()) == '' or str(self.long_name.text()) == '' or str(self.environment.text()) == '' or str(self.emFilePath.text()) == '':
                returnValue = False
                QtGui.QMessageBox.about(self, "Warning!", "Please verify that all the input fields are vaild.")
        elif self.basisClass == 'l':
            if str(self.short_name.text()) == '':
                returnValue = False
                QtGui.QMessageBox.about(self, "Warning!", "Please verify that all the input fields are vaild.")
        return returnValue

    def accept(self):
        db_path = ''
        if sys.platform == 'darwin':
            db_path = "db/fytt_db.sqlite3"
        elif sys.platform == 'linux2' or sys.platform == 'linux':
            db_path = "fytt_db.sqlite3"
        elif sys.platform == 'win32':
            db_path = "fytt_db.sqlite3"
        # db_path = "fytt2_db.sqlite3"
        db_handle = lite.connect(db_path, isolation_level=None)
        db_cursor = db_handle.cursor()
        if self.checkFields() == True:
            if self.basisClass == 'b':
                db_cursor.execute("SELECT id from spectra ORDER BY id DESC LIMIT 1")
                current_id = 0
                fetch = db_cursor.fetchall()
                if len(fetch) > 0:
                    largest_id = fetch[0][0]
                    current_id = largest_id + 1
                db_cursor.execute("INSERT INTO backgrounds(id, name, acronym, environment) VALUES (?,?,?,?)", (current_id, str(self.long_name.text()).rstrip().lstrip(), str(self.short_name.text()).rstrip().lstrip(), str(self.environment.text()).rstrip().lstrip(),))
                db_handle.commit()
                db_cursor.execute("INSERT INTO spectra(id, name, type, x, y) VALUES (?,?,?,?,?)", (current_id, str(self.long_name.text()).rstrip().lstrip(), 'b', lite.Binary(pickle.dumps(self.ExXvalues, protocol=pickle.HIGHEST_PROTOCOL)), lite.Binary(pickle.dumps(self.ExYvalues, protocol=pickle.HIGHEST_PROTOCOL)),))
                db_handle.commit()
            elif self.basisClass == 'l':
                db_cursor.execute("SELECT id from lamps ORDER BY id DESC LIMIT 1")
                current_id = 0
                fetch = db_cursor.fetchall()
                if len(fetch) > 0:
                    largest_id = fetch[0][0]
                    current_id = largest_id + 1
                db_cursor.execute("INSERT INTO lamps(id, name, x, y) VALUES (?,?,?,?)", (current_id, str(self.short_name.text()).rstrip().lstrip(), lite.Binary(pickle.dumps(self.ExXvalues, protocol=pickle.HIGHEST_PROTOCOL)), lite.Binary(pickle.dumps(self.ExYvalues, protocol=pickle.HIGHEST_PROTOCOL)),))
                db_handle.commit()
            else:
                db_cursor.execute("SELECT id from spectra ORDER BY id DESC LIMIT 1")
                current_id = 0
                fetch = db_cursor.fetchall()
                if len(fetch) > 0:
                    largest_id = fetch[0][0]
                    current_id = largest_id + 1
                db_cursor.execute("INSERT INTO attributes(id, name, acronym, type, environment) VALUES (?,?,?,?,?)", (current_id, str(self.long_name.text()).rstrip().lstrip(), str(self.short_name.text()).rstrip().lstrip(), 'x', str(self.environment.text()).rstrip().lstrip(),))
                db_handle.commit()

                db_cursor.execute("INSERT INTO attributes(id, name, acronym, type, environment) VALUES (?,?,?,?,?)", (current_id + 1, str(self.long_name.text()).rstrip().lstrip(), str(self.short_name.text()).rstrip().lstrip(), 'm', str(self.environment.text()).rstrip().lstrip(),))
                db_handle.commit()

                db_cursor.execute("INSERT INTO spectra(id, name, type, x, y) VALUES (?,?,?,?,?)", (current_id, str(self.long_name.text()).rstrip().lstrip(), 'x', lite.Binary(pickle.dumps(self.ExXvalues, protocol=pickle.HIGHEST_PROTOCOL)), lite.Binary(pickle.dumps(self.ExYvalues, protocol=pickle.HIGHEST_PROTOCOL)),))
                db_handle.commit()

                db_cursor.execute("INSERT INTO spectra(id, name, type, x, y) VALUES (?,?,?,?,?)", (current_id + 1, str(self.long_name.text()).rstrip().lstrip(), 'm', lite.Binary(pickle.dumps(self.EmXvalues, protocol=pickle.HIGHEST_PROTOCOL)), lite.Binary(pickle.dumps(self.EmYvalues, protocol=pickle.HIGHEST_PROTOCOL)),))
                db_handle.commit()
            self.close()
