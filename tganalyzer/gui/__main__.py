import argparse
import sys
from PyQt5.QtWidgets import QApplication
from . import MainWindow

LANGUAGES = ['en', 'ru']

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
    window = MainWindow()
    sys.exit(app.exec_())
else:
    print(f"Unexpected language: {args.language}", file=sys.stderr)
    print(f"One of these languages was expected: {', '.join(LANGUAGES)}", file=sys.stderr)
    sys.exit(1)
