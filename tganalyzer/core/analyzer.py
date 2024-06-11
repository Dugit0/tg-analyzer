"""Создает статистику по сообщениям."""
import bisect
import creator
import matplotlib.pyplot as plt


# Константы

MS_TKR = lambda x : x.send_time
TP_SRT = lambda x : x[1]
FEATURES = ["symbol_sum",
            "word_sum",
            "message_sum",
            "gs_sum",
            "gs_len",
            "top_long_gs",
            "circ_sum",
            "circ_len",
            "top_long_circ",
            "ph_call_sum",
            "ph_call_len",
            "top_long_ph_call",
            "gr_call_sum",
            "gr_call_len",
            "fav_stick"]


# Вспомогательные функции

def features_create(features, feat_fl):
    """Помогает 'сузить' фичи"""

    for i in FEATURES:
        features[i] = False
    if feat_fl["top_3_message_quantity"] or \
            feat_fl["proc_messages"] or \
            feat_fl["messages_summary"]:
        features["message_sum"] = True

    if feat_fl["top_3_word_quantity"] or \
            feat_fl["proc_words"] or \
            feat_fl["words_summary"]:
        features["word_sum"] = True

    if feat_fl["top_3_symbol_quantity"] or \
            feat_fl["proc_symbols"] or \
            feat_fl["symbols_summary"]:
        features["symbol_sum"] = True

    if feat_fl["top_3_gs_quantity"]:
        features["gs_sum"] = True
    if feat_fl["top_3_gs_length"] or \
            feat_fl["proc_gs"]:
        features["gs_len"] = True
    if feat_fl["top_3_gs_in_every_chat"]:
        features["top_long_gs"] = True

    if feat_fl["top_3_circ_quantity"]:
        features["circ_sum"] = True
    if feat_fl["top_3_circ_length"] or \
            feat_fl["proc_circ"]:
        features["circ_len"] = True
    if feat_fl["top_3_circ_in_every_chat"]:
        features["top_long_circ"] = True

    if feat_fl["top_3_ph_call_quantity"]:
        features["ph_call_sum"] = True
    if feat_fl["top_3_ph_call_length"] or \
            feat_fl["proc_ph_call"]:
        features["ph_call_len"] = True
    if feat_fl["top_3_ph_call_in_every_chat"]:
        features["top_long_ph_call"] = True

    if feat_fl["top_3_gr_call_quantity"]:
        features["gr_call_sum"] = True
    if feat_fl["top_3_gr_call_length"] or \
            feat_fl["proc_gr_call"]:
        features["gr_call_len"] = True

    if feat_fl["favourite_sticker"]:
        features["fav_stick"]


def quan_counter(update, aut, num):
    """Помогает составлять словари в классе Chat_stat."""

    if aut not in update.keys():
        update[aut] = 0
    update[aut] += num


def top_counter(update, aut, dur):
    """Помогает составлять топы по длительности в чате."""

    if len(update) < 3:
        update.append([aut, dur])
        update.sort(key=TP_SRT, reverse=True)
    else:
        aut_dur = [aut, dur]
        for j in range(3):
            if aut_dur[1] > update[j][1]:
                update[j], aut_dur = aut_dur, update[j]


def top_counter_chats(update, analysed, author):
    """Помогает составлять топы по размеру сообщений по чатово"""

    sum = sum(analysed.values())
    top_counter(update, author, sum)


def pie_create(output_path, all_chats, option):
    """Функция по созданию круговой диаграммы."""

    y = all_chats.keys()
    x = all_chats.values()

    plt.pie(x, labels=y)
    plt.savefig(output_path + f'proc_{option}.png')


def bar_create(output_path, all_chats, option):
    """Функция по созданию столбчатой диаграммы."""

    y = all_chats.keys()
    x = all_chats.values()

    plt.bar(x, labels=y)
    plt.savefig(output_path + f'summary_{option}.png')


def hist_create(output_path, all_chats, option):
    """Функция по созданию хиста."""

    y = all_chats[0]
    x_send = all_chats[1]
    x_recv = all_chats[2]

    plt.hist([x_send, x_recv], stacked=True, label=y)   # не разобрался tbh
    plt.legend()
    plt.savefig(output_path + f'proc_{option}.png')

# Основные классы

