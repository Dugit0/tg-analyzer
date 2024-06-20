#!/bin/bash
pybabel extract -o gui.pot __init__.py &&
# pybabel init -D gui -l ru_RU.UTF-8 -d po -i gui.pot &&
pybabel update --previous --ignore-pot-creation-date -D gui -d po -i gui.pot &&
pybabel compile -D gui -l ru_RU.UTF-8 -d po -i po/ru_RU.UTF-8/LC_MESSAGES/gui.po
rm gui.pot
