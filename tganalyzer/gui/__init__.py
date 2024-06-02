from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import datetime
import os
import sys
import random

random.seed(42)

SIDE_EFFECT = 0


class Chat:
    def __init__(self, chat_name, chat_type, messages_len):
        self.name = chat_name
        self.type = chat_type
        self.messages = [0] * messages_len


def get_all_chats():
    """TMP FUNC! Will be removed."""
    global SIDE_EFFECT
    res = [Chat(f"{SIDE_EFFECT}_{t}_{i:03d}", t, i) for t in ['private', 'public']
           for i in range(100, 1001, 100)]
    SIDE_EFFECT += 1
    # random.shuffle(res)
    # very_long_name = "very " * 20 + "long name"
    # res.append(very_long_name)
    # for i in range(20):
    #     res.append(f"new_chat{i:03d}")
    return res


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(300, 100, 400, 600)

        # Variables for application logic
        self.data_path = ""
        self.chats = []
        self.feature_names = [f"Feature {i:02d}" for i in range(11)]
        self.chat_checkboxes = []
        self.feature_checkboxes = []

        # Main layout
        layout = QVBoxLayout()

        # Horizontal layout with path to json file and button for choice it
        data_file_layout = QHBoxLayout()
        self.data_path_label = QLabel()
        select_data_button = QPushButton("select_data_button", self)
        select_data_button.clicked.connect(self.select_data_dir)
        data_file_layout.addWidget(self.data_path_label, 3)
        data_file_layout.addWidget(select_data_button, 1)

        # Scroll area for chats
        chat_choice_area = QScrollArea(self)
        chat_choice_wiget = QWidget()
        self.chats_layout = QVBoxLayout()
        chat_choice_wiget.setLayout(self.chats_layout)
        chat_choice_area.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        chat_choice_area.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        chat_choice_area.setWidgetResizable(True)
        chat_choice_area.setWidget(chat_choice_wiget)

        # Buttons that show all/only private/only public chats
        filter_button_layout = QHBoxLayout()
        all_chats_button = QPushButton("all_chats_button", self)
        only_private_button = QPushButton("only_private_button", self)
        only_public_button = QPushButton("only_public_button", self)
        filter_button_layout.addWidget(all_chats_button)
        filter_button_layout.addWidget(only_private_button)
        filter_button_layout.addWidget(only_public_button)
        # TODO Button connect

        # Buttons that choice all/don't choice any chats
        choice_button_layout = QHBoxLayout()
        choice_all_button = QPushButton("choice_all", self)
        choice_nothing_button = QPushButton("choice_nothing", self)
        choice_button_layout.addWidget(choice_all_button)
        choice_button_layout.addWidget(choice_nothing_button)
        # TODO Button connect

        # Button and spin that choice chats with more than N messages
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

        # Layout with date range
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

        # Scroll area for features
        features_area = QScrollArea(self)
        features_wiget = QWidget()
        self.features_layout = QVBoxLayout()
        features_wiget.setLayout(self.features_layout)
        for feature_name in self.feature_names:
            checkbox = QCheckBox(feature_name, self)
            checkbox.setCheckState(Qt.CheckState.Checked)
            self.feature_checkboxes.append(checkbox)
            self.features_layout.addWidget(checkbox)
        features_area.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        features_area.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        features_area.setWidgetResizable(True)
        features_area.setWidget(features_wiget)

        # Button that create a report
        create_report_button = QPushButton("create_report_button", self)
        create_report_button.clicked.connect(self.create_report)

        # Adding wigets and layouts to main layout
        layout.addLayout(data_file_layout)
        layout.addWidget(chat_choice_area, 1)
        layout.addLayout(filter_button_layout)
        layout.addLayout(choice_button_layout)
        layout.addLayout(complex_choice_layot)
        layout.addLayout(date_range_layout)
        layout.addWidget(features_area, 1)
        # layout.addStretch(1)
        layout.addWidget(create_report_button)

        # Create central wiget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("tg-analyzer")
        self.show()

    def delete_all_chats(self):
        if (count := self.chats_layout.count()):
            for i in range(count - 1, -1, -1):
                self.chats_layout.removeItem(self.chats_layout.itemAt(i))
        if self.chat_checkboxes:
            for i in range(len(self.chat_checkboxes) - 1, -1, -1):
                self.chat_checkboxes[i].deleteLater()
                del self.chat_checkboxes[i]
        if self.chats:
            for i in range(len(self.chats) - 1, -1, -1):
                del self.chats[i]

    def select_data_dir(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select data", "",
                                              "JSON Files (*.json)")
        if path:
            self.delete_all_chats()
            self.data_path = path
            self.data_path_label.setText(path)
            self.chats = get_all_chats()
            for chat in self.chats:
                checkbox = QCheckBox(chat.name, self)
                self.chat_checkboxes.append(checkbox)
                self.chats_layout.addWidget(checkbox)


    def create_report(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("tg-analyzer")
    window = MainWindow()
    sys.exit(app.exec_())
