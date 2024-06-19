"""Создает статистику по сообщениям.

Список доступного анализа (запросы передаются анализатору через features)
"top_num_symbol_quantity": подсчитывает количество использованных значимых
символов в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_word_quantity": подсчитывает количество использованных слов
в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_message_quantity": подсчитывает количество сообщений
в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"proc_symbols": создает круговую диаграмму с количеством символов в чатах
- False на входе если не использовать
"proc_words": создает круговую диаграмму с количеством слов в чатах
- False на входе если не использовать
"proc_messages": создает круговую диаграмму с количеством сообщений в чатах
- False на входе если не использовать
"symbols_summary": создает столбчатую диаграмму с количеством символов в чатах
- False на входе если не использовать
"words_summary": создает столбчатую диаграмму с количеством слов в чатах
- False на входе если не использовать
"messages_summary": создает столбчатую диаграмму с количеством сообщений
в чатах
- False на входе если не использовать
"symbols_per_day": создает графики с данными по отправке символов в день
- False на входе если не использовать
"words_per_day": создает графики с данными по отправке слов в день
- False на входе если не использовать
"messages_per_day": создает графики с данными по отправке сообщений в день
- False на входе если не использовать
"symbols_quantity_each_person": подсчитывает количество отправленных символов
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с
ключами - логинами пользователей, а значениями - количеством символов в чате
"words_quantity_each_person": подсчитывает количество отправленных слов
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с
ключами - логинами пользователей, а значениями - количеством слов в чате
"messages_quantity_each_person": подсчитывает количество отправленных сообщений
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с
ключами - логинами пользователей, а значениями - количеством сообщений в чате
"top_num_gs_quantity": подсчитывает количество голосовых сообщений
в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_gs_length": подсчитывает суммарную длительность голосовых сообщений
в чатах и возвращает топ по самым длинным голосовым сообщениям
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"proc_gs": создает графики для чатов с данными по полученным и отправленным
голосовым сообщениям
- получает на вход логин пользователя-отправителя (None если не использовать)
"top_num_gs_in_every_chat": создает для каждого чата отдельно топы из
заданного количества по длительности голосовых сообщений
- получает на вход число, сколько мест в топах (0 если не использовать)
- возвращаемым значением является словарь, где ключами являются id чатов, а
значениями являются убывающие массивы пар вида
[имя отправителя, длина голосового сообщения]
"gs_quantity_each_person": подсчитывает количество голосовых сообщений
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с ключами -
логинами пользователей, а значениями - количеством голосовых сообщений в чате
"top_num_circ_quantity": подсчитывает количество видео сообщений
в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_circ_length": подсчитывает суммарную длительность видео сообщений
в чатах и возвращает топ по самым длинным видео сообщениям
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"proc_circ": создает графики для чатов с данными по полученным и отправленным
видео сообщениям
- получает на вход логин пользователя-отправителя (None если не использовать)
"top_num_circ_in_every_chat": создает для каждого чата отдельно топы из
заданного количества по длительности видео сообщений
- получает на вход число, сколько мест в топах (0 если не использовать)
- возвращаемым значением является словарь, где ключами являются id чатов, а
значениями являются убывающие массивы пар вида
[имя отправителя, длина видео сообщения]
"circs_quantity_each_person": подсчитывает количество видео сообщений
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с ключами -
логинами пользователей, а значениями - количеством видео сообщений в чате
"top_num_ph_call_quantity": подсчитывает количество личных звонков
в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_ph_call_length": подсчитывает суммарную длительность личных звонков
в чатах и возвращает топ по самым длинным личным звонкам
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"proc_ph_call": создает графики для чатов с данными по принятым и начатым
личным звонкам
- получает на вход логин пользователя-отправителя (None если не использовать)
"top_num_ph_call_in_every_chat": создает для каждого чата отдельно топы из
заданного количества по длительности личных звонков
- получает на вход число, сколько мест в топах (0 если не использовать)
- возвращаемым значением является словарь, где ключами являются id чатов, а
значениями являются убывающие массивы пар вида
[имя отправителя, длина личного звонка]
"ph_calls_quantity_each_person": подсчитывает количество личных звонков
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с ключами -
логинами пользователей, а значениями - количеством личных звонков в чате
"top_num_gr_call_quantity": подсчитывает количество групповых звонков
в чатах и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_gr_call_length": подсчитывает суммарную длительность групповых звонков
в чатах и возвращает топ по самым длинным групповым звонкам
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"proc_gr_call": создает графики для чатов с данными по принятым и начатым
групповым звонкам
- получает на вход логин пользователя-отправителя (None если не использовать)
"favourite_sticker": создает топ использованых стикеров-эмоджи по всем чатам
заданного пользователя-отправителя
- получает на входе пару [логин отправителя, число мест в топе]
(None если не использовать)
- возвращаемым значением является массив из заданного количества элементов
пар вида [стикер-эмоджи, количество использований]
"top_num_photo_quantity": подсчитывает количество фотографий в чатах
и возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"photos_summary": создает столбчатую диаграмму с количеством фотографий
в чатах
- False на входе если не использовать
"photos_quantity_each_person": подсчитывает количество отправленных фотографий
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с ключами -
логинами пользователей, а значениями - количеством фотографий в чате
"top_num_video_quantity": подсчитывает количество видео в чатах и
возвращает топ по большему количеству использования
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"top_num_video_length": подсчитывает суммарную длительность видео файлов
в чатах и возвращает топ по самым длинным видео файлам
- получает на вход число, сколько мест в топе (0 если не использовать)
- возвращаемым значением является убывающий массив пар [id чата, значение]
"videos_summary": создает столбчатую диаграмму с количеством видео
в чатах
- False на входе если не использовать
"videos_quantity_each_person": подсчитывает количество отправленных видео
отдельно для каждого пользователя
- False на входе если не использовать
- словарь на выходе, где ключи - id чатов, значения - словари с ключами -
логинами пользователей, а значениями - количеством видео в чате
"""
import bisect
import matplotlib.pyplot as plt


