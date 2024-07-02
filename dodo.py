from doit.task import clean_targets
from glob import iglob
from shutil import rmtree

DOIT_CONFIG = {
        "default_tasks": ["wheel"],
        "cleanforget": True,
}

def task_pot():
    "extract text for translation"
    return {
        "actions": [
            "pybabel extract -o tganalyzer/gui/gui.pot tganalyzer/gui/__init__.py",
            "pybabel extract -o tganalyzer/html_export/html_export.pot tganalyzer/html_export/__init__.py",
        ],
        "file_dep": [
            "tganalyzer/gui/__init__.py",
            "tganalyzer/html_export/__init__.py",
        ],
        "targets": [
            "tganalyzer/gui/gui.pot",
            "tganalyzer/html_export/html_export.pot",
        ],
        "clean": [clean_targets],
    }

def task_po():
    "update translation files"
    return {
        "actions": [
            "pybabel update --previous -D gui -d tganalyzer/gui/po -i tganalyzer/gui/gui.pot",
            "pybabel update --previous -D html_export -d tganalyzer/html_export/po -i tganalyzer/html_export/html_export.pot"
        ],
        "file_dep": [
            "tganalyzer/gui/gui.pot",
            "tganalyzer/html_export/html_export.pot",
        ],
        "targets": [
            "tganalyzer/gui/po/ru_RU.UTF-8/LC_MESSAGES/gui.po",
            "tganalyzer/html_export/po/ru_RU.UTF-8/LC_MESSAGES/html_export.po",
        ],
    }

def task_mo():
    "compile translation files"
    return {
        "actions": [
            "mkdir -p tganalyzer/gui/po",
            "pybabel compile -D gui -l ru_RU.UTF-8 -d tganalyzer/gui/po -i tganalyzer/gui/po/ru_RU.UTF-8/LC_MESSAGES/gui.po",
            "mkdir -p tganalyzer/html_export/po",
            "pybabel compile -D html_export -l ru_RU.UTF-8 -d tganalyzer/html_export/po -i tganalyzer/html_export/po/ru_RU.UTF-8/LC_MESSAGES/html_export.po",
        ],
        "file_dep": [
            "tganalyzer/gui/po/ru_RU.UTF-8/LC_MESSAGES/gui.po",
            "tganalyzer/html_export/po/ru_RU.UTF-8/LC_MESSAGES/html_export.po",
        ],
        "targets": [
            "tganalyzer/gui/po/ru_RU.UTF-8/LC_MESSAGES/gui.mo",
            "tganalyzer/html_export/po/ru_RU.UTF-8/LC_MESSAGES/html_export.mo",
        ],
        "clean": [clean_targets],
    }

def task_i18n():
    "do full translation cycle"
    return {
        "actions": None,
        "task_dep": ["pot", "po", "mo"],
    }

def task_html():
    "generate HTML documentation"
    return {
        "actions": ["sphinx-build -M html doc/src doc/build"],
        "file_dep": [*iglob("doc/src/*.rst"), *iglob("tganalyzer/*/*.py")],
        "clean": [(rmtree, ["doc/build"])],
        "task_dep": ["i18n"],
    }


def task_test():
    "Run tests."
    return {
        "actions": [
            "python -m unittest tests_tganalyzer/core_test.py",
        ],
        "task_dep": ["i18n"],
    }

def task_coverage():
    "Show test coverage."
    return {
        "actions": [
            "python -m coverage run -m unittest tests_tganalyzer/core_test.py",
            "python -m coverage report -m",
            "rm .coverage",
        ],
        'verbosity': 2,
        "task_dep": ["i18n"],
    }

def task_wheel():
    "build a wheel (binary distribution)"
    return {
        "actions": ["python -m build -nw"],
        "task_dep": ["i18n"],
    }
