from doit.task import clean_targets
from glob import iglob
import shutil
from pathlib import Path

DOIT_CONFIG = {
        "default_tasks": ["wheel"],
        "cleanforget": True,
}


def task_pot():
    """Extract text for translation and recreate .pot file."""
    file_dep = [
            Path('tganalyzer') / 'gui' / '__init__.py',
            Path('tganalyzer') / 'html_export' / '__init__.py',
            ]
    targets = [
            'gui.pot',
            'html_export.pot',
            ]
    return {
            "actions": [
                f"pybabel extract -o {i[0]} {i[1]}"
                for i in zip(targets, file_dep)
                ],
            "file_dep": file_dep,
            "targets": targets,
            "clean": [clean_targets],
            }


def task_po():
    """Update translation files."""
    domains = [
            'gui',
            'html_export',
            ]
    po_path = Path('tganalyzer') / 'po'
    return {
            "actions": [
                f"pybabel update --previous -D {domain} -d {po_path} "
                f"-i {domain + '.pot'}" for domain in domains
                ],
            "file_dep": [f"{domain}.pot" for domain in domains],
            "targets": [
                po_path / 'ru_RU.UTF-8' / 'LC_MESSAGES' / f"{domain}.pot"
                for domain in domains
                ],
            }


def task_mo():
    """Compile translation files."""
    domains = [
            'gui',
            'html_export',
            ]
    po_path = Path('tganalyzer') / 'po'
    return {
            "actions": [
                f"pybabel compile -D {domain} -l ru_RU.UTF-8 -d {po_path} -i "
                f"{po_path / 'ru_RU.UTF-8' / 'LC_MESSAGES' / (domain + '.po')}"
                for domain in domains
                ],
            "file_dep": [
                po_path / 'ru_RU.UTF-8' / 'LC_MESSAGES' / (domain + '.po')
                for domain in domains
                ],
            "targets": [
                po_path / 'ru_RU.UTF-8' / 'LC_MESSAGES' / (domain + '.mo')
                for domain in domains
                ],
            "clean": [clean_targets],
            }


def task_i18n():
    """Do full translation cycle."""
    return {
        "actions": None,
        "task_dep": ["pot", "po", "mo"],
    }


def task_html():
    """Generate HTML documentation."""
    return {
        "actions": ["sphinx-build -M html doc/src doc/build"],
        "file_dep": [*iglob("doc/src/*.rst"), *iglob("tganalyzer/*/*.py")],
        "clean": [(shutil.rmtree, ["doc/build"])],
        "task_dep": ["i18n"],
    }


def task_test():
    """Run tests."""
    return {
        "actions": [
            "python -m unittest tests_tganalyzer/core_test.py",
        ],
        "task_dep": ["i18n"],
    }


def task_coverage():
    """Show test coverage."""
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
    """Build a wheel (binary distribution)."""
    return {
        "actions": ["python -m build -nw"],
        "task_dep": ["i18n"],
        "clean": [
            (shutil.rmtree, ['dist']),
            (shutil.rmtree, ['tganalyzer.egg-info']),
            (shutil.rmtree, ['build']),
            ]
    }