# Вспомогательные функции

def quan_counter(update, aut, num):
    """Помогает составлять словари в классе Chat_stat.
    
    Функция меняет значение в словаре update по ключу aut на значение num.
    :param update: изменяемый словарь.
    :type update: dict
    :param aut: ключ.
    :type aut: str or int
    :param num: значение изменения.
    :type num: int
    """

    if aut not in update.keys():
        update[aut] = 0
    update[aut] += num


def top_counter(update, aut, dur, top=3):
    """Помогает составлять топы по длительности в чате.
    
    Создает и дополняет массив из top элементов, включающий в себя
    пары (ключ, значение), значения которых входят в топ top элементов 
    по величине.
    :param update: массив, который будет содержать в себе наилучшие величины.
    :type update: array
    :param aut: ключ.
    :type aut: str or int
    :param dur: значение (длительность и тп).
    :type dur: int
    :param top: количество элементов в топе.
    :type top: int
    """

    if len(update) < top:
        update.append([aut, dur])
        update.sort(key=lambda x : x[1],
                    reverse=True)
    else:
        aut_dur = [aut, dur]
        for j in range(top):
            if aut_dur[1] > update[j][1]:
                update[j], aut_dur = aut_dur, update[j]


def top_counter_chats(update, analysed, author, top=3):
    """Помогает составлять топы по размеру сообщений по чатово.
    
    Создает и обновляет массив из top элементов, представляющих собою
    пары (ключ, значение), значениями же являются сумма значений словаря
    analysed. Необходима для общей статистики по чатово.
    :param update: массив с топом.
    :type update: array
    :param analysed: словарь значений.
    :type analysed: dict
    :param author: ключ в паре (id чата и тп).
    :type author: str or int
    :param top: количество элементов в топе.
    :type top: int
    """

    summa = sum(analysed.values())
    top_counter(update, author, summa, top)


def sticker_append(update, chat_stickers):
    """Дополняет информацию о стикерах в общий массив.
    
    Собирают информацию о количестве стикеров с каждого чата и дополняет
    массив с общей инфой по всем чатам информацией с нового чата
    :param update: изменяемый массив с общей информацией о стикерах.
    :type update: array
    :param chat_stickers: словарь с количеством стикеров нового чата.
    :type chat_stickers: dict
    """

    for emo in chat_stickers.keys():
        if emo in update.keys():
            update[emo] += chat_stickers[emo]
        else:
            update[emo] = chat_stickers[emo]


def top_num_stickers_finder(update, stickers, top=3):
    """Находит top наиболее используемых стикеров.
    
    Получает на вход словарь всех появляющихся стикеров по всем чатам
    и находит top наиболее используемых.
    :param update: изменяемый массив.
    :type update: array
    :param stickers: словарь с информацией о появлениях стикеров.
    :type stickers: dict
    :param top: количество элементов в топе.
    :type top: int
    """

    for emo in stickers.keys():
        top_counter(update, emo, stickers[emo], top)

# дизайны всех графиков требуют обговора, Дима
def pie_create(output_path, all_chats, option):
    """Функция по созданию круговой диаграммы.
    
    Создает круговую диаграмму на основе информации all_chats и сохраняет
    полученный график в папку output_path с option в названии.
    :param output_path: выходная папка.
    :type output_path: str
    :param all_chats: словарь с информацией для диаграммы.
    :type all_chats: dict
    :param option: необходимая часть для названия (symbol, word и тп).
    :type option: str
    """

    y = all_chats.keys()
    x = all_chats.values()

    plt.pie(x, labels=y)
    plt.savefig(output_path + f'proc_{option}.png')
    plt.close()


def bar_create(output_path, all_chats, option):
    """Функция по созданию столбчатой диаграммы.
    
    Создает столбчатую диаграмму на основе информации all_chats и сохраняет
    полученный график в папку output_path с option в названии.
    :param output_path: выходная папка.
    :type output_path: str
    :param all_chats: словарь с информацией для диаграммы.
    :type all_chats: dict
    :param option: необходимая часть для названия (symbol, word и тп).
    :type option: str
    """

    x = all_chats.keys()
    y = all_chats.values()

    plt.bar(x, y)
    plt.savefig(output_path + f'summary_{option}.png')
    plt.close()


