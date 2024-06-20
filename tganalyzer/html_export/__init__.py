"""Модуль для сборки наглядного и читаемого HTML-файла."""

import jinja2
import os


PATH = os.path.dirname(__file__)
TEXT = {
    "title": "Анализатор статистики Telegram",
    "user": "Пользователь",
    "empty_list": "Ничего не выбрано",
    "to_top": "Наверх",
}


def html_gen(path, theme, login, features):
    """Генерация HTML-файла из списка чатов.

    :param path: путь к конечному файлу.
    :param theme: название темы.
    :param login: имя пользователя.
    :param features: словарь пар (опция, ссылка на изображение).
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(f"{PATH}/templates")
    )
    tmpl = env.get_template("index.html.jinja2")
    tmpl.stream(
        staticpath=f"{PATH}/static",
        theme=theme,
        text=TEXT,
        login=login,
        features=features,
    ).dump(path)
