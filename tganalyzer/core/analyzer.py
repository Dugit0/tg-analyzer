"""Создает статистику по сообщениям."""
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

    sum = sum(analysed.values())
    top_counter(update, author, sum, top)


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

    y = all_chats.keys()
    x = all_chats.values()

    plt.bar(x, labels=y)
    plt.savefig(output_path + f'summary_{option}.png')


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
    plt.savefig(output_path + f'summary_{option}.png')


# Основные классы

class Chat_stat():
    """Класс, поля которого представляют собой статистику по чату.

    Поля зависят от выставленных флагов в features.
    :param symbol_sum: количество символов в чате.
    :type symbol_sum: dict
    :param symbol_days: количество символов в день.
    :type symbol_days: dict
    :param word_sum: количество слов в чате.
    :type word_sum: dict
    :param word_days: количество слов в день.
    :type word_days: dict
    :param message_sum: количество сообщений в чате.
    :type message_sum: dict
    :param message_days: количество сообщений в день.
    :type message_days: dict
    :param gs_sum: количесвто голосовых сообщений в чате.
    :type gs_sum: dict
    :param gs_len: суммарная длина гсок.
    :type gs_len: dict
    :param top_long_gs: самые длинные голосовые сообщения по чату.
    :type top_long_gs: array
    :param circ_sum: количество видео сообщений в чате.
    :type circ_sum: dict
    :param circ_len: суммарная длина кружков.
    :type circ_sum: dict
    :param top_long_circ: саммые длинные кружки по чату.
    :type top_long_circ: array
    :param ph_call_sum: количество личных звонков в чате.
    :type ph_call_sum: dict
    :param ph_call_len: суммарная длина личных звонков по чату.
    :type ph_call_len: dict
    :param top_long_ph_call: самые длинные звонки по чату.
    :type top_long_ph_call: array
    :param gr_call_sum: количество групповых звонков в чате.
    :type gr_call_sum: dict
    :param gr_call_len: суммарная длина групповых звонков по чату.
    :type gr_call_len: dict
    :param fav_stick: количество поялений стикеров у login по чату.
    :type fav_stick: dict
    :param photo_sum: количество фото в чате.
    :type photo_sum: dict
    :param video_sum: количество видео в чате.
    :type video_sum: dict
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
        if features["symbol_per_day"]:
            self.symbol_days = {}

        if features["top_num_word_quantity"] > 0 or \
                features["proc_words"] or \
                features["words_summary"]:
            self.word_sum = {}
        if features["word_per_day"]:
            self.word_days = {}

        if features["top_num_message_quantity"] > 0 or \
                features["proc_messages"] or \
                features["messages_summary"]:
            self.message_sum = {}
        if features["message_per_day"]:
            self.message_days = {}

        if features["top_num_gs_quantity"] > 0:
            self.gs_sum = {}
        if features["top_num_gs_length"] > 0 or \
                features["proc_gs"] is not None:
            self.gs_len = {}
        if features["top_num_gs_in_every_chat"] > 0:
            self.top_long_gs = []

        if features["top_num_circ_quantity"] > 0:
            self.circ_sum = {}
        if features["top_num_circ_length"] > 0 or \
                features["proc_circ"] is not None:
            self.circ_len = {}
        if features["top_num_circ_in_every_chat"] > 0:
            self.top_long_circ = []

        if features["top_num_ph_call_quantity"] > 0:
            self.ph_call_sum = {}
        if features["top_num_ph_call_length"] > 0 or \
                features["proc_ph_call"] is not None:
            self.ph_call_len = {}
        if features["top_num_ph_call_in_every_chat"] > 0:
            self.top_long_ph_call = []

        if features["top_num_gr_call_quantity"] > 0:
            self.gr_call_sum = {}
        if features["top_num_gr_call_length"] > 0 or \
                features["proc_gr_call"] is not None:
            self.gr_call_len = {}

        if features["favourite_sticker"] is not None:
            self.fav_stick = {}

        if features["photos_summary"]:
            self.photo_sum = {}

        if features["videos_summary"]:
            self.video_sum = {}

        start_mes = bisect.bisect_left(chat.messages, time_gap[0],
                                        key= lambda x : x.send_time)
        end_mes = bisect.bisect_right(chat.messages, time_gap[1],
                                      key= lambda x : x.send_time)
        for i in range(start_mes, end_mes + 1):
            message = chat.messages[i]
            aut = message.author
            if features["top_num_symbol_quantity"] > 0 or \
                    features["proc_symbols"] or \
                    features["symbols_summary"]:   #only useful symbols
                tmp_str = message.text.replace(' ', '')
                quan_counter(self.symbol_sum, aut, len(tmp_str))
            if features["symbol_per_day"]:
                tmp_str = message.text.replace(' ', '')
                quan_counter(self.symbol_days, i, len(tmp_str))

            if features["top_num_word_quantity"] > 0 or \
                    features["proc_words"] or \
                    features["words_summary"]:
                quan_counter(self.word_sum, aut, len(message.text.split()))
            if features["word_per_day"]:
                quan_counter(self.word_days, i, len(message.text.split()))

            if features["top_num_message_quantity"] > 0 or \
                    features["proc_messages"] or \
                    features["messages_summary"]:
                quan_counter(self.message_sum, aut, 1)
            if features["message_per_day"]:
                quan_counter(self.message_days, i, 1)
            
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

            if features["top_num_gr_call_quantity"] > 0 and \
                    message.type == "group_call":
                quan_counter(self.gr_call_sum, aut, 1)
            if (features["top_num_gr_call_length"] > 0 or \
                    features["proc_gr_call"] is not None) and \
                    message.type == "group_call":
                dur = message.duration
                quan_counter(self.gr_call_len, aut, dur)

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
                top_counter(self.top_long_circ, aut, dur)

            if features["favourite_sticker"] is not None and \
                    message.type == "sticker" and \
                    message.sticker_emoji is not None and \
                    aut == features["fav_stick"][0]:
                emo = message.sticker_emoji
                quan_counter(self.fav_stick, emo, 1)

            if features["photos_summary"] and \
                    message.type == "photo":
                quan_counter(self.photo_sum, aut, 1)

            if features["videos_summary"] and \
                    message.type == "video_file":
                quan_counter(self.video_sum, aut, 1)


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
        symbols_summary = 0
    if features["words_summary"]:
        words_summary = 0
    if features["messages_summary"]:
        messages_summary = 0

    if features["symbols_per_day"]:
        symbol_per_day = {}
    if features["words_per_day"]:
        word_per_day = {}
    if features["messages_per_day"]:
        message_per_day = {}

    if features["top_num_gs_quantity"] > 0:
        top_gs_quan = []
    if features["top_num_gs_length"] > 0:
        top_gs_len = []
    if features["proc_gs"]:
        len_gs_chats = [[], [], []]   # all chats
    if features["top_num_gs_in_every_chat"] > 0:
        len_gs_in_chat = {}   # top long gs in chat

    if features["top_num_circ_quantity"] > 0:
        top_circ_quan = []
    if features["top_num_circ_length"] > 0:
        top_circ_len = []
    if features["proc_circ"]:
        len_circ_chats = [[], [], []]   # all chats
    if features["top_num_circ_in_every_chat"] > 0:
        len_circ_in_chat = {}   # top long circ in chat

    if features["top_num_ph_call_quantity"] > 0:
        top_ph_call_quan = []
    if features["top_num_ph_call_length"] > 0:
        top_ph_call_len = []
    if features["proc_ph_call"]:
        len_ph_call_chats = [[], [], []]   # all chats
    if features["top_num_ph_call_in_every_chat"] > 0:
        len_ph_call_in_chat = {}   # top long ph_call in chat

    if features["top_num_gr_call_quantity"] > 0:
        top_gr_call_quan = []
    if features["top_num_gr_call_length"] > 0:
        top_gr_call_len = []
    if features["proc_gr_call"]:
        len_gr_call_chats = [[], [], []]   # all chats

    if features["favourite_sticker"] is not None:
        top_fav_stickers = {}

    if features["photos_summary"]:
        photos_summary = 0

    if features["videos_summary"]:
        videos_summary = 0

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
                sum = sum(analysed_chat.symbol_sum.values())
                quan_symbol_chats[chat.name] = sum
            if features["proc_words"]:
                sum = sum(analysed_chat.word_sum.values())
                quan_word_chats[chat.name] = sum
            if features["proc_messages"]:
                sum = sum(analysed_chat.message_sum.values())
                quan_message_chats[chat.name] = sum

            if features["symbols_summary"]:
                sum = sum(analysed_chat.symbol_sum.values())
                symbols_summary += sum
            if features["words_summary"]:
                sum = sum(analysed_chat.word_sum.values())
                words_summary += sum
            if features["messages_summary"]:
                sum = sum(analysed_chat.message_sum.values())
                messages_summary += sum

            if features["symbols_per_day"]:
                analysed = analysed_chat.symbol_days
                symbol_per_day[chat.id] = [chat.name, analysed]
            if features["words_per_day"]:
                analysed = analysed_chat.word_days
                word_per_day[chat.id] = [chat.name, analysed]
            if features["messages_per_day"]:
                analysed = analysed_chat.message_days
                message_per_day[chat.id] = [chat.name, analysed]

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
                    sum = analysed_chat.gs_len[aut]
                    if aut == features["proc_gs"]:
                        send += sum
                    else:
                        recv += sum
                len_gs_chats[1].append(send)
                len_gs_chats[2].append(recv)
            if features["top_num_gs_in_every_chat"] > 0:
                len_gs_in_chat[chat.id] = [chat.name, analysed_chat.top_long_gs]

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
                    sum = analysed_chat.circ_len[aut]
                    if aut == features["proc_circ"]:
                        send += sum
                    else:
                        recv += sum
                len_circ_chats[1].append(send)
                len_circ_chats[2].append(recv)
            if features["top_num_circ_in_every_chat"] > 0:
                len_circ_in_chat[chat.id] = [chat.name, analysed_chat.top_long_circ]

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
                    sum = analysed_chat.ph_call_len[aut]
                    if aut == features["proc_ph_call"]:
                        send += sum
                    else:
                        recv += sum
                len_ph_call_chats[1].append(send)
                len_ph_call_chats[2].append(recv)
            if features["top_num_ph_call_in_every_chat"] > 0:
                len_ph_call_in_chat[chat.id] = [chat.name, analysed_chat.top_long_ph_call]

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
                    sum = analysed_chat.gr_call_len[aut]
                    if aut == features["proc_gr_call"]:
                        send += sum
                    else:
                        recv += sum
                len_gr_call_chats[1].append(send)
                len_gr_call_chats[2].append(recv)
            
            if features["favourite_sticker"] is not None:
                sticker_append(top_fav_stickers, analysed_chat.fav_stick)

            if features["photos_summary"]:
                sum = sum(analysed_chat.photo_sum.values())
                photos_summary += sum
            
            if features["videos_summary"]:
                sum = sum(analysed_chat.video_sum.values())
                videos_summary += sum
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
        plot_create(output_folder, symbols_summary, "symbol")
    if features["words_per_day"]:
        plot_create(output_folder, words_summary, "word")
    if features["messages_per_day"]:
        plot_create(output_folder, messages_summary, "message")

    if features["top_num_gs_quantity"] > 0:
        ret_stats["top_num_gs_quantity"] = top_gs_quan
    if features["top_num_gs_length"] > 0:
        ret_stats["top_num_gs_length"] = top_gs_len
    if features["proc_gs"] is not None:
        hist_create(output_folder, len_gs_chats, "gs")
    if features["top_num_gs_in_every_chat"] > 0:
        ret_stats["top_num_gs_in_every_chat"] = len_gs_in_chat

    if features["top_num_circ_quantity"] > 0:
        ret_stats["top_num_circ_quantity"] = top_circ_quan
    if features["top_num_circ_length"] > 0:
        ret_stats["top_num_circ_length"] = top_circ_len
    if features["proc_circ"] is not None:
        hist_create(output_folder, len_circ_chats, "circ")
    if features["top_num_circ_in_every_chat"] > 0:
        ret_stats["top_num_circ_in_every_chat"] = len_circ_in_chat

    if features["top_num_ph_call_quantity"] > 0:
        ret_stats["top_num_ph_call_quantity"] = top_ph_call_quan
    if features["top_num_ph_call_length"] > 0:
        ret_stats["top_num_ph_call_length"] = top_ph_call_len
    if features["proc_ph_call"] is not None:
        hist_create(output_folder, len_ph_call_chats, "ph_call")
    if features["top_num_ph_call_in_every_chat"] > 0:
        ret_stats["top_num_ph_call_in_every_chat"] = len_ph_call_in_chat

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

    if features["photos_summary"]:
        bar_create(output_folder, photos_summary, "photo")

    if features["videos_summary"]:
        bar_create(output_folder, videos_summary, "video")

    return ret_stats
