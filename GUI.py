from PyQt5 import uic, QtWidgets
import main
import sys, threading

form_class = uic.loadUiType('GUI.ui')[0]


class ZhiHuGui(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        super().__init__()
        # self.setWindowTitle("ZhiHu Spider")  在ui文件中已添加
        # self.setWindowOpacity(0.5)
        self.show()
        # QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.check_event()
        self.Save_File_Button.clicked.connect(self.save_file)
        self.UrlInput.text()
        # self.nameLabel = QtWidgets.QLabel(self)
        # self.nameLabel.setText("URL")
        # self.line = QtWidgets.QLineEdit(self)
        self.pushButton.clicked.connect(self.submit_uri)

        # self.exut_action.triggered.connect(self.exit)

    def check_event(self):
        '部分状态运行监测'
        # 写初始化状态时用的代码
        self.pushButton.setEnabled(False)
        self.Save_File_Button.setEnabled(False)
        def check_events():
            while True:
                # 写运行时要监测的状态代码
                if self.UrlInput.text() !=  '':
                    self.pushButton.setEnabled(True)
        check_thread = threading.Thread(target = check_events)
        check_thread.start()

    def submit_uri(self):
        print(self.UrlInput.text())
        try:
            question = main.Question(self.UrlInput.text(), None)
            print('Question:', question.get_question())
        except:
            QtWidgets.QMessageBox.warning(self, '错误的网址！！！', '请检查网址的正确性！', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

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
