# -*- coding: utf-8 -*-

"""
Module implementing MainDialog.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Ui_main import Ui_Dialog
from DownloadEngine import DownloadEngine

import webbrowser


class MainDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.size_radio_group = QButtonGroup()
        self.size_radio_group.addButton(self.total_radioButton, 0)
        self.size_radio_group.addButton(self.XL_radioButton, 9)
        self.size_radio_group.addButton(self.L_radioButton, 3)
        self.size_radio_group.addButton(self.M_radioButton, 2)
        self.size_radio_group.addButton(self.S_radioButton, 1)
        self.count = 0
        
    
    def check_option(self):
        if self.word_lineEdit.text() == "":
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "请输入搜索关键词！")
            msg_box.exec_()
            return 0
        if self.dir_lineEdit.text() == "":
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "请选择图片存储目录！")
            msg_box.exec_()
            return 0
        return 1
            
    @pyqtSlot()
    def on_dir_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        dir = QFileDialog.getExistingDirectory(self, "选择图片存储目录",".")
        self.dir_lineEdit.setText(dir)
    
    @pyqtSlot()
    def on_download_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.progressBar.setValue(0)
        if self.check_option() == 1:
            self.progressBar.setMaximum(self.num_spinBox.value())
            self.download_pushButton.setEnabled(False)
            self.de = DownloadEngine(self.word_lineEdit.text(), self.size_radio_group.checkedId(), self.num_spinBox.value(), self.dir_lineEdit.text(), self.thread_spinBox.value())
            self.de.start()
            self.de.status_changed_signal.connect(self.status_changed_slot)
            self.de.download_done_signal.connect(self.download_done_slot)
            self.de.progressBar_updated_signal.connect(self.progressBar_updated_slot)
        
    
    @pyqtSlot()
    def on_src_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        webbrowser.open("https://github.com/01joy/BaiduImageDownloader")

    def progressBar_updated_slot(self):
        self.count += 1
        self.progressBar.setValue(self.count)
        
    def status_changed_slot(self, tip):
        self.status_label.setText(tip)
        self.count = 0
        if tip != '下载完成':
            self.progressBar.setValue(0)
        
    def download_done_slot(self, bad):
        msg_box = QMessageBox(QMessageBox.Information, "提示", "下载完毕\n成功%d,失败%d"%(self.num_spinBox.value() - bad, bad))
        msg_box.exec_()
        self.download_pushButton.setEnabled(True)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = MainDialog()
    Dialog.show()
    sys.exit(app.exec_())
