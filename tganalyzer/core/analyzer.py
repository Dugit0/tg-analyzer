"""Создает статистику по сообщениям."""
import bisect
import creator


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

features_create(features, feat_fl):
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
    if feat_fl["top_3_gs_length"]:
        features["gs_len"] = True
        features["top_long_gs"] = True
    if feat_fl["proc_gs"]:
        features["gs_len"] = True

    if feat_fl["top_3_circ_quantity"]:
        features["circ_sum"] = True
    if feat_fl["top_3_circ_length"]:
        features["circ_len"] = True
        features["top_long_circ"] = True
    if feat_fl["proc_circ"]:
        features["circ_len"] = True

    if feat_fl["top_3_ph_call_quantity"]:
        features["ph_call_sum"] = True
    if feat_fl["top_3_ph_call_length"]:
        features["ph_call_len"] = True
        features["top_long_ph_call"] = True
    if feat_fl["proc_ph_call"]:
        features["ph_call_len"] = True

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

def top_counter_chats(update, analysed, author, number):
    """Помогает составлять топы по размеру сообщений по чатово"""

    sum = 0
    for aut in analysed.keys():
        sum += analysed[aut]
    top_counter(update, author, sum)


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

    def __init__(self, features, chat):
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
        if features["top_long_ph_call_len"]:
            self.top_long_ph_call_len = []
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
                if aut not in fav_stick.keys():
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
    features_creat(features, features_flags)
    if features_flags["top_3_symbol_quantity"]:
        top_symbols = []
    if features_flags["top_3_word_quantity"]:
        top_words = []
    if features_flags["top_3_message_quantity"]:
        top_messages = []

    for chat in parsed_chats:
        if chat.id in chat_ids:
            analysed_chat = Chat_stat(features, chat)
            if features_flags["top_3_symbol_quantity"]:
                analysed = analysed_chat.symbol_sum
                top_counter_chats(top_symbols, analysed, chat.id, sum)
            if features["top_3_word_quantity"]:
                analysed = analysed_chat.word_sum
                top_counter_chats(top_words, analysed, chat.id, sum)
            if features["top_3_message_quantity"]:
                analysed = analysed_chat.message_sum
                top_counter_chats(top_messages, analysed, chat.id, sum)
        else:
            continue

    ret_stats = {}
    if features_flags["top_3_symbol_quantity"]:
        ret_stats["top_3_symbol_quantity"] = top_symbols
    if features_flags["top_3_word_quantity"]:
        ret_stats["top_3_word_quantity"] = top_words
    if features_flags["top_3_message_quantity"]:
        ret_stats["top_3_message_quantity"] = top_messages

    return ret_stats
