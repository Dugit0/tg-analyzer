"""Создает статистику по сообщениям."""
import bisect
from . import creator
import datetime
from collections import defaultdict


# Функции подсчета

def counter_symbols(
        update: defaultdict[str, defaultdict[datetime.datetime.date, int]],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число символов каждого пользователя в каждый день.

    :param update: структура для подсчета символов.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    update[message.author][message.send_time.date()] += len(message.text)


def counter_words(
        update: defaultdict[str, defaultdict[datetime.datetime.date, int]],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число слов каждого пользователя в каждый день.

    :param update: структура для подсчета слов.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    update[message.author][message.send_time.date()] += \
        len(message.text.split())


def counter_msgs(
        update: defaultdict[str, defaultdict[datetime.datetime.date, int]],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число сообщений каждого пользователя в каждый день.

    :param update: структура для подсчета сообщений.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    update[message.author][message.send_time.date()] += 1


def counter_files(
        update: defaultdict[str, defaultdict[str, int]],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число и длину сообщений-файлов каждого пользователя.

    К сообщениям-файлам относятся голосовые сообщения, видео сообщения,
    и видео файлы.
    :param update: структура для подсчета количества и длины сообщений-файлов.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    if message.type == feature:
        update[message.author]["quantity"] += 1
        update[message.author]["length"] += message.duration


def counter_photos(
        update: defaultdict[str, int],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число фотографий каждого пользователя.

    :param update: структура для подсчета фотографий.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    if message.type == feature:
        update[message.author] += 1


def counter_days_nights(
        update: defaultdict[str, defaultdict[str, int]],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число сообщений каждого пользователя в разное время суток.

    :param update: структура для подсчета сообщений.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    _time = ["night", "morning", "afternoon", "evening"]
    update[message.author][_time[message.send_time.hour // 6]] += 1


def counter_links(
        update: defaultdict[str, defaultdict[str, int]],
        message: creator.Message,
        feature: str
        ):
    """Подсчитывает число ссылок каждого пользователя в сообщениях.
    :param update: структура для подсчета ссылок.
    :param message: анализируемое сообщение.
    :param feature: название цели анализа.
    """
    if message.has_links:
        for syte in message.links.keys():
            update[message.author][syte] += message.links[syte]


# Функции подготовки вывода

def return_text_info(
        update: dict[int, defaultdict],
        chat_data: defaultdict,
        id: int
        ):
    """Собирает текстовую информацию в одном месте (символы, слова и тп).

    :param update: общая дополняемая структура.
    :param chat_data: информация о символах ,словах и тп об одном чате.
    :param id: id чата.
    """
    update[id] = chat_data


# Константы

DEPENDENCIES = {
        "symb": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_symbols,
            "return_type": dict,
            "return_func": return_text_info
        },
        # symb structure in final data:
        # "symb": {
        #   chat.id: {
        #       "username": {
        #           datetime.datetime.date: int
        #       }
        #   }
        # }
        "word": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_words,
            "return_type": dict,
            "return_func": return_text_info
        },
        # word structure in final data:
        # "word": {
        #   chat.id: {
        #       "username": {
        #           datetime.datetime.date: int
        #       }
        #   }
        # }
        "msg": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_msgs,
            "return_type": dict,
            "return_func": return_text_info
        },
        # msg structure in final data:
        # "msg": {
        #   chat.id: {
        #       "username": {
        #           datetime.datetime.date: int
        #       }
        #   }
        # }
        "voice_message": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_files,
            "return_type": dict,
            "return_func": return_text_info
        },
        # voice_message structure in final data:
        # "voice_message": {
        #   chat.id: {
        #       "username": {
        #           "quantity": int,
        #           "length": int
        #       }
        #   }
        # }
        "video_message": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_files,
            "return_type": dict,
            "return_func": return_text_info
        },
        # video_message structure in final data:
        # "video_message": {
        #   chat.id: {
        #       "username": {
        #           "quantity": int,
        #           "length": int
        #       }
        #   }
        # }
        "video_file": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_files,
            "return_type": dict,
            "return_func": return_text_info
        },
        # video_file structure in final data:
        # "video_file": {
        #   chat.id: {
        #       "username": {
        #           "quantity": int,
        #           "length": int
        #       }
        #   }
        # }
        "photo": {
            "class_type": defaultdict,
            "class_ex_type": int,
            "class_func": counter_photos,
            "return_type": dict,
            "return_func": return_text_info
        },
        # photo structure in final data:
        # "photo": {
        #   chat.id: {
        #       "username": int
        #       }
        #   }
        # }
        "day_night": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_days_nights,
            "return_type": dict,
            "return_func": return_text_info
        },
        # day_night structure in final data:
        # "day_night": {
        #   chat.id: {
        #       "username": {
        #           "night": int,
        #           "morning": int,
        #           "afternoon": int,
        #           "evening": int
        #       }
        #   }
        # }
        "phone_call": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_files,
            "return_type": dict,
            "return_func": return_text_info
        },
        # phone_call structure in final data:
        # "phone_call": {
        #   chat.id: {
        #       "username": {
        #           "quantity": int,
        #           "length": int
        #       }
        #   }
        # }
        "group_call": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_files,
            "return_type": dict,
            "return_func": return_text_info
        },
        # group_call structure in final data:
        # "group_call": {
        #   chat.id: {
        #       "username": {
        #           "quantity": int,
        #           "length": int
        #       }
        #   }
        # }
        "links": {
            "class_type": defaultdict,
            "class_ex_type": lambda: defaultdict(int),
            "class_func": counter_links,
            "return_type": dict,
            "return_func": return_text_info
        },
        # links structure in final data:
        # "links": {
        #   chat.id: {
        #       "username": {
        #           "syte": int
        #       }
        #   }
        # }
    }


