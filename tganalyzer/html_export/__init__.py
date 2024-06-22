"""Модуль для сборки наглядного и читаемого HTML-файла."""

import datetime
import jinja2
import os
import shutil
from collections import defaultdict
from matplotlib import pyplot as plt


def draw_msg_word(
    path: str,
    data: dict[int, dict[str, dict[datetime.date, int]]],
    feature: str,
) -> dict:
    """Отрисовка графиков статистики сообщений/слов.

    :param path: путь к папке, в которой сохранить изображения.
    :param data: сведения о чатах вида
        {ID чата: {имя пользователя: {дата: количество сообщений/слов}}}.
    :param feature: код опции ("msg" или "word").
    :return: названия файлов изображений вида
        {ID чата: {"user": путь, "date": путь}} или
        {"agg": {"chat": путь, "date": путь}}.
    """
    # Вспомогательные словари:
    # по чатам
    by_chat_agg = defaultdict(int)
    # по дате среди всех чатов
    by_date_agg = defaultdict(int)
    # по пользователям для каждого чата
    by_user = defaultdict(lambda: defaultdict(int))
    # по дате для каждого чата
    by_date = defaultdict(lambda: defaultdict(int))

    for chatid, chatdata in data.items():
        for username, userdata in chatdata.items():
            for date, count in userdata.items():
                by_chat_agg[chatid] += count
                by_date_agg[date] += count
                by_user[chatid][username] += count
                by_date[chatid][date] += count

    # Возвращаемый словарь путей
    ans = {}

    ans["agg"] = {}
    # Построение отсортированной столбчатой диаграммы по всем чатам
    fig, ax = plt.subplots(figsize=(len(by_chat_agg) + 1, 5))
    by_chat_agg = dict(
        sorted(by_chat_agg.items(), key=lambda it: it[1], reverse=True)
    )   # предварительная сортировка (в порядке убывания) по значению (кол-ву)
    ax.bar(range(len(by_chat_agg)), by_chat_agg.values())
    ax.set_xticks(range(len(by_chat_agg)), by_chat_agg.keys())
    fig.savefig(f"{path}/agg_{feature}_chat.svg",
                format="svg", transparent=True)
    plt.close(fig)
    ans["agg"]["chat"] = f"agg_{feature}_chat.svg"

    # Построение графика по дате среди всех чатов
    fig, ax = plt.subplots(figsize=(len(by_date_agg) + 1, 5))
    by_date_agg = dict(
        sorted(by_date_agg.items(), key=lambda it: it[0])
    )   # предварительная сортировка по ключу (дате)
    ax.plot(range(len(by_date_agg)), by_date_agg.values())
    ax.set_xticks(range(len(by_date_agg)), by_date_agg.keys())
    fig.savefig(f"{path}/agg_{feature}_date.svg",
                format="svg", transparent=True)
    plt.close(fig)
    ans["agg"]["date"] = f"agg_{feature}_date.svg"

    # Построение по каждому чату:
    for chatid in data:
        ans[chatid] = {}
        # круговой диаграммы по пользователям
        fig, ax = plt.subplots()
        ax.pie(
            by_user[chatid].values(),
            labels=by_user[chatid].keys(),
            autopct="%1.1f%%"
        )
        fig.savefig(f"{path}/{chatid}_{feature}_user.svg",
                    format="svg", transparent=True)
        plt.close(fig)
        ans[chatid]["user"] = f"{chatid}_{feature}_user.svg"

        # графика по дате
        fig, ax = plt.subplots(figsize=(len(by_date[chatid]) + 1, 5))
        by_date[chatid] = dict(
            sorted(by_date[chatid].items(), key=lambda it: it[0])
        )   # предварительная сортировка по ключу (дате)
        ax.plot(range(len(by_date[chatid])), by_date[chatid].values())
        ax.set_xticks(range(len(by_date[chatid])), by_date[chatid].keys())
        fig.savefig(f"{path}/{chatid}_{feature}_date.svg",
                    format="svg", transparent=True)
        plt.close(fig)
        ans[chatid]["date"] = f"{chatid}_{feature}_date.svg"

    return ans


PATH = os.path.dirname(__file__)
TEXT = {
    "title": "Анализатор статистики Telegram",
    "user": "Пользователь",
    "empty_list": "Ничего не выбрано",
    "to_top": "Наверх",
}


def html_export(path: str, theme: str, metadata: dict, chatdata: dict):
    """Создание HTML-файла из данных о пользователе и чатах.

    :param path: путь к конечному файлу.
    :param theme: название темы.
    :param metadata: данные о пользователе вида {поле: значение}.
    :param chatdata: данные о чатах вида {опция: данные}.
    """
    path = os.path.abspath(path)
    dirname, basename = os.path.dirname(path), os.path.basename(path)
    basename_nodots = basename.replace(".", "_")
    files_dir = f"{dirname}/{basename_nodots}_files"
    os.makedirs(files_dir, exist_ok=True)
    shutil.copy(f"{PATH}/themes/{theme}.css", f"{files_dir}/style.css")

    features = {}
    for feat, data in chatdata.items():
        if feat in ("msg", "word"):
            features[feat] = draw_msg_word(files_dir, data, feat)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(f"{PATH}/templates")
    )
    tmpl = env.get_template("index.html.jinja2")
    tmpl.stream(
        files_dir=os.path.basename(files_dir),
        text=TEXT,
        login=metadata["login"],
        features=features,
    ).dump(path)
