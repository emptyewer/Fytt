# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filelist.ui'
#
# Created: Tue Mar 17 10:24:10 2015
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

class Ui_FileList(object):
    def setupUi(self, FileList):
        FileList.setObjectName(_fromUtf8("FileList"))
        FileList.resize(240, 550)
        FileList.setMinimumSize(QtCore.QSize(240, 550))
        FileList.setMaximumSize(QtCore.QSize(240, 550))
        self.horizontalLayoutWidget = QtGui.QWidget(FileList)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 510, 221, 30))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayoutWidget = QtGui.QWidget(FileList)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 441))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidget = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setMinimumSize(QtCore.QSize(219, 439))
        self.listWidget.setMaximumSize(QtCore.QSize(219, 439))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica Neue"))
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.listWidget.setFont(font)
        self.listWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.listWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.listWidget.setLineWidth(2)
        self.listWidget.setFlow(QtGui.QListView.TopToBottom)
        self.listWidget.setSpacing(5)
        self.listWidget.setViewMode(QtGui.QListView.ListMode)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout.addWidget(self.listWidget)
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
        FileList.setWindowTitle(_translate("FileList", "Form", None))
        self.pushButton_2.setText(_translate("FileList", "Autofit All", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("FileList", "One", None))
        item = self.listWidget.item(1)
        item.setText(_translate("FileList", "Two", None))
        item = self.listWidget.item(2)
        item.setText(_translate("FileList", "Three", None))
        item = self.listWidget.item(3)
        item.setText(_translate("FileList", "Four", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("FileList", "Add...", None))
        self.pushButton_3.setText(_translate("FileList", "Clear", None))

