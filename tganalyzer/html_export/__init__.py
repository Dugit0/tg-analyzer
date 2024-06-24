"""Модуль для сборки наглядного и читаемого HTML-файла."""

import datetime
import jinja2
import matplotlib
import os
import shutil
from collections import defaultdict
from matplotlib import pyplot as plt
from pathlib import Path


PATH = Path(__file__).resolve().parent
TEXT = {
    "title": "Анализатор статистики Telegram",
    "user": "Пользователь",
    "daterange": "Диапазон дат",
    "agg_stat": "Статистика по всем чатам",
    "na": "Нет информации",
    "empty_list": "Ничего не выбрано",
    "to_top": "Наверх",
    "features": {
        "symb": {
            "name": "Символы",
            "avg_unit": "символов в день",
        },
        "msg": {
            "name": "Сообщения",
            "avg_unit": "сообщений в день",
        },
        "word": {
            "name": "Слова",
            "avg_unit": "слов в день",
        },
    },
    "types": {
        "chat": "По чатам",
        "user": "По пользователям",
        "date": "По дате",
        "avg": "Среднее количество",
    },
    "other": "Другие",
}


class daterange:
    """Итерация по диапазону дат с заданным шагом аналогично range()."""

    __slots__ = "start", "stop", "step"

    def __init__(
        self, start: datetime.date, stop: datetime.date, step: int = 1
    ):
        """Создание объекта.

        :param start: дата начала.
        :param stop: дата конца (не входит в диапазон).
        :param step: шаг итерации.
        """
        self.start, self.stop = start, stop
        self.step = datetime.timedelta(days=step)

    def __iter__(self):
        """Итерация по диапазону."""
        date = self.start
        while (self.step.days > 0 and date < self.stop
               or self.step.days < 0 and date > self.stop):
            yield date
            date += self.step

    def __len__(self):
        """Длина диапазона."""
        len = (self.stop - self.start).days / self.step.days
        return len.__ceil__() if len > 0 else 0

    def __getitem__(self, idx: int):
        """Взятие элемента диапазона.

        :param idx: индекс.
        """
        if idx not in range(len(self)):
            raise IndexError(f"{self.__class__.__name__} index out of range")
        return self.start + datetime.timedelta(days=(idx * self.step.days))

    def __str__(self):
        """Строковое представление."""
        return "{}({}, {}, {}d)".format(
            self.__class__.__name__,
            self.start.isoformat(), self.stop.isoformat(), self.step.days
        )

    __repr__ = __str__


def draw_top_bar(path: Path, data: dict, topsize: int = 3):
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
        x[topsize:], y[topsize:] = [TEXT["other"]], [sum(y[topsize:])]

    bar = ax.bar(range(len(x)), y)
    ax.set_xticks(
        range(len(x)), x,
        rotation=45, ha="right", rotation_mode="anchor"
    )
    ax.bar_label(bar)
    ax.grid(axis="y")
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


