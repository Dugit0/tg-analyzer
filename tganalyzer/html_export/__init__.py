"""Модуль для сборки наглядного и читаемого HTML-файла."""

import datetime
import jinja2
import os
import shutil
from collections import defaultdict
from matplotlib import pyplot as plt


def daterange(start: datetime.date, stop: datetime.date, step: int = 1):
    """Итерация по диапазону дат с заданным шагом аналогично range().

    :param start: дата начала.
    :param stop: дата конца (не входит в диапазон).
    :param step: шаг итерации.
    """
    date = start
    while (step > 0 and date < stop) or (step < 0 and date > stop):
        yield date
        date += datetime.timedelta(days=step)


def draw_top_bar(path: str, data: dict, topsize: int = 3):
    """Построение отсортированной столбчатой диаграммы топ-``topsize``.

    :param path: путь к конечному файлу.
    :param data: словарь данных с ключами-метками.
    :param topsize: количество элементов в топе.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    data_sorted = dict(
        sorted(data.items(), key=lambda it: it[1], reverse=True)
    )   # предварительная сортировка (в порядке убывания) по значению
    x, y = list(data_sorted.keys()), list(data_sorted.values())
    if len(y) > topsize:
        x[topsize:], y[topsize:] = ["other"], [sum(y[topsize:])]

    bar = ax.bar(range(len(x)), y)
    ax.set_xticks(range(len(x)), x)
    ax.bar_label(bar)
    ax.grid(axis="y")
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


def draw_date_plot(path: str, data: dict, label_max: int = 7):
    """Построение графика данных по дате.

    :param path: путь к конечному файлу.
    :param data: словарь данных с ключами класса ``datetime.date``.
    :param label_max: максимальное количество меток на оси дат.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    data_sorted = {dt: data[dt] for dt in daterange(
        min(data.keys()), max(data.keys()) + datetime.timedelta(days=1)
    )}  # предварительная сортировка по ключу (дате) с включением 0
    x, y = list(data_sorted.keys()), list(data_sorted.values())

    ax.plot(range(len(x)), y)
    label_pos = list(range(0, len(x), (len(x) / label_max).__ceil__()))
    ax.set_xticks(label_pos, [x[i] for i in label_pos])
    ax.grid(axis="both")
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


def draw_pie(path: str, data: dict, pieces: int = 5):
    """Построение отсортированной круговой диаграммы топ-``pieces``.

    :param path: путь к конечному файлу.
    :param data: словарь данных.
    :param pieces: количество элементов в топе.
    """
    fig, ax = plt.subplots()
    data_sorted = dict(
        sorted(data.items(), key=lambda it: it[1], reverse=True)
    )   # предварительная сортировка (в порядке убывания) по значению
    labels, values = list(data_sorted.keys()), list(data_sorted.values())
    if len(values) > pieces:
        labels[pieces:], values[pieces:] = ["other"], [sum(values[pieces:])]

    ax.pie(values, labels=labels, autopct="%1.1f%%")
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


def draw_msg_word(
    path: str,
    data: dict[int, dict[str, dict[datetime.date, int]]],
    feature: str,
) -> dict:
    """Отрисовка графиков и сбор статистики сообщений/слов.

    :param path: путь к папке, в которой сохранить изображения.
    :param data: сведения о чатах вида
        {ID чата: {имя пользователя: {дата: количество сообщений/слов}}}.
    :param feature: код опции ("msg" или "word").
    :return: названия файлов изображений вида
        {ID чата: {"user": путь, "date": путь, "avg": число}} или
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

    draw_top_bar(f"{path}/agg_{feature}_chat.svg", by_chat_agg, 10)
    ans["agg"]["chat"] = f"agg_{feature}_chat.svg"

    draw_date_plot(f"{path}/agg_{feature}_date.svg", by_date_agg, 15)
    ans["agg"]["date"] = f"agg_{feature}_date.svg"

    for chatid in data:
        ans[chatid] = {}

        draw_pie(f"{path}/{chatid}_{feature}_user.svg", by_user[chatid], 5)
        ans[chatid]["user"] = f"{chatid}_{feature}_user.svg"

        draw_date_plot(
            f"{path}/{chatid}_{feature}_date.svg",
            by_date[chatid],
            15
        )
        ans[chatid]["date"] = f"{chatid}_{feature}_date.svg"

        # среднее число сообщений в день
        dates_sorted = list(by_date[chatid].keys())
        delta = (dates_sorted[-1] - dates_sorted[0]).days
        ans[chatid]["avg"] = sum(by_date[chatid].values()) / delta

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