def hist_create(output_path, all_chats, option):   # Dmitry help with this
    """Функция по созданию хиста.
    
    Ведется работа.
    """

    y = all_chats[0]
    x_send = all_chats[1]
    x_recv = all_chats[2]

    plt.hist([x_send, x_recv], stacked=True, label=y)   # не разобрался tbh
    plt.legend()
    plt.savefig(output_path + f'proc_{option}.png')
    plt.close()


def plot_create(output_path, all_chats, option):
    """Функция по созданию линейных графиков.
    
    Создает линейные графики на основе информации all_chats и сохраняет
    полученный рисунок в папку output_path с option в названии.
    :param output_path: выходная папка.
    :type output_path: str
    :param all_chats: словарь с информацией для рисунка.
    :type all_chats: dict
    :param option: необходимая часть для названия (symbol, word и тп).
    :type option: str
    """

    for chat in all_chats.keys():
        analysed = all_chats[chat]
        name = analysed[0]
        stats = analysed[1]
        y, x = stats.keys(), stats.values()
        plt.plot(x, y, label=name)

    plt.legend()
    plt.savefig(output_path + f'{option}_per_day.png')
    plt.close()


# Основные классы

class Chat_stat():
    """Класс, поля которого представляют собой статистику по чату.

    Поля зависят от выставленных флагов в features.
    :param symbol_sum: количество символов в чате.
    :type symbol_sum: dict
    :param symbol_days: количество символов в день.
    :type symbol_days: dict
    :param symbol_people: количесто символов у каждого пользователя
    :type symbol_people: dict
    :param word_sum: количество слов в чате.
    :type word_sum: dict
    :param word_days: количество слов в день.
    :type word_days: dict
    :param word_people: количесто слов у каждого пользователя
    :type word_people: dict
    :param message_sum: количество сообщений в чате.
    :type message_sum: dict
    :param message_days: количество сообщений в день.
    :type message_days: dict
    :param message_people: количесто сообщений у каждого пользователя
    :type message_people: dict
    :param gs_sum: количесвто голосовых сообщений в чате.
    :type gs_sum: dict
    :param gs_len: суммарная длина гсок.
    :type gs_len: dict
    :param top_long_gs: самые длинные голосовые сообщения по чату.
    :type top_long_gs: array
    :param gs_people: количесто голосовых сообщений у каждого пользователя
    :type gs_people: dict
    :param circ_sum: количество видео сообщений в чате.
    :type circ_sum: dict
    :param circ_len: суммарная длина кружков.
    :type circ_len: dict
    :param top_long_circ: саммые длинные кружки по чату.
    :type top_long_circ: array
    :param circ_people: количесто видео сообщений у каждого пользователя
    :type circ_people: dict
    :param ph_call_sum: количество личных звонков в чате.
    :type ph_call_sum: dict
    :param ph_call_len: суммарная длина личных звонков по чату.
    :type ph_call_len: dict
    :param top_long_ph_call: самые длинные звонки по чату.
    :type top_long_ph_call: array
    :param ph_call_people: количесто личных звонков у каждого пользователя
    :type ph_call_people: dict
    :param gr_call_sum: количество групповых звонков в чате.
    :type gr_call_sum: dict
    :param gr_call_len: суммарная длина групповых звонков по чату.
    :type gr_call_len: dict
    :param fav_stick: количество поялений стикеров у login по чату.
    :type fav_stick: dict
    :param photo_sum: количество фото в чате.
    :type photo_sum: dict
    :param photo_people: количесто фотографий у каждого пользователя
    :type photo_people: dict
    :param video_sum: количество видео файлов в чате.
    :type video_sum: dict
    :param video_len: суммарная длина видео файлов.
    :type video_len: dict
    :param video_people: количесто видео файлов у каждого пользователя
    :type video_people: dict
    """

    def __init__(self, features, chat, time_gap):
        """Инициализирует объект класса, подсчитывая статистику по чату.

        :param features: какие статистики надо подсчитать.
        :type features: dict
        :param chat: анализируемый чат.
        :type chat: creator.Chat
        :param time_gap: временной промежуток рассматриваемых сообщений.
        :type time_gap: array (начальная дата и конечная)
        """

        if features["top_num_symbol_quantity"] > 0 or \
                features["proc_symbols"] or \
                features["symbols_summary"]:
            self.symbol_sum = {}
        if features["symbols_per_day"]:
            self.symbol_days = {}
        if features["symbols_quantity_each_person"]:
            self.symbol_people = {}

        if features["top_num_word_quantity"] > 0 or \
                features["proc_words"] or \
                features["words_summary"]:
            self.word_sum = {}
        if features["words_per_day"]:
            self.word_days = {}
        if features["words_quantity_each_person"]:
            self.word_people = {}

        if features["top_num_message_quantity"] > 0 or \
                features["proc_messages"] or \
                features["messages_summary"]:
            self.message_sum = {}
        if features["messages_per_day"]:
            self.message_days = {}
        if features["messages_quantity_each_person"]:
            self.message_people = {}

        if features["top_num_gs_quantity"] > 0:
            self.gs_sum = {}
        if features["top_num_gs_length"] > 0 or \
                features["proc_gs"] is not None:
            self.gs_len = {}
        if features["top_num_gs_in_every_chat"] > 0:
            self.top_long_gs = []
        if features["gs_quantity_each_person"]:
            self.gs_people = {}

        if features["top_num_circ_quantity"] > 0:
            self.circ_sum = {}
        if features["top_num_circ_length"] > 0 or \
                features["proc_circ"] is not None:
            self.circ_len = {}
        if features["top_num_circ_in_every_chat"] > 0:
            self.top_long_circ = []
        if features["circs_quantity_each_person"]:
            self.circ_people = {}

        if features["top_num_ph_call_quantity"] > 0:
            self.ph_call_sum = {}
        if features["top_num_ph_call_length"] > 0 or \
                features["proc_ph_call"] is not None:
            self.ph_call_len = {}
        if features["top_num_ph_call_in_every_chat"] > 0:
            self.top_long_ph_call = []
        if features["ph_calls_quantity_each_person"]:
            self.ph_call_people = {}

        if features["top_num_gr_call_quantity"] > 0:
            self.gr_call_sum = {}
        if features["top_num_gr_call_length"] > 0 or \
                features["proc_gr_call"] is not None:
            self.gr_call_len = {}

        if features["favourite_sticker"] is not None:
            self.fav_stick = {}

        if features["top_num_photo_quantity"] > 0 or \
                features["photos_summary"]:
            self.photo_sum = {}
        if features["photos_quantity_each_person"]:
            self.photo_people = {}

        if features["top_num_video_quantity"] > 0 or \
                features["videos_summary"]:
            self.video_sum = {}
        if features["top_num_video_length"] > 0:
            self.video_len = {}
        if features["videos_quantity_each_person"]:
            self.video_people = {}

        start_mes = bisect.bisect_left(chat.messages, time_gap[0],
                                        key= lambda x : x.send_time)
        end_mes = bisect.bisect_right(chat.messages, time_gap[1],
                                      key= lambda x : x.send_time)
        for i in range(start_mes, end_mes):
            message = chat.messages[i]
            aut = message.author

            # symbols
            if features["top_num_symbol_quantity"] > 0 or \
                    features["proc_symbols"] or \
                    features["symbols_summary"]:   #only useful symbols
                if type(message.text) is list:
                    tmp_str = ''
                    for elem in message.text:
                        if type(elem) is str:
                            tmp_str += elem.replace(' ', '')
                else:
                    tmp_str = message.text.replace(' ', '')
                quan_counter(self.symbol_sum, aut, len(tmp_str))
            if features["symbols_per_day"]:
                if type(message.text) is list:
                    tmp_str = ''
                    for elem in message.text:
                        if type(elem) is str:
                            tmp_str += elem.replace(' ', '')
                else:
                    tmp_str = message.text.replace(' ', '')
                date = message.send_time.date()
                quan_counter(self.symbol_days, date, len(tmp_str))
            if features["symbols_quantity_each_person"]:
                if type(message.text) is list:
                    tmp_str = ''
                    for elem in message.text:
                        if type(elem) is str:
                            tmp_str += elem.replace(' ', '')
                else:
                    tmp_str = message.text.replace(' ', '')
                quan_counter(self.symbol_people, aut, len(tmp_str))

            # words
            if features["top_num_word_quantity"] > 0 or \
                    features["proc_words"] or \
                    features["words_summary"]:
                if type(message.text) is list:
                    tmp_str = ''
                    for elem in message.text:
                        if type(elem) is str:
                            tmp_str += elem + " "
                else:
                    tmp_str = message.text
                quan_counter(self.word_sum, aut, len(tmp_str.split()))
            if features["words_per_day"]:
                if type(message.text) is list:
                    tmp_str = ''
                    for elem in message.text:
                        if type(elem) is str:
                            tmp_str += elem + " "
                else:
                    tmp_str = message.text
                date = message.send_time.date()
                quan_counter(self.word_days, date, len(tmp_str.split()))
            if features["words_quantity_each_person"]:
                if type(message.text) is list:
                    tmp_str = ''
                    for elem in message.text:
                        if type(elem) is str:
                            tmp_str += elem + " "
                else:
                    tmp_str = message.text
                quan_counter(self.word_people, aut, len(tmp_str.split()))

            # messages
            if features["top_num_message_quantity"] > 0 or \
                    features["proc_messages"] or \
                    features["messages_summary"]:
                quan_counter(self.message_sum, aut, 1)
            if features["messages_per_day"]:
                date = message.send_time.date()
                quan_counter(self.message_days, date, 1)
            if features["messages_quantity_each_person"]:
                quan_counter(self.message_people, aut, 1)

            # single calls
            if features["top_num_ph_call_quantity"] > 0 and \
                    message.type == "single_call":
                quan_counter(self.ph_call_sum, aut, 1)
            if (features["top_num_ph_call_length"] > 0 or \
                    features["proc_ph_call"] is not None) and \
                    message.type == "single_call":
                dur = message.duration
                quan_counter(self.ph_call_len, aut, dur)
            if features["top_num_ph_call_in_every_chat"] > 0 and \
                    message.type == "single_call":
                dur = message.duration
                top = features["top_num_ph_call_in_every_chat"]
                top_counter(self.top_long_ph_call, aut, dur, top)
            if features["ph_calls_quantity_each_person"] and \
                    message.type == "single_call":
                quan_counter(self.ph_call_people, aut, 1)

            # group calls
            if features["top_num_gr_call_quantity"] > 0 and \
                    message.type == "group_call":
                quan_counter(self.gr_call_sum, aut, 1)
            if (features["top_num_gr_call_length"] > 0 or \
                    features["proc_gr_call"] is not None) and \
                    message.type == "group_call":
                dur = message.duration
                quan_counter(self.gr_call_len, aut, dur)

            # gs
            if features["top_num_gs_quantity"] > 0 and \
                    message.type == "voice_message":
                quan_counter(self.gs_sum, aut, 1)
            if (features["top_num_gs_length"] > 0 or \
                    features["proc_gs"] is not None) and \
                    message.type == "voice_message":
                dur = message.duration
                quan_counter(self.gs_len, aut, dur)
            if features["top_num_gs_in_every_chat"] > 0 and \
                    message.type == "voice_message":
                dur = message.duration
                top = features["top_num_gs_in_every_chat"]
                top_counter(self.top_long_gs, aut, dur, top)
            if features["gs_quantity_each_person"] and \
                    message.type == "voice_message":
                quan_counter(self.gs_people, aut, 1)

            # circles
            if features["top_num_circ_quantity"] > 0 and \
                    message.type == "video_message":
                quan_counter(self.circ_sum, aut, 1)
            if (features["top_num_circ_length"] > 0 or \
                    features["proc_circ"] is not None) and \
                    message.type == "video_message":
                dur = message.duration
                quan_counter(self.circ_len, aut, dur)
            if features["top_num_circ_in_every_chat"] > 0 and \
                    message.type == "video_message":
                dur = message.duration
                top = features["top_num_circ_in_every_chat"]
                top_counter(self.top_long_circ, aut, dur, top)
            if features["circs_quantity_each_person"] and \
                    message.type == "video_message":
                quan_counter(self.circ_people, aut, 1)

            # stickers
            if features["favourite_sticker"] is not None and \
                    message.type == "sticker" and \
                    message.sticker_emoji is not None and \
                    aut == features["favourite_sticker"][0]:
                emo = message.sticker_emoji
                quan_counter(self.fav_stick, emo, 1)

            # photos
            if (features["top_num_photo_quantity"] > 0 or \
                    features["photos_summary"]) and \
                    message.type == "photo":
                quan_counter(self.photo_sum, aut, 1)
            if features["photos_quantity_each_person"] and \
                    message.type == "photo":
                quan_counter(self.photo_people, aut, 1)

            # videos
            if (features["top_num_video_quantity"] or \
                    features["videos_summary"]) and \
                    message.type == "video_file":
                quan_counter(self.video_sum, aut, 1)
            if features["top_num_video_length"] > 0 and \
                    message.type == "video_file":
                dur = message.duration
                quan_counter(self.video_len, aut, dur)
            if features["videos_quantity_each_person"] and \
                    message.type == "video_file":
                quan_counter(self.video_people, aut, 1)


