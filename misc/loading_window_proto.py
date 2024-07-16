from PySide6.QtCore import (Qt, Signal, Slot, QObject, QDate, QRunnable, QThreadPool)
from PySide6.QtWidgets import (QMainWindow, QFileDialog, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QDateEdit,
                               QCheckBox, QScrollArea, QSpinBox, QComboBox,
                               QApplication, QProgressBar, QDialog)
from pathlib import Path
import time
import datetime
import gettext
import pytz
import webbrowser
import traceback
import sys




class WorkerSignals(QObject):
    """
    Определяет сигналы доступные в выполняющемся треде класса Worker.

    Поддерживаемые сигналы:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object результат выполнения функции треда
    """

    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """
    Обертка над тредом.

    Унаследован от QRunnable. Создает и присоединяет сигналы к треду.

    :param func: Функция запускающаяся в треде.
    :type func: function
    :param args: ``args`` передающиеся в ``func``
    :param kwargs: ``kwargs`` передающиеся в ``func``
    """

    def __init__(self, func, *args, progress_flag=False):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.func = func
        self.args = args
        self.progress_flag = progress_flag
        self.signals = WorkerSignals()

    @Slot()  # QtCore.Slot
    def run(self):
        """Запускает функцию с параметрами ``args`` и ``kwargs``."""
        try:
            if self.progress_flag:
                result = self.func(*self.args,
                                   progress=self.signals.progress)
            else:
                result = self.func(*self.args)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            # Done
            self.signals.finished.emit()

def payload(progress):
    n = 5
    for i in range(101):
        progress.emit(i)
        time.sleep(n/100)

class CustomDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")
        self.progress_bar = QProgressBar(self)

        # QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.progress_bar)
        # self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def update_wigets(self, percent):
        # self.label.setText(f"Progress is {percent}%")
        self.progress_bar.setValue(percent)



class MainWindow(QMainWindow):
    """Основное окно приложения."""

    def __init__(self, *args, **kwargs):
        """Основное окно приложения.

        :param lang: название языка, для которого поддерживается перевод.
        :type lang: str
        """
        super(MainWindow, self).__init__()
        self.setGeometry(300, 100, 500, 300)
        self.threadpool = QThreadPool()
        self.label = QLabel("MEOW")
        # self.button = QPushButton("Button")
        # self.button.clicked.connect(lambda : self.update_label(12))
        
        layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("proto")

        self.show()
        
        dialog = CustomDialog(self)
        
        worker = Worker(payload, progress_flag=True)
        worker.signals.progress.connect(dialog.update_wigets)
        self.threadpool.start(worker)

        dialog.exec()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("proto")
    window = MainWindow()
    sys.exit(app.exec())