# Основные классы

class Chat_stat():
    """Класс, поля которого представляют собой статистику по чату."""

    def __init__(
            self,
            features: dict[str, bool],
            chat: creator.Chat,
            time_gap: tuple[datetime.datetime, datetime.datetime]
            ):
        """Инициализирует объект класса, подсчитывая статистику по чату.

        :param features: какие статистики надо подсчитать.
        :param chat: анализируемый чат.
        :param time_gap: временной промежуток рассматриваемых сообщений.
        Начальная дата и конечная, aware.
        """
        for feature in DEPENDENCIES.keys():
            if features[feature]:
                setattr(self,
                        feature,
                        DEPENDENCIES[feature]["class_type"](
                                DEPENDENCIES[feature]["class_ex_type"]))

        start_mes = bisect.bisect_left(chat.messages, time_gap[0],
                                       key=lambda x: x.send_time)
        end_mes = bisect.bisect_right(chat.messages, time_gap[1],
                                      key=lambda x: x.send_time)
        for i in range(start_mes, end_mes):
            msg = chat.messages[i]
            for feature in features.keys():
                if features[feature]:
                    DEPENDENCIES[feature]["class_func"](
                            getattr(self, feature), msg, feature)


# Основные функции

def start_analyses(
        parsed_chats: list[creator.Chat],
        time_gap: tuple[datetime.datetime, datetime.datetime],
        features: dict[str, bool]
        ) -> tuple[dict, dict[int, creator.Chat]]:
    """Основная функция для анализа.

    :param parsed_chats: массив объектов класса Chat из creator.
    :param time_gap: границы временного интервала (aware).
    :param features: словарь с необходимыми для подсчета статистик данными.
    :return: массив, содержащий общую статистику и метаданные на отправку
    для репрезентации. Общая статистика представляет собой словарь, где
    ключом является имя опции, а значением - возврааемая структура опции,
    опеределенная отдельно для каждой опции.
    """
    # Словарь, хранящий заведенные структуры для опций.
    features_type = {feature: DEPENDENCIES[feature]["return_type"]()
                     for feature in features.keys() if features[feature]}

    ret_parsed_chats = {}
    for chat in parsed_chats:
        ret_parsed_chats[chat.id] = chat   # упорядочивание для удобства html
        analysed_chat = Chat_stat(features, chat, time_gap)
        for feature in features.keys():
            if features[feature]:
                DEPENDENCIES[feature]["return_func"](
                        features_type[feature],
                        getattr(analysed_chat, feature),
                        chat.id)

    ret_stats = {feature: features_type[feature]
                 for feature in features.keys() if features[feature]}

    return ret_stats, ret_parsed_chats
