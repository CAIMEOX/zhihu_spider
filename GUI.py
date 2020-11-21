from PyQt4 import QtCore, QtGui, uic
import sys, docx #, threading 多线程

form_class = uic.loadUiType('GUI.ui')[0]

class ZhiHuGui(QtGui.QMainWindow, form_class):
    def __init__(self,parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.Save_File_Button.clicked.connect(self.save_file)
        self.exut_action.triggered.connect(self.exit)

    def save_file(self, content):
        file_path =  QtGui.QFileDialog.getSaveFileName(self,"save file","savefile" ,"docx files (*.docx);;pdf files (*.pdf);;txt files (*.txt);;all files(*.*)")
        if '.txt' in file_path:
            pass
        elif '.docx' in file_path:
            pass

    def exit(self):
        sys.exit()

app = QtGui.QApplication(sys.argv)
myapp = ZhiHuGui(None)
myapp.show()
app.exec_()