# TODO Решить проблему с 10 цветами matplotlib
def draw_date_plot(path: Path, data: dict[str, dict], label_max: int = 7):
    """Построение графика данных по дате.

    :param path: путь к конечному файлу.
    :param data: словарь данных вида {имя пользователя: {дата: данные}}.
    :param label_max: максимальное количество меток на оси дат.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    date_min, date_max = datetime.date.max, datetime.date.min
    for user, userdata in data.items():
        tmp = sorted(userdata.keys())
        if tmp[0] < date_min:
            date_min = tmp[0]
        if tmp[-1] > date_max:
            date_max = tmp[-1]
        data_sorted = {dt: userdata[dt] for dt in daterange(
            tmp[0], tmp[-1] + datetime.timedelta(days=1)
        )}  # предварительная сортировка по ключу (дате) с включением 0
        ax.plot(data_sorted.keys(), data_sorted.values(), label=user)

    ax.set_xticks(list(daterange(
        date_min, date_max,
        (((date_max - date_min).days + 1) / label_max).__ceil__()
    )))
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
    ax.grid(axis="both")
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


def draw_pie(path: Path, data: dict, pieces: int = 5):
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
        labels[pieces:] = [TEXT["other"]]
        values[pieces:] = [sum(values[pieces:])]

    wedges, _, _ = ax.pie(values, autopct="%1.1f%%", pctdistance=1.25)
    ax.legend(
        wedges, labels,
        loc="center left", bbox_to_anchor=(1, 0.5), frameon=False
    )
    fig.savefig(path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


def draw_symb_msg_word(
    path: Path,
    data: dict[int, dict[str, dict[datetime.date, int]]],
    chatnames: dict[int, str],
    feature: str,
) -> dict[str]:
    """Отрисовка графиков и сбор статистики символов/сообщений/слов.

    :param path: путь к папке, в которой сохранить изображения.
    :param data: сведения о чатах вида
        {ID чата: {имя пользователя: {дата: количество}}}.
    :param chatnames: словарь вида {ID чата: имя чата} (для отрисовки).
    :param feature: код опции ("symb", "msg" или "word").
    :return: имена файлов изображений или числовые характеристики вида
        {ID чата: {"user": имя, "date": имя, "avg": число}} или
        {"agg": {"chat": имя, "date": имя}}.
    """
    # Возвращаемый словарь имен/характеристик
    ans = {}
    # Вспомогательные словари:
    # по чатам
    by_chat_agg = defaultdict(int)
    # по пользователям и дате среди всех чатов
    by_date_agg = defaultdict(lambda: defaultdict(int))
    # по пользователям для каждого чата
    by_user = defaultdict(lambda: defaultdict(int))
    # по продолжительности каждого чата в днях
    len_days = {}

    for chatid, chatdata in data.items():
        date_min, date_max = datetime.date.max, datetime.date.min
        for username, userdata in chatdata.items():
            for date, count in userdata.items():
                if date < date_min:
                    date_min = date
                if date > date_max:
                    date_max = date
                by_chat_agg[chatnames[chatid]] += count
                by_date_agg[username][date] += count
                by_user[chatid][username] += count
        len_days[chatid] = (date_max - date_min).days + 1

    ans["agg"] = {}
    if not by_chat_agg:
        return ans

    draw_top_bar(path / f"agg_{feature}_chat.svg", by_chat_agg, 10)
    ans["agg"]["chat"] = f"agg_{feature}_chat.svg"
    draw_date_plot(path / f"agg_{feature}_date.svg", by_date_agg, 10)
    ans["agg"]["date"] = f"agg_{feature}_date.svg"

    for chatid in data:
        ans[chatid] = {}
        if not by_user[chatid]:
            continue

        if sum(by_user[chatid].values()) > 0:
            draw_pie(path / f"{chatid}_{feature}_user.svg", by_user[chatid], 5)
            ans[chatid]["user"] = f"{chatid}_{feature}_user.svg"
        else:
            ans[chatid]["user"] = None
        draw_date_plot(path / f"{chatid}_{feature}_date.svg", data[chatid], 10)
        ans[chatid]["date"] = f"{chatid}_{feature}_date.svg"
        ans[chatid]["avg"] = by_chat_agg[chatnames[chatid]] / len_days[chatid]

    return ans


def html_export(
    path: str,
    metadata: dict,
    chatdata: dict[str, dict[int, dict]],
    theme: str = "light"
):
    """Создание HTML-файла из данных о пользователе и чатах.

    :param path: путь к конечному файлу.
    :param theme: название темы.
    :param metadata: данные о пользователе вида {поле: значение}.
    :param chatdata: данные о чатах вида {опция: данные}.
    """
    matplotlib.use("svg")   # отключение интерактивного бэкенда

    abspath = Path(path).resolve()
    files_dir = abspath.parent / f"{abspath.name.replace('.', '_')}_files"
    os.makedirs(files_dir, exist_ok=True)
    shutil.copyfile(PATH / "themes" / f"{theme}.css", files_dir / "style.css")

    chatnames = {
        chatid: chat.name for chatid, chat in metadata["chats"].items()
    }
    features = defaultdict(lambda: defaultdict(str))
    for feat in TEXT["features"]:
        if feat not in chatdata:
            continue
        match feat:
            case "symb" | "msg" | "word":
                features[feat] = draw_symb_msg_word(
                    files_dir, chatdata[feat], chatnames, feat
                )

    chatstat = defaultdict(lambda: defaultdict(str))
    for feat, featdata in features.items():
        for chat, stat in featdata.items():
            chatstat[chat][feat] = stat

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(PATH / "templates")
    )
    tmpl = env.get_template("index.html.jinja2")
    tmpl.stream(
        files_dir=files_dir.name,
        text=TEXT,
        metadata=metadata,
        chatstat=chatstat,
    ).dump(path)
