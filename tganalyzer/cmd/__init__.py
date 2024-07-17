"""CLI для запуска GUI. Для более подробной информации см. `--help`."""
import argparse
import sys
from PySide6.QtWidgets import QApplication
from tganalyzer.gui import MainWindow


def start_cmd():
    """Запускает CLI интерфейс."""
    LANGUAGES = {'en': 'en_US.UTF-8',
                 'ru': 'ru_RU.UTF-8',
                 }

    parser = argparse.ArgumentParser(
            prog='tg-analyzer',
            description='Message analyzer for Telegram')
    parser.add_argument('-l', '--language',
                        default='en')
    args = parser.parse_args()
    if args.language in LANGUAGES:
        print(args.language)
        app = QApplication(sys.argv)
        app.setApplicationName("tg-analyzer")
        window = MainWindow(lang=LANGUAGES[args.language])
        sys.exit(app.exec())
    else:
        print(f"Unexpected language: {args.language}", file=sys.stderr)
        print(f"One of these languages was expected: {', '.join(LANGUAGES)}",
              file=sys.stderr)
        sys.exit(1)
