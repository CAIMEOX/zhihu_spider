from PyQt5 import uic, QtWidgets
import spider
import sys, threading

form_class = uic.loadUiType('GUI.ui')[0]


class ZhiHuGui(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        super().__init__()
        # self.setWindowTitle("ZhiHu Spider")  在ui文件中已添加
        # self.setWindowOpacity(0.5)
        # QtWidgets.QMainWindow.__init__(self, parent)

        #######################初始化##########################
        self.show()
        self.setupUi(self)
        self.check_event()
        #######################初始化##########################

        # self.nameLabel = QtWidgets.QLabel(self)
        # self.nameLabel.setText("URL")
        # self.line = QtWidgets.QLineEdit(self)

        ########################问题###########################
        self.A_Button.clicked.connect(self.A_submit_url)
        self.A_Save_File_Button.clicked.connect(self.A_save_file)
        self.A_UrlInput.text()
        self.A_list.clicked.connect(self.A_click)
        ########################问题###########################

        ########################专栏###########################
        self.C_Button.clicked.connect(self.C_submit_url)
        self.C_Save_File_Button.clicked.connect(self.C_save_file)
        self.C_UrlInput.text()
        self.C_list.clicked.connect(self.C_click)
        ########################专栏###########################

        self.exit_action.triggered.connect(self.exit)

    def check_event(self):
        '部分状态运行监测'
        # 写初始化状态时用的代码
        self.A_Button.setEnabled(False)
        self.A_Save_File_Button.setEnabled(False)
        self.C_Button.setEnabled(False)
        self.C_Save_File_Button.setEnabled(False)
        def check_events():
            while True:
                # 写运行时要监测的状态代码
                if self.A_UrlInput.text() !=  '':
                    self.A_Button.setEnabled(True)
                if self.C_UrlInput.text() !=  '':
                    self.C_Button.setEnabled(True)
        check_thread = threading.Thread(target = check_events)
        check_thread.setDaemon(True)  #主程序退出进程关闭
        check_thread.start()

    ##################################################################问题######################################################################
    def A_click(self,qModelIndex):
        #print(qModelIndex.row())
        #self.ids(qModelIndex.row())
        self.A_choice = self.ids[int(qModelIndex.row())]
        self.A_Save_File_Button.setEnabled(True)
        QtWidgets.QMessageBox.information(self, '内容显示',
                                          '<h2 style="color:#ff0000">作者太懒了，没有做</h2>\n<h5>coming soon</h5>',
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def A_submit_url(self):
        print(self.A_UrlInput.text())
        try:
            self.question = spider.Question(self.A_UrlInput.text())
            self.A_title.setText(self.question.get_title())
            print('Question:', self.question.get_title())
            print('Please choose the answer you want to download:')
            ids = self.question.get_answer_ids()
            self.ids = list(ids)
            self.A_number.setText(str(len(ids)))
            for i in ids:
                self.A_list.addItem(str(i))
                print(i)
        except Exception as e:
            s = sys.exc_info()
            print('\n',"Error '%s' happend on line %d" %(s[1],s[2].tb_lineno),'\n')
            QtWidgets.QMessageBox.warning(self, '错误的网址！！！', '请检查网址的正确性！', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def A_save_file(self, content):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "savefile",
                                                          "pdf files (*.pdf);;all files(*.*)")

        print(file_path)
        id = self.A_choice
        try:
            self.question.save_to_pdf(id, file_path[0])
        except Exception as e:
            s = sys.exc_info()
            QtWidgets.QMessageBox.warning(self, '错误！！！', '<h2>保存失败</h2>\n<h5 style="color:#ff0000">(错误代码:%d,%s)</h5>'%(s[2].tb_lineno,s[1]),
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
    ##################################################################问题######################################################################

    ##################################################################专题######################################################################
    def C_click(self,qModelIndex):
        #print(qModelIndex.row())
        #self.ids(qModelIndex.row())
        self.C_choice = self.titles[int(qModelIndex.row())]
        self.C_Save_File_Button.setEnabled(True)
        QtWidgets.QMessageBox.information(self, '内容显示',
                                          '<h2 style="color:#ff0000">作者太懒了，没有做</h2>\n<h5>coming soon</h5>',
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def C_submit_url(self):
        print(self.C_UrlInput.text())
        try:
            self.column = spider.Column(self.C_UrlInput.text())
            self.C_title.setText(self.column.get_title())
            print('Please choose the answer you want to download:')
            titles = self.column.get_titles()
            self.titles = list(titles)
            self.C_number.setText(str(len(titles)))
            for i in titles:
                self.C_list.addItem(str(i))
                print(i)
        except Exception as e:
            s = sys.exc_info()
            print('\n',"Error '%s' happend on line %d" %(s[1],s[2].tb_lineno),'\n')
            QtWidgets.QMessageBox.warning(self, '错误的网址！！！', '请检查网址的正确性！', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def C_save_file(self, content):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "savefile",
                                                          "pdf files (*.pdf);;all files(*.*)")

        print(file_path)
        title = self.C_choice
        try:
            self.column.save_to_pdf(title, file_path[0])
        except Exception as e:
            s = sys.exc_info()
            QtWidgets.QMessageBox.warning(self, '错误！！！', '<h2>保存失败</h2>\n<h5 style="color:#ff0000">(错误代码:%d,%s)</h5>'%(s[2].tb_lineno,s[1]),
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
    ##################################################################专题######################################################################

    def exit(self):
        self.exit()
        sys.exit()


app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
myapp = ZhiHuGui(None)
myapp.show()
app.exec_()
