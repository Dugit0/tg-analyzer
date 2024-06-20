"""Создает статистику по сообщениям."""
import bisect
import matplotlib.pyplot as plt
from collections import defaultdict


# Функции подсчета

def counter_symbols(update, message, feat_meaning):
    update[message.author][message.send_time.date()] += len(message.text)


def counter_words(update, message, feat_meaning):
    update[message.author][message.send_time.date()] += len(message.text.split())


def counter_msgs(update, message, feat_meaning):
    update[message.author][message.send_time.date()] += 1


# Функции подготовки вывода

def return_text_info(update, chat_data, id):
    update[id] = chat_data


# Константы

DEPENDENCIES = {"symb": {"class_type": defaultdict,
                         "class_extra_type": defaultdict,
                         "class_func": counter_symbols,
                         "return_type": dict,
                         "return_func": return_text_info
                        },
                "word": {"class_type": defaultdict,
                         "class_extra_type": defaultdict,
                         "class_func": counter_words,
                         "return_type": dict,
                         "return_func": return_text_info
                        },
                "msg": {"class_type": defaultdict,
                        "class_extra_type": defaultdict,
                        "class_func": counter_msgs,
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

        for feature in DEPENDENCIES.keys():
            if features[feature]:
                tmp_type = int
                if "class_extra_type" in DEPENDENCIES[feature].keys():
                    tmp_type = lambda: DEPENDENCIES[feature]["class_extra_type"](int)
                setattr(self, feature, 
                        DEPENDENCIES[feature]["class_type"](tmp_type))

        start_mes = bisect.bisect_left(chat.messages, time_gap[0],
                                        key=lambda x : x.send_time)
        end_mes = bisect.bisect_right(chat.messages, time_gap[1],
                                      key=lambda x : x.send_time)
        for i in range(start_mes, end_mes):
            message = chat.messages[i]
            for feature in features.keys():
                if features[feature]:
                    DEPENDENCIES[feature]["class_func"](getattr(self, feature), message, features[feature])


# Основные функции

def start_analyses(parsed_chats, time_gap, 
                   features, output_folder):
    """Основная функция для анализа.

    :param parsed_chats: массив объектов класса Chat из creator.
    :type parsed_chats: list
    :param chat_ids: id чатов, которые будут анализироваться.
    :type chat_ids: list
    :param time_gap: границы временного интервала.
    :type time_gap: list
    :param features: словарь с необходимыми для подсчета статистик данными.
    :type features: dict
    :param output_folder: папка, в которую пойдут выходные файлы.
    :type output_folder: str
    :return: словарь, содержащий общую статистику.
    :rtype: dict
    """
    features_type = {}
    for feature in features.keys():
        if features[feature]:
            features_type[feature] = DEPENDENCIES[feature]["return_type"]()

    for chat in parsed_chats:
        analysed_chat = Chat_stat(features, chat, time_gap)

        for feature in features.keys():
            if features[feature]:
                DEPENDENCIES[feature]["return_func"](features_type[feature],
                                                 getattr(analysed_chat, feature), chat.id)

    ret_stats = {}
    for feature in features.keys():
        if features[feature]:
            ret_stats[feature] = features_type[feature]

    return [ret_stats, parsed_chats, time_gap]
