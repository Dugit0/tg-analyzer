"""Графический интерфейс tg-analyzer."""
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QDateEdit, QCheckBox
from PyQt5.QtWidgets import QScrollArea, QSpinBox
from PyQt5.QtCore import Qt, QDate
from pathlib import Path
import datetime
import gettext
import pytz

import tganalyzer
from tganalyzer.core.creator import start_creator
from tganalyzer.core.analyzer import start_analyses
from tganalyzer.html_export import html_export


PO_PATH = Path(__file__).resolve().parent / 'po'
LOCALES = {
    "ru_RU.UTF-8": gettext.translation("gui", PO_PATH, ["ru"]),
    "en_US.UTF-8": gettext.NullTranslations(),
}


class MainWindow(QMainWindow):
    """Основное окно приложения."""

    def __init__(self, *args, lang='en_US.UTF-8', **kwargs):
        """Основное окно приложения.

        :param lang: название языка, для которого поддерживается перевод.
        :type lang: str
        """
        super(MainWindow, self).__init__()
        self.setGeometry(300, 100, 500, 700)

        # Variables for application logic
        self.locale = LOCALES[lang]
        self.data_path = ""
        self.chats = []
        self.features = {
                "symb": self.locale.gettext("Symbol counting"),
                "word": self.locale.gettext("Word counting"),
                "msg": self.locale.gettext("Message counting"),
                "voice_message": self.locale.gettext("Voice message analysis"),
                "video_message": self.locale.gettext("Circle analysis"),
                "video_file": self.locale.gettext("Video file analysis"),
                "photo": self.locale.gettext("Photo counting"),
                "day_night": self.locale.gettext("Activity at different times"
                                                 "of the day"),
                }
        self.chat_checkboxes = []
        self.feature_checkboxes = []

        # Main layout
        layout = QVBoxLayout()

        # Horizontal layout with path to json file and button for choice it
        data_file_layout = QHBoxLayout()
        self.data_path_label = QLabel()
        select_data_button = QPushButton(self.locale.gettext("Select file"),
                                         self)
        select_data_button.clicked.connect(self.select_data_file)
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
        all_chats_button = QPushButton(
                self.locale.gettext("Show all chats"), self)
        only_private_button = QPushButton(
                self.locale.gettext("Show only private chats"), self)
        only_public_button = QPushButton(
                self.locale.gettext("Show only public chats"), self)
        all_chats_button.clicked.connect(self.show_all_chats)
        only_private_button.clicked.connect(self.show_only_private_chats)
        only_public_button.clicked.connect(self.show_only_public_chats)
        filter_button_layout.addWidget(all_chats_button)
        filter_button_layout.addWidget(only_private_button)
        filter_button_layout.addWidget(only_public_button)

        # Buttons that choice all/don't choice any chats
        choice_button_layout = QHBoxLayout()
        choice_all_button = QPushButton(
                self.locale.gettext("Select all chats"), self)
        choice_nothing_button = QPushButton(
                self.locale.gettext("Remove selection"), self)
        choice_all_button.clicked.connect(self.choice_all_chat)
        choice_nothing_button.clicked.connect(self.choice_nothing_chat)
        choice_button_layout.addWidget(choice_all_button)
        choice_button_layout.addWidget(choice_nothing_button)

        # Button and spin that choice chats with more than N messages
        complex_choice_layot = QHBoxLayout()
        complex_choice_button = QPushButton(
                self.locale.gettext("Select chats with more than X messages"),
                self)
        # complex_choice_label = QLabel()
        # complex_choice_label.setText("complex_choice_label")
        self.complex_choice_spin = QSpinBox()
        self.complex_choice_spin.setRange(0, 1_000_000_000)
        self.complex_choice_spin.setSingleStep(100)
        self.complex_choice_spin.setValue(100)
        complex_choice_button.clicked.connect(self.complex_chat_choice)
        complex_choice_layot.addWidget(complex_choice_button, 3)
        # complex_choice_layot.addWidget(complex_choice_label)
        complex_choice_layot.addWidget(self.complex_choice_spin, 1)

        # Layout with date range
        date_range_layout = QHBoxLayout()
        today_date = datetime.date.today()
        assert today_date.year - 5 > 0
        # From date widgets
        from_date_label = QLabel()
        from_date_label.setText(
                self.locale.gettext("Analyze the time period from"))
        from_date_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.from_date = QDateEdit(QDate(today_date.year - 5,
                                         today_date.month,
                                         today_date.day))
        self.from_date.setCalendarPopup(True)
        self.from_date.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # To date widgets
        to_date_label = QLabel()
        to_date_label.setText(self.locale.gettext("to"))
        to_date_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.to_date = QDateEdit(QDate(today_date.year,
                                       today_date.month,
                                       today_date.day))
        self.to_date.setCalendarPopup(True)
        self.to_date.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        date_range_layout.addWidget(from_date_label, 5)
        date_range_layout.addWidget(self.from_date, 3)
        date_range_layout.addWidget(to_date_label, 1)
        date_range_layout.addWidget(self.to_date, 3)

        # Scroll area for features
        features_area = QScrollArea(self)
        features_wiget = QWidget()
        self.features_layout = QVBoxLayout()
        features_wiget.setLayout(self.features_layout)
        for feature in self.features:
            checkbox = QCheckBox(self.features[feature], self)
            checkbox.feature_name = feature
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
        create_report_button = QPushButton(
                self.locale.gettext("Create report"), self)
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

    def clear_chat_area(self):
        """Очищает область чатов.

        Удаляет все чекбоксы чатов при выборе нового .json-файла из области
        чатов. Не удаляет сами чаты.
        """
        if (count := self.chats_layout.count()):
            for i in range(count - 1, -1, -1):
                self.chats_layout.removeItem(self.chats_layout.itemAt(i))
        if self.chat_checkboxes:
            for i in range(len(self.chat_checkboxes) - 1, -1, -1):
                self.chat_checkboxes[i].deleteLater()
                del self.chat_checkboxes[i]

    def select_data_file(self):
        """Выбирает файл экспорта.

        Удаляет чаты и их чекбоксы, если они были, открывает окно выбора файла
        и создает новые чекбоксы на основе полученного .json-файла.
        """
        # TODO localisation?
        path, _ = QFileDialog.getOpenFileName(self, "Select data", "",
                                              "JSON Files (*.json)")
        if path:
            self.clear_chat_area()
            if self.chats:
                for i in range(len(self.chats) - 1, -1, -1):
                    del self.chats[i]
            self.data_path = path
            self.data_path_label.setText(path)
            all_chats = start_creator(path)
            print(*[(chat.name, chat.type) for chat in all_chats], sep='\n')
            self.chats = [chat for chat in all_chats
                          if (chat.type in {"personal_chat",
                                           "private_group",
                                           "private_supergroup"}
                              and chat.name is not None)]
            for chat in self.chats:
                checkbox = QCheckBox(chat.name, self)
                checkbox.chat_id = chat.id
                self.chat_checkboxes.append(checkbox)
                self.chats_layout.addWidget(checkbox)

    def show_chat_with_filter(self, key):
        """Отфильтровывает чаты для отображения.

        Показывает в области чатов только те чаты, для которых `key` возвращает
        True.

        :param key: key-функция для выбора чатов
        :type key: function
        """
        self.clear_chat_area()
        for chat in self.chats:
            if key(chat):
                checkbox = QCheckBox(chat.name, self)
                checkbox.chat_id = chat.id
                self.chat_checkboxes.append(checkbox)
                self.chats_layout.addWidget(checkbox)

    def show_all_chats(self):
        """Показывает в области чатов все чаты."""
        self.show_chat_with_filter(lambda chat: True)

    def show_only_private_chats(self):
        """Показывает в области чатов только личные чаты."""
        # TODO Есть ли другие типы личных чатов?
        self.show_chat_with_filter(lambda chat: chat.type == "personal_chat")

    def show_only_public_chats(self):
        """Показывает в области чатов только беседы чаты."""
        # TODO Есть ли другие типы групп?
        self.show_chat_with_filter(lambda chat:
                                   chat.type in ["private_group",
                                                 "private_supergroup"])

    def choice_all_chat(self):
        """Помечает выбранными все отображенные чаты."""
        for checkbox in self.chat_checkboxes:
            checkbox.setCheckState(Qt.CheckState.Checked)

    def choice_nothing_chat(self):
        """Снимает выделение со всех отображенных чатов."""
        for checkbox in self.chat_checkboxes:
            checkbox.setCheckState(Qt.CheckState.Unchecked)

    def complex_chat_choice(self):
        """Помечает только те чаты, в которых больше, чем X сообщений.

        X выбирается пользователем в виджете `complex_choice_spin`.
        """
        self.choice_nothing_chat()
        n = self.complex_choice_spin.value()
        chat_ids = {chat.id for chat in self.chats
                    if len(chat.messages) > n}
        for checkbox in self.chat_checkboxes:
            if checkbox.chat_id in chat_ids:
                checkbox.setCheckState(Qt.CheckState.Checked)

    def create_report(self):
        """Создает отчет."""
        chat_ids = {checkbox.chat_id for checkbox in self.chat_checkboxes
                    if checkbox.isChecked()}
        parsed_chats = [chat for chat in self.chats if chat.id in chat_ids]
        from_datetime = datetime.datetime.combine(
                self.from_date.date().toPyDate(),
                datetime.datetime.min.time()
                )
        to_datetime = datetime.datetime.combine(
                self.to_date.date().toPyDate(),
                datetime.datetime.max.time()
                )
        from_datetime = from_datetime.replace(tzinfo=pytz.utc)
        to_datetime = to_datetime.replace(tzinfo=pytz.utc)
        time_gap = [from_datetime, to_datetime]
        features = {checkbox.feature_name:
                    checkbox.isChecked()
                    for checkbox in self.feature_checkboxes}
        ret_stats, ret_parsed_chats = start_analyses(parsed_chats,
                                                     time_gap,
                                                     features)
        metadata = {
                "login": "TODO LOGIN",
                "chats": ret_parsed_chats,
                "time_gap": time_gap,
                }
        # TODO path
        html_export("index.html", metadata, ret_stats)