# Основные функции

def start_analyses(parsed_chats, chat_ids, time_gap, 
                   features, output_folder):
    """Основная функция для анализа.

    :param parsed_chats: массив объектов класса Chat из creator.
    :type parsed_chats: array
    :param chat_ids: id чатов, которые будут анализироваться.
    :type chat_ids: array
    :param time_gap: границы временного интервала.
    :type time_gap: array
    :param features: словарь с необходимыми для подсчета статистик данными.
    :type features: dict
    :param output_folder: папка, в которую пойдут выходные файлы.
    :type output_folder: str
    :return: словарь, содержащий общую статистику.
    :rtype: dict
    """

    if features["top_num_symbol_quantity"] > 0:
        top_symbols = []
    if features["top_num_word_quantity"] > 0:
        top_words = []
    if features["top_num_message_quantity"] > 0:
        top_messages = []

    if features["proc_symbols"]:
        quan_symbol_chats = {}
    if features["proc_words"]:
        quan_word_chats = {}
    if features["proc_messages"]:
        quan_message_chats = {}

    if features["symbols_summary"]:
        symbols_summary = {}
    if features["words_summary"]:
        words_summary = {}
    if features["messages_summary"]:
        messages_summary = {}

    if features["symbols_per_day"]:
        symbols_per_day = {}
    if features["words_per_day"]:
        words_per_day = {}
    if features["messages_per_day"]:
        messages_per_day = {}

    if features["symbols_quantity_each_person"]:
        symbols_per_person = {}
    if features["words_quantity_each_person"]:
        words_per_person = {}
    if features["messages_quantity_each_person"]:
        messages_per_person = {}

    if features["top_num_gs_quantity"] > 0:
        top_gs_quan = []
    if features["top_num_gs_length"] > 0:
        top_gs_len = []
    if features["proc_gs"] is not None:
        len_gs_chats = [[], [], []]   # all chats
    if features["top_num_gs_in_every_chat"] > 0:
        len_gs_in_chat = {}   # top long gs in chat
    if features["gs_quantity_each_person"]:
        gs_per_person = {}

    if features["top_num_circ_quantity"] > 0:
        top_circ_quan = []
    if features["top_num_circ_length"] > 0:
        top_circ_len = []
    if features["proc_circ"] is not None:
        len_circ_chats = [[], [], []]   # all chats
    if features["top_num_circ_in_every_chat"] > 0:
        len_circ_in_chat = {}   # top long circ in chat
    if features["circs_quantity_each_person"]:
        circs_per_person = {}

    if features["top_num_ph_call_quantity"] > 0:
        top_ph_call_quan = []
    if features["top_num_ph_call_length"] > 0:
        top_ph_call_len = []
    if features["proc_ph_call"] is not None:
        len_ph_call_chats = [[], [], []]   # all chats
    if features["top_num_ph_call_in_every_chat"] > 0:
        len_ph_call_in_chat = {}   # top long ph_call in chat
    if features["ph_calls_quantity_each_person"]:
        ph_calls_per_person = {}

    if features["top_num_gr_call_quantity"] > 0:
        top_gr_call_quan = []
    if features["top_num_gr_call_length"] > 0:
        top_gr_call_len = []
    if features["proc_gr_call"] is not None:
        len_gr_call_chats = [[], [], []]   # all chats

    if features["favourite_sticker"] is not None:
        top_fav_stickers = {}

    if features["top_num_photo_quantity"] > 0:
        top_photos = []
    if features["photos_summary"]:
        photos_summary = {}
    if features["photos_quantity_each_person"]:
        photos_per_person = {}

    if features["top_num_video_quantity"] > 0:
        top_videos = []
    if features["top_num_video_length"] > 0:
        top_video_len = []
    if features["videos_summary"]:
        videos_summary = {}
    if features["videos_quantity_each_person"]:
        videos_per_person = {}

    for chat in parsed_chats:
        if chat.id in chat_ids:
            analysed_chat = Chat_stat(features, chat, time_gap)

            if features["top_num_symbol_quantity"] > 0:
                analysed = analysed_chat.symbol_sum
                top = features["top_num_symbol_quantity"]
                top_counter_chats(top_symbols, analysed, chat.id, top)
            if features["top_num_word_quantity"] > 0:
                analysed = analysed_chat.word_sum
                top = features["top_num_word_quantity"]
                top_counter_chats(top_words, analysed, chat.id, top)
            if features["top_num_message_quantity"] > 0:
                analysed = analysed_chat.message_sum
                top = features["top_num_message_quantity"]
                top_counter_chats(top_messages, analysed, chat.id, top)

            if features["proc_symbols"]:
                summa = sum(analysed_chat.symbol_sum.values())
                quan_symbol_chats[chat.name] = summa
            if features["proc_words"]:
                summa = sum(analysed_chat.word_sum.values())
                quan_word_chats[chat.name] = summa
            if features["proc_messages"]:
                summa = sum(analysed_chat.message_sum.values())
                quan_message_chats[chat.name] = summa

            if features["symbols_summary"]:
                summa = sum(analysed_chat.symbol_sum.values())
                symbols_summary[chat.name] = summa
            if features["words_summary"]:
                summa = sum(analysed_chat.word_sum.values())
                words_summary[chat.name] = summa
            if features["messages_summary"]:
                summa = sum(analysed_chat.message_sum.values())
                messages_summary[chat.name] = summa

            if features["symbols_per_day"]:
                analysed = analysed_chat.symbol_days
                symbols_per_day[chat.id] = [chat.name, analysed]
            if features["words_per_day"]:
                analysed = analysed_chat.word_days
                words_per_day[chat.id] = [chat.name, analysed]
            if features["messages_per_day"]:
                analysed = analysed_chat.message_days
                messages_per_day[chat.id] = [chat.name, analysed]

            if features["symbols_quantity_each_person"]:
                analysed = analysed_chat.symbol_people
                symbols_per_person[chat.id] = analysed
            if features["words_quantity_each_person"]:
                analysed = analysed_chat.word_people
                words_per_person[chat.id] = analysed
            if features["messages_quantity_each_person"]:
                analysed = analysed_chat.message_people
                messages_per_person[chat.id] = analysed

            # gs
            if features["top_num_gs_quantity"] > 0:
                analysed = analysed_chat.gs_sum
                top = features["top_num_gs_quantity"]
                top_counter_chats(top_gs_quan, analysed, chat.id, top)
            if features["top_num_gs_length"] > 0:
                analysed = analysed_chat.gs_len
                top = features["top_num_gs_length"]
                top_counter_chats(top_gs_len, analysed, chat.id, top)
            if features["proc_gs"] is not None:
                len_gs_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.gs_len.keys():
                    summa = analysed_chat.gs_len[aut]
                    if aut == features["proc_gs"]:
                        send += summa
                    else:
                        recv += summa
                len_gs_chats[1].append(send)
                len_gs_chats[2].append(recv)
            if features["top_num_gs_in_every_chat"] > 0:
                len_gs_in_chat[chat.id] = [chat.name, analysed_chat.top_long_gs]
            if features["gs_quantity_each_person"]:
                analysed = analysed_chat.gs_people
                gs_per_person[chat.id] = analysed

            # circles
            if features["top_num_circ_quantity"] > 0:
                analysed = analysed_chat.circ_sum
                top = features["top_num_circ_quantity"]
                top_counter_chats(top_circ_quan, analysed, chat.id, top)
            if features["top_num_circ_length"] > 0:
                analysed = analysed_chat.circ_len
                top = features["top_num_circ_length"]
                top_counter_chats(top_circ_len, analysed, chat.id, top)
            if features["proc_circ"] is not None:
                len_circ_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.circ_len.keys():
                    summa = analysed_chat.circ_len[aut]
                    if aut == features["proc_circ"]:
                        send += summa
                    else:
                        recv += summa
                len_circ_chats[1].append(send)
                len_circ_chats[2].append(recv)
            if features["top_num_circ_in_every_chat"] > 0:
                len_circ_in_chat[chat.id] = [chat.name, analysed_chat.top_long_circ]
            if features["circs_quantity_each_person"]:
                analysed = analysed_chat.circ_people
                circs_per_person[chat.id] = analysed

            # single calls
            if features["top_num_ph_call_quantity"] > 0:
                analysed = analysed_chat.ph_call_sum
                top = features["top_num_ph_call_quantity"]
                top_counter_chats(top_ph_call_quan, analysed, chat.id, top)
            if features["top_num_ph_call_length"] > 0:
                analysed = analysed_chat.ph_call_len
                top = features["top_num_ph_call_length"]
                top_counter_chats(top_ph_call_len, analysed, chat.id, top)
            if features["proc_ph_call"] is not None:
                len_ph_call_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.ph_call_len.keys():
                    summa = analysed_chat.ph_call_len[aut]
                    if aut == features["proc_ph_call"]:
                        send += summa
                    else:
                        recv += summa
                len_ph_call_chats[1].append(send)
                len_ph_call_chats[2].append(recv)
            if features["top_num_ph_call_in_every_chat"] > 0:
                len_ph_call_in_chat[chat.id] = [chat.name, analysed_chat.top_long_ph_call]
            if features["ph_calls_quantity_each_person"]:
                analysed = analysed_chat.ph_call_people
                ph_calls_per_person[chat.id] = analysed

            # group calls
            if features["top_num_gr_call_quantity"] > 0:
                analysed = analysed_chat.gr_call_sum
                top = features["top_num_gr_call_quantity"]
                top_counter_chats(top_gr_call_quan, analysed, chat.id, top)
            if features["top_num_gr_call_length"] > 0:
                analysed = analysed_chat.gr_call_len
                top = features["top_num_gr_call_length"] 
                top_counter_chats(top_gr_call_len, analysed, chat.id, top)
            if features["proc_gr_call"] is not None:
                len_gr_call_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.gr_call_len.keys():
                    summa = analysed_chat.gr_call_len[aut]
                    if aut == features["proc_gr_call"]:
                        send += summa
                    else:
                        recv += summa
                len_gr_call_chats[1].append(send)
                len_gr_call_chats[2].append(recv)

            # stickers
            if features["favourite_sticker"] is not None:
                sticker_append(top_fav_stickers, analysed_chat.fav_stick)

            # photos
            if features["top_num_photo_quantity"] > 0:
                analysed = analysed_chat.photo_sum
                top = features["top_num_photo_quantity"]
                top_counter_chats(top_photos, analysed, chat.id, top)
            if features["photos_summary"]:
                summa = sum(analysed_chat.photo_sum.values())
                photos_summary[chat.name] = summa
            if features["photos_quantity_each_person"]:
                analysed = analysed_chat.photo_people
                photos_per_person[chat.id] = analysed

            # videos
            if features["top_num_video_quantity"] > 0:
                analysed = analysed_chat.video_sum
                top = features["top_num_video_quantity"]
                top_counter_chats(top_videos, analysed, chat.id, top)
            if features["top_num_video_length"] > 0:
                analysed = analysed_chat.video_len
                top = features["top_num_video_length"]
                top_counter_chats(top_video_len, analysed, chat.id, top)
            if features["videos_summary"]:
                summa = sum(analysed_chat.video_sum.values())
                videos_summary[chat.name] = summa
            if features["videos_quantity_each_person"]:
                analysed = analysed_chat.video_people
                videos_per_person[chat.id] = analysed
        else:
            continue

    ret_stats = {}
    if features["top_num_symbol_quantity"] > 0:
        ret_stats["top_num_symbol_quantity"] = top_symbols
    if features["top_num_word_quantity"] > 0:
        ret_stats["top_num_word_quantity"] = top_words
    if features["top_num_message_quantity"] > 0:
        ret_stats["top_num_message_quantity"] = top_messages

    if features["proc_symbols"]:
        pie_create(output_folder, quan_symbol_chats, "symbol")
    if features["proc_words"]:
        pie_create(output_folder, quan_word_chats, "word")
    if features["proc_messages"]:
        pie_create(output_folder, quan_message_chats, "message")

    if features["symbols_summary"]:
        bar_create(output_folder, symbols_summary, "symbol")
    if features["words_summary"]:
        bar_create(output_folder, words_summary, "word")
    if features["messages_summary"]:
        bar_create(output_folder, messages_summary, "message")

    if features["symbols_per_day"]:
        plot_create(output_folder, symbols_per_day, "symbol")
    if features["words_per_day"]:
        plot_create(output_folder, words_per_day, "word")
    if features["messages_per_day"]:
        plot_create(output_folder, messages_per_day, "message")

    if features["symbols_quantity_each_person"]:
        ret_stats["symbols_quantity_each_person"] = symbols_per_person
    if features["words_quantity_each_person"]:
        ret_stats["words_quantity_each_person"] = words_per_person
    if features["messages_quantity_each_person"]:
        ret_stats["messages_quantity_each_person"] = messages_per_person

    if features["top_num_gs_quantity"] > 0:
        ret_stats["top_num_gs_quantity"] = top_gs_quan
    if features["top_num_gs_length"] > 0:
        ret_stats["top_num_gs_length"] = top_gs_len
    if features["proc_gs"] is not None:
        hist_create(output_folder, len_gs_chats, "gs")
    if features["top_num_gs_in_every_chat"] > 0:
        ret_stats["top_num_gs_in_every_chat"] = len_gs_in_chat
    if features["gs_quantity_each_person"]:
        ret_stats["gs_quantity_each_person"] = gs_per_person

    if features["top_num_circ_quantity"] > 0:
        ret_stats["top_num_circ_quantity"] = top_circ_quan
    if features["top_num_circ_length"] > 0:
        ret_stats["top_num_circ_length"] = top_circ_len
    if features["proc_circ"] is not None:
        hist_create(output_folder, len_circ_chats, "circ")
    if features["top_num_circ_in_every_chat"] > 0:
        ret_stats["top_num_circ_in_every_chat"] = len_circ_in_chat
    if features["circs_quantity_each_person"]:
        ret_stats["circs_quantity_each_person"] = circs_per_person

    if features["top_num_ph_call_quantity"] > 0:
        ret_stats["top_num_ph_call_quantity"] = top_ph_call_quan
    if features["top_num_ph_call_length"] > 0:
        ret_stats["top_num_ph_call_length"] = top_ph_call_len
    if features["proc_ph_call"] is not None:
        hist_create(output_folder, len_ph_call_chats, "ph_call")
    if features["top_num_ph_call_in_every_chat"] > 0:
        ret_stats["top_num_ph_call_in_every_chat"] = len_ph_call_in_chat
    if features["ph_calls_quantity_each_person"]:
        ret_stats["ph_calls_quantity_each_person"] = ph_calls_per_person

    if features["top_num_gr_call_quantity"] > 0:
        ret_stats["top_num_gr_call_quantity"] = top_gr_call_quan
    if features["top_num_gr_call_length"] > 0:
        ret_stats["top_num_gr_call_length"] = top_gr_call_len
    if features["proc_gr_call"] is not None:
        hist_create(output_folder, len_gr_call_chats, "gr_call")

    if features["favourite_sticker"] is not None:
        top_num_stickers = []
        top = features["favourite_sticker"][1]
        top_num_stickers_finder(top_num_stickers, top_fav_stickers, top)
        ret_stats["favourite_sticker"] = top_num_stickers

    if features["top_num_photo_quantity"] > 0:
        ret_stats["top_num_photo_quantity"] = top_photos
    if features["photos_summary"]:
        bar_create(output_folder, photos_summary, "photo")
    if features["photos_quantity_each_person"]:
        ret_stats["photos_quantity_each_person"] = photos_per_person

    if features["top_num_video_quantity"] > 0:
        ret_stats["top_num_video_quantity"] = top_videos
    if features["top_num_video_length"] > 0:
        ret_stats["top_num_video_length"] = top_video_len
    if features["videos_summary"]:
        bar_create(output_folder, videos_summary, "video")
    if features["videos_quantity_each_person"]:
        ret_stats["videos_quantity_each_person"] = videos_per_person

    return ret_stats
