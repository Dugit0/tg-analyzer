from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import datetime
import os
import sys


def get_all_chats():
    """TMP FUNC! Will be removed."""
    return ["chat00", "chat01", "chat02", "chat03", "chat04", "chat05"]


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

        self.chat_choice_box = QComboBox(self)
        
        date_range_layout = QHBoxLayout()
        today_date = datetime.date.today()
        assert today_date.year - 5 > 0
        from_date = QDateEdit(QDate(today_date.year - 5,
                                    today_date.month,
                                    today_date.day))
        to_date = QDateEdit(QDate(today_date.year,
                                  today_date.month,
                                  today_date.day))
        from_date.setCalendarPopup(True)
        to_date.setCalendarPopup(True)
        date_range_layout.addWidget(from_date)
        date_range_layout.addWidget(to_date)
        create_report_button = QPushButton("create_report_button", self)
        create_report_button.clicked.connect(self.create_report)


        layout.addLayout(data_file_layout)
        layout.addWidget(self.chat_choice_box)
        layout.addLayout(date_range_layout)
        layout.addStretch(1)
        layout.addWidget(create_report_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("tg-analyzer")
        self.show()

    def select_data_dir(self):
        path, _ = QFileDialog.getOpenFileName(self,
                                              "Select data",
                                              "",
                                              "JSON Files (*.json)")
        if path:
            self.data_path = path
            self.data_path_label.setText(path)
            self.chat_choice_box.addItems(get_all_chats())
        return

    def create_report(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("tg-analyzer")
    window = MainWindow()
    sys.exit(app.exec_())

