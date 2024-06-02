from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import datetime
import os
import sys

SIDE_EFFECT = 1


def get_all_chats():
    """TMP FUNC! Will be removed."""
    global SIDE_EFFECT
    if SIDE_EFFECT == 1:
        res = []
        very_long_name = "very " * 20 + "long name"
        res.append(very_long_name)
        for i in range(20):
            res.append(f"chat{i:03d}")
        SIDE_EFFECT += 1
        return res
    else:
        res = []
        very_long_name = "very " * 20 + "long name"
        res.append(very_long_name)
        for i in range(20):
            res.append(f"new_chat{i:03d}")
        return res


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(300, 100, 400, 600)

        self.data_path = ""
        self.chat_names = []
        self.feature_names = [f"Feature {i:02d}" for i in range(11)]
        self.chat_checkboxes = []
        self.feature_checkboxes = []

        layout = QVBoxLayout()

        data_file_layout = QHBoxLayout()
        select_data_button = QPushButton("select_data_button", self)
        select_data_button.clicked.connect(self.select_data_dir)
        self.data_path_label = QLabel()
        data_file_layout.addWidget(self.data_path_label, 3)
        data_file_layout.addWidget(select_data_button, 1)

        chat_choice_area = QScrollArea(self)
        chat_choice_wiget = QWidget()
        self.chats_layout = QVBoxLayout()
        chat_choice_wiget.setLayout(self.chats_layout)
        chat_choice_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        chat_choice_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        chat_choice_area.setWidgetResizable(True)
        chat_choice_area.setWidget(chat_choice_wiget)

        filter_button_layout = QHBoxLayout()
        all_chats_button = QPushButton("all_chats_button", self)
        only_private_button = QPushButton("only_private_button", self)
        only_public_button = QPushButton("only_public_button", self)
        filter_button_layout.addWidget(all_chats_button)
        filter_button_layout.addWidget(only_private_button)
        filter_button_layout.addWidget(only_public_button)
        # TODO Button connect

        choice_button_layout = QHBoxLayout()
        choice_all_button = QPushButton("choice_all", self)
        choice_nothing_button = QPushButton("choice_nothing", self)
        choice_button_layout.addWidget(choice_all_button)
        choice_button_layout.addWidget(choice_nothing_button)
        # TODO Button connect

        complex_choice_layot = QHBoxLayout()
        complex_choice_button = QPushButton("complex_choice_button", self)
        complex_choice_label = QLabel()
        complex_choice_label.setText("complex_choice_label")
        complex_choice_spin = QSpinBox()
        complex_choice_spin.setRange(0, 1_000_000_000)
        complex_choice_spin.setSingleStep(100)
        complex_choice_spin.setValue(100)
        complex_choice_layot.addWidget(complex_choice_button)
        complex_choice_layot.addWidget(complex_choice_label)
        complex_choice_layot.addWidget(complex_choice_spin)
        # TODO Button connect

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

        features_area = QScrollArea(self)
        features_wiget = QWidget()
        self.features_layout = QVBoxLayout()
        features_wiget.setLayout(self.features_layout)
        for feature_name in self.feature_names:
            checkbox = QCheckBox(feature_name, self)
            self.feature_checkboxes.append(checkbox)
            self.features_layout.addWidget(checkbox)
        features_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        features_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        features_area.setWidgetResizable(True)
        features_area.setWidget(features_wiget)

        create_report_button = QPushButton("create_report_button", self)
        create_report_button.clicked.connect(self.create_report)

        layout.addLayout(data_file_layout)
        layout.addWidget(chat_choice_area, 1)
        layout.addLayout(filter_button_layout)
        layout.addLayout(choice_button_layout)
        layout.addLayout(complex_choice_layot)
        layout.addLayout(date_range_layout)
        layout.addWidget(features_area, 1)
        # layout.addStretch(1)
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
            self.chat_names = get_all_chats()
            for chat_name in self.chat_names:
                checkbox = QCheckBox(chat_name, self)
                self.chat_checkboxes.append(checkbox)
                self.chats_layout.addWidget(checkbox)
            # self.chat_choice_box.addItems(get_all_chats())
        return

    def create_report(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("tg-analyzer")
    window = MainWindow()
    sys.exit(app.exec_())
