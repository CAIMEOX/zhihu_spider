from PyQt5 import uic, QtWidgets
import sys
import main
form_class = uic.loadUiType('GUI.ui')[0]


class ZhiHuGui(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("ZhiHu Spider")
        self.setWindowOpacity(0.5)
        self.show()
        # QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.Save_File_Button.clicked.connect(self.save_file)
        self.UrlInput.text()
        self.nameLabel = QtWidgets.QLabel(self)
        self.nameLabel.setText("URL")
        self.line = QtWidgets.QLineEdit(self)
        self.pushButton.clicked.connect(self.submit_uri)

        # self.exut_action.triggered.connect(self.exit)

    def submit_uri(self):
        print(self.UrlInput.text())
        question = main.Question(self.UrlInput.text(), None)
        print('Question:', question.get_question())

    def save_file(self, content):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "savefile",
                                                      "docx files (*.docx);;pdf files (*.pdf);;txt files (*.txt);;all files(*.*)")
        if '.txt' in file_path:
            pass
        elif '.docx' in file_path:
            pass

    def exit(self):
        sys.exit()


app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
myapp = ZhiHuGui(None)
myapp.show()
app.exec_()
