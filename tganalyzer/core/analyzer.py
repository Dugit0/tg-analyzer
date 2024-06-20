"""Создает статистику по сообщениям."""
import bisect
import matplotlib.pyplot as plt
from collections import defaultdict


# Функции подсчета

def counter_symbols(update, message, feat_meaning):
    update[message.author] += len(message.text)


# Функции подготовки вывода

def return_symbols(update, chat_data, id):
    update[id] = chat_data


# Константы

DEPENDENCIES = {"symbols_per_person": {"class_type": defaultdict,
                                       "class_func": counter_symbols,
                                       "return_type": dict,
                                       "return_func": return_symbols
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
                setattr(self, feature, DEPENDENCIES[feature]["class_type"](int))

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

def start_analyses(parsed_chats, chat_ids, time_gap, 
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
        if chat.id not in chat_ids:
            continue
        analysed_chat = Chat_stat(features, chat, time_gap)
        
        for feature in features.keys():
            if features[feature]:
                #print(getattr(analysed_chat, feature))
                #print(DEPENDENCIES[feature]["class_type"])
                DEPENDENCIES[feature]["return_func"](features_type[feature],
                                                 getattr(analysed_chat, feature), chat.id)

    ret_stats = {}
    for feature in features.keys():
        if features[feature]:
            ret_stats[feature] = features_type[feature]

    return ret_stats