class Chat_stat():
    """Класс, поля которого представляют собой статистику по чату.

    fields: (objects' fields depend on the feature_flags)
    - symbol_sum: количество символов в чате (словарь).
    - word_sum: количество слов в чате (словарь).
    - message_sum: количество сообщений в чате (словарь).
    - gs_len: суммарная длина гсок (словарь).
    - top_long_gs: самые длинные гс по чату (массив).
    - circ_len: суммарная длина кружков (словарь).
    - top_long_circ: саммые длинные кружки по чату (массив).
    - ph_call_len: суммарная длина личных звонков по чату (словарь).
    - top_long_ph_call: самые длинные звонки по чату (массив).
    - gr_call_len: суммарная длина групповых звонков по чату (число).
    - fav_stick: любимый стикер-эмоджи по чату (словарь).
    """

    def __init__(self, features, chat, time_gap):
        """Инициализирует объект класса, подсчитывая статистику по чату.

        params:
        - features: какие фичи надо проанализировать.
        - chat: анализируемый чат.
        """

        if features["symbol_sum"]:
            self.symbol_sum = {}
        if features["word_sum"]:
            self.word_sum = {}
        if features["message_sum"]:
            self.message_sum = {}
        if features["gs_sum"]:
            self.gs_sum = {}
        if features["gs_len"]:
            self.gs_len = {}
        if features["top_long_gs"]:
            self.top_long_gs = []
        if features["circ_sum"]:
            self.circ_sum = {}
        if features["circ_len"]:
            self.circ_len = {}
        if features["top_long_circ"]:
            self.top_long_circ = []
        if features["ph_call_sum"]:
            self.ph_call_sum = {}
        if features["ph_call_len"]:
            self.ph_call_len = {}
        if features["top_long_ph_call"]:
            self.top_long_ph_call = []
        if features["gr_call_sum"]:
            self.gr_call_sum = {}
        if features["gr_call_len"]:
            self.gr_call_len = {}
        if features["fav_stick"]:
            self.fav_stick = {}

        start_mes = bisect.bisect_left(chat.messages, time_gap[0], key=MS_TKR)
        end_mes = bisect.bisect_right(chat.messages, time_gap[1], key=MS_TKR)
        for i in range(start_mes, end_mes + 1):
            message = chat.messages[i]
            aut = message.author
            if features["symbol_sum"]:
                tmp_str = message.text.replace(' ', '')
                quan_counter(self.symbol_sum, aut, len(tmp_str))
            if features["word_sum"]:
                quan_counter(self.word_sum, aut, len(message.text.split()))
            if features["message_sum"]:
                quan_counter(self.message_sum, aut, 1)
            if features["ph_call_sum"] and \
                    message.type == "single_call":
                quan_counter(self.ph_call_sum, aut, 1)
            if features["ph_call_len"] and \
                    message.type == "single_call":
                dur = message.duration
                quan_counter(self.ph_call_len, aut, dur)
            if features["top_long_ph_call"] and \
                    message.type == "single_call":
                dur = message.duration
                top_counter(self.top_long_ph_call, aut, dur)
            if features["gr_call_sum"] and \
                    message.type == "group_call":
                quan_counter(self.gr_call_sum, aut, 1)
            if features["gr_call_len"] and \
                    message.type == "group_call":
                dur = message.duration
                quan_counter(self.gr_call_len, aut, dur)

            if features["gs_sum"] and \
                    message.type == "voice_message":
                quan_counter(self.gs_sum, aut, 1)
            if features["gs_len"] and \
                    message.type == "voice_message":
                dur = message.duration
                quan_counter(self.gs_len, aut, dur)
            if features["top_long_gs"] and \
                    message.type == "voice_message":
                dur = message.duration
                top_counter(self.top_long_gs, aut, dur)
            if features["circ_sum"] and \
                    message.type == "video_message":
                quan_counter(self.circ_sum, aut, 1)
            if message.type == "video_message" and \
                    features["circ_len"]:
                dur = message.duration
                quan_counter(self.circ_len, aut, dur)
            if message.type == "video_message" and \
                    features["top_long_circ"]:
                dur = message.duration
                top_counter(self.top_long_circ, aut, dur)
            if features["fav_stick"] and \
                    message.type == "sticker" and \
                            message.sticker_emoji is not None:
                emo = message.sticker_emoji
                if aut not in self.fav_stick.keys():
                    self.fav_stick[aut] = {}
                quan_counter(self.fav_stick[aut], emo, 1)


# Основные функции

