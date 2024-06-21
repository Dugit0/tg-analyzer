"""Модуль для сборки наглядного и читаемого HTML-файла."""

import datetime
import jinja2
import os
from collections import defaultdict
from matplotlib import pyplot as plt


def draw_msg(
    path: str,
    msgdata: dict[int, dict[str, dict[datetime.date, int]]]
) -> dict:
    """Отрисовка графиков статистики сообщений.

    :param path: путь к папке, в которой сохранить изображения.
    :param msgdata: сведения о сообщениях вида
        {ID чата: {имя пользователя: {дата: количество сообщений}}}.
    :return: пути к изображениям вида {код опции: путь}.
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

    for chatid, chatdata in msgdata.items():
        for username, userdata in chatdata.items():
            for date, count in userdata.items():
                by_chat_agg[chatid] += count
                by_date_agg[date] += count
                by_user[chatid][username] += count
                by_date[chatid][date] += count

    # Возвращаемый словарь путей
    ans = {}

    # Построение отсортированной столбчатой диаграммы по всем чатам
    ans["agg_msg_all"] = f"{path}/agg_msg_all.svg"
    fig, ax = plt.subplots(figsize=(len(by_chat_agg) + 1, 5))
    by_chat_agg = dict(
        sorted(by_chat_agg.items(), key=lambda it: it[1], reverse=True)
    )   # предварительная сортировка (в порядке убывания) по значению (кол-ву)
    ax.bar(range(len(by_chat_agg)), by_chat_agg.values())
    ax.set_xticks(range(len(by_chat_agg)), by_chat_agg.keys())
    fig.savefig(ans["agg_msg_all"], format="svg", transparent=True)

    # Построение графика по дате среди всех чатов
    ans["agg_msg_day"] = f"{path}/agg_msg_day.svg"
    fig, ax = plt.subplots(figsize=(len(by_date_agg) + 1, 5))
    by_date_agg = dict(
        sorted(by_date_agg.items(), key=lambda it: it[0])
    )   # предварительная сортировка по ключу (дате)
    ax.plot(range(len(by_date_agg)), by_date_agg.values())
    ax.set_xticks(range(len(by_date_agg)), by_date_agg.keys())
    fig.savefig(ans["agg_msg_day"], format="svg", transparent=True)

    # Построение по каждому чату:
    for chatid in msgdata:
        # круговой диаграммы по пользователям
        ans[f"msg_person_{chatid}"] = f"{path}/msg_person_{chatid}.svg"
        fig, ax = plt.subplots()
        ax.pie(
            by_user[chatid].values(),
            labels=by_user[chatid].keys(),
            autopct="%1.1f%%"
        )
        fig.savefig(ans[f"msg_person_{chatid}"],
                    format="svg", transparent=True)

        # графика по дате
        ans[f"msg_day_{chatid}"] = f"{path}/msg_day_{chatid}.svg"
        fig, ax = plt.subplots(figsize=(len(by_date[chatid]) + 1, 5))
        by_date[chatid] = dict(
            sorted(by_date[chatid].items(), key=lambda it: it[0])
        )   # предварительная сортировка по ключу (дате)
        ax.plot(range(len(by_date[chatid])), by_date[chatid].values())
        ax.set_xticks(range(len(by_date[chatid])), by_date[chatid].keys())
        fig.savefig(ans[f"msg_day_{chatid}"], format="svg", transparent=True)

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

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(f"{PATH}/templates")
    )
    tmpl = env.get_template("index.html.jinja2")
    tmpl.stream(
        staticpath=f"{PATH}/static",
        theme=theme,
        text=TEXT,
        login=metadata["login"],
        features=draw_msg(files_dir, chatdata["msg"]),
    ).dump(path)
