# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insertdb.ui'
#
# Created: Wed Apr 15 14:08:14 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 322)
        Dialog.setMinimumSize(QtCore.QSize(640, 322))
        Dialog.setMaximumSize(QtCore.QSize(640, 322))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 280, 611, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 190, 581, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.exFile_lbl = QtGui.QLabel(self.horizontalLayoutWidget)
        self.exFile_lbl.setObjectName(_fromUtf8("exFile_lbl"))
        self.horizontalLayout.addWidget(self.exFile_lbl)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.exFilePath = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.exFilePath.setMinimumSize(QtCore.QSize(330, 0))
        self.exFilePath.setObjectName(_fromUtf8("exFilePath"))
        self.horizontalLayout.addWidget(self.exFilePath)
        self.exLoadButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.exLoadButton.setObjectName(_fromUtf8("exLoadButton"))
        self.horizontalLayout.addWidget(self.exLoadButton)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 601, 181))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayoutWidget = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 70, 561, 101))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.long_name = QtGui.QLineEdit(self.gridLayoutWidget)
        self.long_name.setObjectName(_fromUtf8("long_name"))
        self.gridLayout.addWidget(self.long_name, 1, 1, 1, 1)
        self.short_name = QtGui.QLineEdit(self.gridLayoutWidget)
        self.short_name.setObjectName(_fromUtf8("short_name"))
        self.gridLayout.addWidget(self.short_name, 0, 1, 1, 1)
        self.short_lbl = QtGui.QLabel(self.gridLayoutWidget)
        self.short_lbl.setObjectName(_fromUtf8("short_lbl"))
        self.gridLayout.addWidget(self.short_lbl, 0, 0, 1, 1)
        self.long_lbl = QtGui.QLabel(self.gridLayoutWidget)
        self.long_lbl.setObjectName(_fromUtf8("long_lbl"))
        self.gridLayout.addWidget(self.long_lbl, 1, 0, 1, 1)
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
        self.lamp_radio = QtGui.QRadioButton(self.horizontalLayoutWidget_2)
        self.lamp_radio.setObjectName(_fromUtf8("lamp_radio"))
        self.horizontalLayout_2.addWidget(self.lamp_radio)
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

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.exem_radio, self.background_radio)
        Dialog.setTabOrder(self.background_radio, self.lamp_radio)
        Dialog.setTabOrder(self.lamp_radio, self.short_name)
        Dialog.setTabOrder(self.short_name, self.long_name)
        Dialog.setTabOrder(self.long_name, self.environment)
        Dialog.setTabOrder(self.environment, self.exFilePath)
        Dialog.setTabOrder(self.exFilePath, self.exLoadButton)
        Dialog.setTabOrder(self.exLoadButton, self.emFilePath)
        Dialog.setTabOrder(self.emFilePath, self.emLoadButton)
        Dialog.setTabOrder(self.emLoadButton, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Insert Spectra to Database", None))
        self.exFile_lbl.setText(_translate("Dialog", "Excitation Spectrum", None))
        self.exLoadButton.setText(_translate("Dialog", "Choose...", None))
        self.groupBox.setTitle(_translate("Dialog", "Basis Set Type", None))
        self.short_lbl.setText(_translate("Dialog", "Short Name", None))
        self.long_lbl.setText(_translate("Dialog", "Long Name", None))
        self.environment_lbl.setText(_translate("Dialog", "Environment", None))
        self.exem_radio.setText(_translate("Dialog", "Donor/Acceptor", None))
        self.background_radio.setText(_translate("Dialog", "Background", None))
        self.lamp_radio.setText(_translate("Dialog", "Lamp", None))
        self.emFile_lbl.setText(_translate("Dialog", "Emission Spectrum", None))
        self.emLoadButton.setText(_translate("Dialog", "Choose...", None))