def start_analyses(parsed_chats, chat_ids, time_gap, 
                   features_flags, output_folder, login):
    """Основная функция для анализа.

    params:
    - parsed_chats: массив объектов класса Chat из creator.
    - chat_ids: id чатов, которые будут анализироваться.
    - time_gap: границы временного интервала.
    - features_flags: словарь фичей, на основе которых будет происходить анализ.
                - структура: (фича: bool)
    - output_folder: папка, в которую пойдут выходные файлы.
    - login: логин отправителя.
    return params:
    - ret_stat: словарь, содержащий общую статистику.
    """

    features = {}
    features_create(features, features_flags)
    if features_flags["top_3_symbol_quantity"]:
        top_symbols = []
    if features_flags["top_3_word_quantity"]:
        top_words = []
    if features_flags["top_3_message_quantity"]:
        top_messages = []

    if features_flags["proc_symbols"]:
        quan_symbol_chats = {}
    if features_flags["proc_words"]:
        quan_word_chats = {}
    if features_flags["proc_messages"]:
        quan_message_chats = {}

    if features_flags["symbols_summary"]:
        symbols_summary = 0
    if features_flags["words_summary"]:
        words_summary = 0
    if features_flags["messages_summary"]:
        messages_summary = 0

    if features_flags["top_3_gs_quantity"]:
        top_gs_quan = []
    if features_flags["top_3_gs_length"]:
        top_gs_len = []
    if features_flags["proc_gs"]:
        len_gs_chats = [[], [], []]   # all chats
    if features_flags["top_3_gs_in_every_chat"]:
        len_gs_in_chat = {}   # top long gs in chat

    if features_flags["top_3_circ_quantity"]:
        top_circ_quan = []
    if features_flags["top_3_circ_length"]:
        top_circ_len = []
    if features_flags["proc_circ"]:
        len_circ_chats = [[], [], []]   # all chats
    if features_flags["top_3_circ_in_every_chat"]:
        len_circ_in_chat = {}   # top long circ in chat

    if features_flags["top_3_ph_call_quantity"]:
        top_ph_call_quan = []
    if features_flags["top_3_ph_call_length"]:
        top_ph_call_len = []
    if features_flags["proc_ph_call"]:
        len_ph_call_chats = [[], [], []]   # all chats
    if features_flags["top_3_ph_call_in_every_chat"]:
        len_ph_call_in_chat = {}   # top long ph_call in chat

    if features_flags["top_3_gr_call_quantity"]:
        top_gr_call_quan = []
    if features_flags["top_3_gr_call_length"]:
        top_gr_call_len = []
    if features_flags["proc_gr_call"]:
        len_gr_call_chats = [[], [], []]   # all chats

    for chat in parsed_chats:
        if chat.id in chat_ids:
            analysed_chat = Chat_stat(features, chat, time_gap)

            if features_flags["top_3_symbol_quantity"]:
                analysed = analysed_chat.symbol_sum
                top_counter_chats(top_symbols, analysed, chat.id)
            if features["top_3_word_quantity"]:
                analysed = analysed_chat.word_sum
                top_counter_chats(top_words, analysed, chat.id)
            if features["top_3_message_quantity"]:
                analysed = analysed_chat.message_sum
                top_counter_chats(top_messages, analysed, chat.id)

            if features_flags["proc_symbols"]:
                sum = sum(analysed_chat.symbol_sum.valuses())
                quan_symbol_chats[chat.name] = sum
            if features_flags["proc_words"]:
                sum = sum(analysed_chat.word_sum.valuses())
                quan_word_chats[chat.name] = sum
            if features_flags["proc_messages"]:
                sum = sum(analysed_chat.message_sum.valuses())
                quan_message_chats[chat.name] = sum

            if features_flags["symbols_summary"]:
                sum = sum(analysed_chat.symbol_sum.valuses())
                symbols_summary += sum
            if features_flags["words_summary"]:
                sum = sum(analysed_chat.word_sum.valuses())
                words_summary += sum
            if features_flags["messages_summary"]:
                sum = sum(analysed_chat.message_sum.valuses())
                messages_summary += sum

            if features_flags["top_3_gs_quantity"]:
                analysed = analysed_chat.gs_sum
                top_counter_chats(top_gs_quan, analysed, chat.id)
            if features_flags["top_3_gs_length"]:
                analysed = analysed_chat.gs_len
                top_counter_chats(top_gs_len, analysed, chat.id)
            if features_flags["proc_gs"]:
                len_gs_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.gs_len.keys():
                    sum = analysed_chat.gs_len[aut]
                    if aut == login:
                        send += sum
                    else:
                        recv += sum
                len_gs_chats[1].append(send)
                len_gs_chats[2].append(recv)
            if features_flags["top_3_gs_in_every_chat"]:
                len_gs_in_chat[chat.id] = [chat.name, analysed_chat.top_long_gs]

            if features_flags["top_3_circ_quantity"]:
                analysed = analysed_chat.circ_sum
                top_counter_chats(top_circ_quan, analysed, chat.id)
            if features_flags["top_3_circ_length"]:
                analysed = analysed_chat.circ_len
                top_counter_chats(top_circ_len, analysed, chat.id)
            if features_flags["proc_circ"]:
                len_circ_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.circ_len.keys():
                    sum = analysed_chat.circ_len[aut]
                    if aut == login:
                        send += sum
                    else:
                        recv += sum
                len_circ_chats[1].append(send)
                len_circ_chats[2].append(recv)
            if features_flags["top_3_circ_in_every_chat"]:
                len_circ_in_chat[chat.id] = [chat.name, analysed_chat.top_long_circ]

            if features_flags["top_3_ph_call_quantity"]:
                analysed = analysed_chat.ph_call_sum
                top_counter_chats(top_ph_call_quan, analysed, chat.id)
            if features_flags["top_3_ph_call_length"]:
                analysed = analysed_chat.ph_call_len
                top_counter_chats(top_ph_call_len, analysed, chat.id)
            if features_flags["proc_ph_call"]:
                len_ph_call_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.ph_call_len.keys():
                    sum = analysed_chat.ph_call_len[aut]
                    if aut == login:
                        send += sum
                    else:
                        recv += sum
                len_ph_call_chats[1].append(send)
                len_ph_call_chats[2].append(recv)
            if features_flags["top_3_ph_call_in_every_chat"]:
                len_ph_call_in_chat[chat.id] = [chat.name, analysed_chat.top_long_ph_call]

            if features_flags["top_3_gr_call_quantity"]:
                analysed = analysed_chat.gr_call_sum
                top_counter_chats(top_gr_call_quan, analysed, chat.id)
            if features_flags["top_3_gr_call_length"]:
                analysed = analysed_chat.gr_call_len
                top_counter_chats(top_gr_call_len, analysed, chat.id)
            if features_flags["proc_gr_call"]:
                len_gr_call_chats[0].append(chat.name)
                send = 0
                recv = 0
                for aut in analysed_chat.gr_call_len.keys():
                    sum = analysed_chat.gr_call_len[aut]
                    if aut == login:
                        send += sum
                    else:
                        recv += sum
                len_gr_call_chats[1].append(send)
                len_gr_call_chats[2].append(recv)
        else:
            continue

    ret_stats = {}
    if features_flags["top_3_symbol_quantity"]:
        ret_stats["top_3_symbol_quantity"] = top_symbols
    if features_flags["top_3_word_quantity"]:
        ret_stats["top_3_word_quantity"] = top_words
    if features_flags["top_3_message_quantity"]:
        ret_stats["top_3_message_quantity"] = top_messages

    if features_flags["proc_symbols"]:
        pie_create(output_folder, quan_symbol_chats, "symbol")
    if features_flags["proc_words"]:
        pie_create(output_folder, quan_word_chats, "word")
    if features_flags["proc_messages"]:
        pie_create(output_folder, quan_message_chats, "message")

    if features_flags["symbols_summary"]:
        bar_create(output_folder, symbols_summary, "symbol")
    if features_flags["words_summary"]:
        bar_create(output_folder, words_summary, "word")
    if features_flags["messages_summary"]:
        bar_create(output_folder, messages_summary, "message")

    if features_flags["top_3_gs_quantity"]:
        ret_stats["top_3_gs_quantity"] = top_gs_quan
    if features_flags["top_3_gs_length"]:
        ret_stats["top_3_gs_length"] = top_gs_len
    if features_flags["proc_gs"]:
        hist_create(output_folder, len_gs_chats, "gs")
    if features_flags["top_3_gs_in_every_chat"]:
        ret_stats["top_3_gs_in_every_chat"] = len_gs_in_chat

    if features_flags["top_3_circ_quantity"]:
        ret_stats["top_3_circ_quantity"] = top_circ_quan
    if features_flags["top_3_circ_length"]:
        ret_stats["top_3_circ_length"] = top_circ_len
    if features_flags["proc_circ"]:
        hist_create(output_folder, len_circ_chats, "circ")
    if features_flags["top_3_circ_in_every_chat"]:
        ret_stats["top_3_circ_in_every_chat"] = len_circ_in_chat

    if features_flags["top_3_ph_call_quantity"]:
        ret_stats["top_3_ph_call_quantity"] = top_ph_call_quan
    if features_flags["top_3_ph_call_length"]:
        ret_stats["top_3_ph_call_length"] = top_ph_call_len
    if features_flags["proc_ph_call"]:
        hist_create(output_folder, len_ph_call_chats, "ph_call")
    if features_flags["top_3_ph_call_in_every_chat"]:
        ret_stats["top_3_ph_call_in_every_chat"] = len_ph_call_in_chat

    if features_flags["top_3_gr_call_quantity"]:
        ret_stats["top_3_gr_call_quantity"] = top_gr_call_quan
    if features_flags["top_3_gr_call_length"]:
        ret_stats["top_3_gr_call_length"] = top_gr_call_len
    if features_flags["proc_gr_call"]:
        hist_create(output_folder, len_gr_call_chats, "gr_call")

    return ret_stats
