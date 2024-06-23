"""Создает статистику по сообщениям."""
import bisect
from collections import defaultdict


# Функции подсчета

def counter_symbols(update, message, feat_meaning, feature):
    """Подсчитывает число символов каждого пользователя в каждый день.

    :param update: структура для подсчета символов.
    :type update: defaultdict[str, defaultdict[datetime, int]]
    :param message: анализируемое сообщение.
    :type message: Message
    :param feat_meaning: значение, передаваемое при вызове анализатора.
    :type feat_meaning: int/bool/str
    :param feature: название цели анализа.
    :type feature: str
    """
    num = len(message.text)
    update[message.author][message.send_time.date()] += num


def counter_words(update, message, feat_meaning, feature):
    """Подсчитывает число слов каждого пользователя в каждый день.

    :param update: структура для подсчета слов.
    :type update: defaultdict[str, defaultdict[datetime, int]]
    :param message: анализируемое сообщение.
    :type message: Message
    :param feat_meaning: значение, передаваемое при вызове анализатора.
    :type feat_meaning: int/bool/str
    :param feature: название цели анализа.
    :type feature: str
    """
    num = len(message.text.split())
    update[message.author][message.send_time.date()] += num


def counter_msgs(update, message, feat_meaning, feature):
    """Подсчитывает число сообщений каждого пользователя в каждый день.

    :param update: структура для подсчета сообщений.
    :type update: defaultdict[str, defaultdict[datetime, int]]
    :param message: анализируемое сообщение.
    :type message: Message
    :param feat_meaning: значение, передаваемое при вызове анализатора.
    :type feat_meaning: int/bool/str
    :param feature: название цели анализа.
    :type feature: str
    """
    update[message.author][message.send_time.date()] += 1


def counter_files(update, message, feat_meaning, feature):
    """Подсчитывает число и длину сообщений-файлов каждого пользователя.

    К сообщениям-файлам относятся голосовые сообщения, видео сообщения,
    и видео файлы.
    :param update: структура для подсчета количества и длины сообщений-файлов.
    :type update: defaultdict[str, defaultdict[str, int]]
    :param message: анализируемое сообщение.
    :type message: Message
    :param feat_meaning: значение, передаваемое при вызове анализатора.
    :type feat_meaning: int/bool/str
    :param feature: название цели анализа.
    :type feature: str
    """
    if message.type == feature:
        update[message.author]["quantity"] += 1
        update[message.author]["length"] += message.duration


def counter_photos(update, message, feat_meaning, feature):
    """Подсчитывает число фотографий каждого пользователя.

    :param update: структура для подсчета фотографий.
    :type update: defaultdict[str, int]
    :param message: анализируемое сообщение.
    :type message: Message
    :param feat_meaning: значение, передаваемое при вызове анализатора.
    :type feat_meaning: int/bool/str
    :param feature: название цели анализа.
    :type feature: str
    """
    if message.type == feature:
        update[message.author] += 1


def counter_days_nights(update, message, feat_meaning, feature):
    """Подсчитывает число сообщений каждого пользователя в разное время суток.

    :param update: структура для подсчета сообщений.
    :type update: defaultdict[str, defaultdict[str, int]]
    :param message: анализируемое сообщение.
    :type message: Message
    :param feat_meaning: значение, передаваемое при вызове анализатора.
    :type feat_meaning: int/bool/str
    :param feature: название цели анализа.
    :type feature: str
    """
    _time = ["night", "morning", "afternoon", "evening"]
    update[message.author][_time[message.send_time.hour // 6]] += 1


# Функции подготовки вывода

def return_text_info(update, chat_data, id):
    """Собирает текстовую информацию в одном месте (символы, слова и тп).

    :param update: общая дополняемая структура.
    :type update: dict
    :param chat_data: информация о символах ,словах и тп об одном чате.
    :type chat_data: dict
    :param id: id чата.
    :type id: int
    """
    update[id] = chat_data


# Константы

DP = {"symb": {"class_type": defaultdict,
               "class_ex_type": lambda: defaultdict(int),
               "class_func": counter_symbols,
               "return_type": dict,
               "return_func": return_text_info
               },
      "word": {"class_type": defaultdict,
               "class_ex_type": lambda: defaultdict(int),
               "class_func": counter_words,
               "return_type": dict,
               "return_func": return_text_info
               },
      "msg": {"class_type": defaultdict,
              "class_ex_type": lambda: defaultdict(int),
              "class_func": counter_msgs,
              "return_type": dict,
              "return_func": return_text_info
              },
      "voice_message": {"class_type": defaultdict,
                        "class_ex_type": lambda: defaultdict(int),
                        "class_func": counter_files,
                        "return_type": dict,
                        "return_func": return_text_info
                        },
      "video_message": {"class_type": defaultdict,
                        "class_ex_type": lambda: defaultdict(int),
                        "class_func": counter_files,
                        "return_type": dict,
                        "return_func": return_text_info
                        },
      "video_file": {"class_type": defaultdict,
                     "class_ex_type": lambda: defaultdict(int),
                     "class_func": counter_files,
                     "return_type": dict,
                     "return_func": return_text_info
                     },
      "photo": {"class_type": defaultdict,
                "class_ex_type": int,
                "class_func": counter_photos,
                "return_type": dict,
                "return_func": return_text_info
                },
      "day_night": {"class_type": defaultdict,
                    "class_ex_type": lambda: defaultdict(int),
                    "class_func": counter_days_nights,
                    "return_type": dict,
                    "return_func": return_text_info
                    }
      }


# Основные классы

class Chat_stat():
    """Класс, поля которого представляют собой статистику по чату."""

    def __init__(self, features, chat, time_gap):
        """Инициализирует объект класса, подсчитывая статистику по чату.

        :param features: какие статистики надо подсчитать.
        :type features: dict
        :param chat: анализируемый чат.
        :type chat: creator.Chat
        :param time_gap: временной промежуток рассматриваемых сообщений.
        :type time_gap: list (начальная дата и конечная)
        """
        for f in DP.keys():
            if features[f]:
                meaning = DP[f]["class_type"](DP[f]["class_ex_type"])
                setattr(self, f, meaning)

        start_mes = bisect.bisect_left(chat.messages, time_gap[0],
                                       key=lambda x: x.send_time)
        end_mes = bisect.bisect_right(chat.messages, time_gap[1],
                                      key=lambda x: x.send_time)
        for i in range(start_mes, end_mes):
            msg = chat.messages[i]
            for f in features.keys():
                if features[f]:
                    DP[f]["class_func"](getattr(self, f), msg, features[f], f)


# Основные функции

def start_analyses(parsed_chats, time_gap, features):
    """Основная функция для анализа.

    :param parsed_chats: массив объектов класса Chat из creator.
    :type parsed_chats: list
    :param time_gap: границы временного интервала.
    :type time_gap: list
    :param features: словарь с необходимыми для подсчета статистик данными.
    :type features: dict
    :return: массив, содержащий общую статистику и метаданные на отправку
    для репрезентации.
    :rtype: list
    """
    features_type = {f: DP[f]["return_type"]()
                     for f in features.keys() if features[f]}

    ret_parsed_chats = {}
    for chat in parsed_chats:
        ret_parsed_chats[chat.id] = chat   # упорядочивание для удобства html
        analysed_chat = Chat_stat(features, chat, time_gap)
        for f in features.keys():
            if features[f]:
                DP[f]["return_func"](features_type[f],
                                     getattr(analysed_chat, f),
                                     chat.id)

    ret_stats = {f: features_type[f]
                 for f in features.keys() if features[f]}

    return [ret_stats, ret_parsed_chats, time_gap]
