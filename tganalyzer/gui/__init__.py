from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(300, 100, 400, 600)
        
        self.data_path = ""
        
        layout = QVBoxLayout()

        data_file_layout = QHBoxLayout()
        select_data_button = QPushButton("select_data_button", self)
        select_data_button.clicked.connect(self.select_data_dir)
        self.data_path_label = QLabel()
        data_file_layout.addWidget(self.data_path_label)
        data_file_layout.addWidget(select_data_button)

        layout.addLayout(data_file_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("tg-analyzer")
        self.show()

    def select_data_dir(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select data", "", "JSON Files (*.json)")
        if path:
            self.data_path = path
            self.data_path_label.setText(path)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("tg-analyzer")
    window = MainWindow()
    sys.exit(app.exec_())

