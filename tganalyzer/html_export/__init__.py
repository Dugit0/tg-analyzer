"""Модуль для сборки наглядного и читаемого HTML-файла."""

import jinja2
import os


PATH = os.path.dirname(__file__)


def html_gen(path, login, features):
    """Генерация HTML-файла из списка чатов.

    :param path: путь к конечному файлу.
    :param login: имя пользователя.
    :param features: словарь пар (опция, ссылка на изображение).
    """

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(f"{PATH}/templates")
    )
    tmpl = env.get_template("index.html.jinja2")
    tmpl.stream(login=login, features=features).dump(path)
