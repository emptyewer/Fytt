import os
import sys
from PyQt4 import QtCore, QtGui, uic


app = QtGui.QApplication(sys.argv)

def appExit():
    app.quit()
    sys.exit()

app.aboutToQuit.connect(appExit)
form_class, base_class = uic.loadUiType(os.path.join(os.path.curdir, 'ui', 'info.ui'))


class Info_Dialog(QtGui.QDialog, form_class):
    def __init__(self, *args):
        super(Info_Dialog, self).__init__(*args)
        self.setupUi(self)
        self.mainWindow = args

    def set_reference(self, text):
        self.ref_lbl.setText(text)

    def set_donor(self, text):
        self.donor_lbl.setText(text)

    def set_acceptor(self, text):
        self.acceptor_lbl.setText(text)

    def set_background(self, text):
        self.background_lbl.setText(text)

    def set_directexcitation(self, text):
        self.directexcitation_lbl.setText(text)

    @QtCore.pyqtSlot()
    def on_clear_btn_clicked(self):
        self.mainWindow.clearSpectraList()
        self.reset_labels()

    def reset_labels(self):
        text = '...'
        self.ref_lbl.setText(text)
        self.donor_lbl.setText(text)
        self.acceptor_lbl.setText(text)
        self.background_lbl.setText(text)
        self.directexcitation_lbl.setText(text)

    def windowTitle(self, str):
        self.setWindowTitle(str)