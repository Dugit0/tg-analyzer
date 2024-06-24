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
            "units": "символов в день",
        },
        "msg": {
            "name": "Сообщения",
            "units": "сообщений в день",
        },
        "word": {
            "name": "Слова",
            "units": "слов в день",
        },
        "voice_message": {
            "name": "Голосовые сообщения",
        },
        "video_message": {
            "name": "Видеосообщения",
        },
        "video_file": {
            "name": "Видеофайлы",
        },
        "photo": {
            "name": "Фотографии",
        },
    },
    "types": {
        "chat": "По чатам",
        "user": "По пользователям",
        "date": "По дате",
        "avg": "Среднее значение",
        "quantity": "По количеству",
        "length": "По общей длительности",
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


def draw_pie(
    path: Path, data: dict, pieces: int = 5,
    pct: bool = True, amounts: bool = False,
):
    """Построение отсортированной круговой диаграммы топ-``pieces``.

    :param path: путь к конечному файлу.
    :param data: словарь данных.
    :param pieces: количество элементов в топе.
    :param pct: отображать ли подписи процентов (да/нет).
    :param amounts: отображать ли подписи процентов (да/нет).
    """
    fig, ax = plt.subplots()
    data_sorted = dict(
        sorted(data.items(), key=lambda it: it[1], reverse=True)
    )   # предварительная сортировка (в порядке убывания) по значению
    labels, values = list(data_sorted.keys()), list(data_sorted.values())
    if len(values) > pieces:
        labels[pieces:] = [TEXT["other"]]
        values[pieces:] = [sum(values[pieces:])]

    wedges, *_ = ax.pie(
        values,
        labels=(values if amounts else None),
        autopct=("%1.1f%%" if pct else None),
        labeldistance=0.875,
        pctdistance=1.25,
    )
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


# TODO Придумать, как добавить на графики единицы измерения (секунды)
def draw_voicemsg_videomsg_videos_photos(
    path: Path,
    data: dict[int, dict],
    chatnames: dict[int, str],
    feature: str,
):
    """Отрисовка графиков статистики видео-/голосовых сообщений, видео и фото.

    :param path: путь к папке, в которой сохранить изображения.
    :param data: сведения о чатах вида:
        ("photo")
            {ID чата: {имя пользователя: количество}};
        (остальные)
            {ID чата: {имя пользователя: {характеристика: количество}}}.
    :param chatnames: словарь вида {ID чата: имя чата} (для отрисовки).
    :param feature: код опции
        ("voice_message", "video_message", "video_file" или "photo").
    :return: имена файлов изображений вида:
        ("voice_message" и "video_message")
            {ID чата: {"quantity": имя, "length": имя, "avg": имя}} или
            {"agg": {"quantity": имя, "length": имя}};
        ("video_file" и "photo")
            {ID чата или "agg": {"quantity": имя}}.
    """
    # Возвращаемый словарь имен/характеристик
    ans = {}
    # Вспомогательные словари:
    # по количеству для всех чатов
    quantity_agg = defaultdict(int)
    # по суммарной длительности для всех чатов
    length_agg = defaultdict(int)
    # по количеству для каждого чата
    quantity = defaultdict(dict)
    # по суммарной длительности для каждого чата
    length = defaultdict(dict)
    # по средней длительности для каждого чата
    len_avg = defaultdict(dict)

    msg_mode = feature.endswith("_message")
    for chatid, chatdata in data.items():
        for username, userdata in chatdata.items():
            if feature == "photo":
                quantity_agg[chatnames[chatid]] += userdata
                quantity[chatid][username] = userdata
            else:
                quantity_agg[chatnames[chatid]] += userdata["quantity"]
                quantity[chatid][username] = userdata["quantity"]
            if msg_mode:
                length_agg[chatnames[chatid]] += userdata["length"]
                length[chatid][username] = userdata["length"]
                len_avg[chatid][username] = (userdata["length"]
                                            / userdata["quantity"])

    ans["agg"] = {}
    if not quantity_agg:
        return ans

    if sum(quantity_agg.values()) > 0:
        draw_pie(
            path / f"agg_{feature}_quantity.svg",
            quantity_agg, 5, pct=False, amounts=True
        )
        ans["agg"]["quantity"] = f"agg_{feature}_quantity.svg"
    else:
        ans["agg"]["quantity"] = None
    if msg_mode:
        if sum(length_agg.values()) > 0:
            draw_pie(
                path / f"agg_{feature}_length.svg",
                length_agg, 5, pct=False, amounts=True
            )
            ans["agg"]["length"] = f"agg_{feature}_length.svg"
        else:
            ans["agg"]["length"] = None

    for chatid in data:
        ans[chatid] = {}
        if not quantity[chatid]:
            continue

        if sum(quantity[chatid].values()) > 0:
            draw_pie(
                path / f"{chatid}_{feature}_quantity.svg",
                quantity[chatid], 5, pct=False, amounts=True
            )
            ans[chatid]["quantity"] = f"{chatid}_{feature}_quantity.svg"
        else:
            ans[chatid]["quantity"] = None
        if msg_mode:
            if sum(length[chatid].values()) > 0:
                draw_pie(
                    path / f"{chatid}_{feature}_length.svg",
                    length[chatid], 5, pct=False, amounts=True
                )
                ans[chatid]["length"] = f"{chatid}_{feature}_length.svg"
            else:
                ans[chatid]["length"] = None
            draw_top_bar(
                path / f"{chatid}_{feature}_lenavg.svg", len_avg[chatid]
            )
            ans[chatid]["avg"] = f"{chatid}_{feature}_lenavg.svg"

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
            case "voice_message" | "video_message" | "video_file" | "photo":
                features[feat] = draw_voicemsg_videomsg_videos_photos(
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
