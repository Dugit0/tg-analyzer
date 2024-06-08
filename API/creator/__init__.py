"""Специальный модуль для создания массива чатов."""
import json
from datetime import datetime


# Константы и массивы

ZERO = '.000000+00:00'   # для перевода времени в datetime
required_fields_message = ['date',
                           'date_unixtime',
                           'from',
                           'from_id',
                           'id',
                           'text',
                           'text_entities',
                           'type']
optional_fields_message = ['author',
                           'contact_information',
                           'duration_seconds',
                           'edited',
                           'edited_unixtime',
                           'file',
                           'file_name',
                           'forwarded_from',
                           'game_description',
                           'game_link',
                           'game_title',
                           'height',
                           'inline_bot_buttons',
                           'location_information',
                           'media_type',
                           'mime_type',
                           'performer',
                           'photo',
                           'poll',
                           'reply_to_message_id',
                           'reply_to_peer_id',
                           'saved_from',
                           'self_destruct_period_seconds',
                           'sticker_emoji',
                           'thumbnail',
                           'title',
                           'via_bot',
                           'width']
required_fields_service = ['action',
                           'actor',
                           'actor_id',
                           'date',
                           'date_unixtime',
                           'id',
                           'text',
                           'text_entities',
                           'type']
optional_fields_service = ['boosts',
                           'discard_reason',
                           'duration',
                           'duration_seconds',
                           'game_message_id',
                           'height',
                           'inviter',
                           'members',
                           'message_id',
                           'new_icon_emoji_id',
                           'new_title',
                           'photo',
                           'score',
                           'title',
                           'width']

# Доп функции


def game_finder(login, message):
    """Вспомогательная функция, находит место пользователя в игре."""
    for line in message["text"]:
        if type(line) is str and line.find(login) != -1:
            return line[1: line.find(".")]


# Основные классы


class Extraction():
    """Этот класс достает информацию из json файла."""

    def __init__(self, data_path):
        """Достает информацию из json."""
        with open(data_path) as f:
            self.data = json.load(f)

    def chats_ex(self):
        """Возвращает словарь из чатов."""
        self.chats = self.data['chats']['list']
        return self.chats


class Chat():
    """Объект класса Chat состоит из полей чата телеграмма.

    Еще содержит массив из объектов класса Message.
    """

    name = None
    id = None
    type = None
    messages = None

    def __init__(self, chat, login):
        """Берет чат и создает объект с упомянутыми выше полями.

        Еще итерирутеся по сообщениям чата и создает массив объектов Message.
        """
        self.name = chat["name"] if "name" in chat.keys() else None
        self.id = chat["id"]
        self.type = chat["type"]
        messages = []
        for message in chat['messages']:
            if message["type"] == "service" and \
                    message["action"] != "phone_call" and \
                    message["action"] != "group_call":
                continue   # если сообщение типа service и не call, пропуск
            messages.append(Message(message, chat, login))
        self.messages = messages


class Message():
    """Объект класса Message состоит из полей телеграмма.

    Еще есть некоторые поля, такие как тип, игровое место и тп.
    """

    author = None
    send_time = None
    type = None
    text = None
    edited = None
    forwarded = None

    def __init__(self, message, chat, login):
        """Берет сообщение и создает объект.

        Если сообщение типа service, то заведомо оно есть call.
        """
        send_time = datetime.fromisoformat(message["date"] + ZERO)
        self.send_time = send_time
        self.text = message["text"]
        if message["type"] == "service":
            self.author = message["actor"]
            if message["action"] == "phone_call":
                self.duration = message["duration_seconds"] if \
                        "duration_seconds" in message.keys() else 0
                self.type = "single_call"
            else:
                self.duration = message["duration"] if \
                        "duration" in message.keys() else 0
                self.type = "group_call"
        else:
            self.author = message["from"]
            if "edited" in message.keys():
                self.edited = True
                edit_time = datetime.fromisoformat(message["edited"] + ZERO)
                self.edit_time = edit_time
            else:
                self.edited = False
            if "forwarded_from" in message.keys():
                self.forwarded = True
                self.forwarded_from = message["forwarded_from"]
            else:
                self.forwarded = False
            tmp_simple_text = True   # флаг для simple text сообщения
            for key in message.keys():
                if key not in required_fields_message and \
                        key not in ['edited',
                                    'edited_unixtime',
                                    'forwarded_from',
                                    'reply_to_message_id',
                                    'reply_to_peer_id']:
                    tmp_simple_text = False
            if tmp_simple_text:
                self.type = "simple_text"
            elif "media_type" in message.keys() and \
                    message["media_type"] in ["sticker",  # стикер
                                              "voice_message",  # гска
                                              "video_message",  # кружочек
                                              "audio_file",  # аудио файл
                                              "video_file",  # видео
                                              "animation"]:  # гифка
                self.type = message["media_type"]
                if "sticker_emoji" in message.keys():
                    self.sticker_emoji = message["sticker_emoji"]
                if "duration_seconds" in message.keys():
                    self.duration = message["duration_seconds"]
            elif "mime_type" in message.keys():   # сообщение с файлом
                self.type = "file"
            elif "photo" in message.keys():   # сообщение с фото
                self.type = "photo"
            elif "poll" in message.keys():   # опросник
                self.type = "poll"
            elif "contact_information" in message.keys():   # контакт
                self.type = "contact"
            elif "location_information" in message.keys():   # геолокация
                self.type = "location"
            elif "via_bot" in message.keys():   # использование бота
                self.type = "bot_usage"
            elif "game_title" in message.keys() and \
                    (place := game_finder(login, message)):   # игры
                self.type = "game"
                self.game_title = message["game_title"]
                self.game_place = place
            self.type = "unknown"


def start_api(login, path):
    """Анализирует файл json и возвращает массив с объектами класса Chat.

    params:
    - login: логин пользователя, о котором будет главная инфа.
    return params:
    - ret_chats: массив объектов класса Chat.
    """
    extractor = Extraction(path)
    old_chats = extractor.chats_ex()
    ret_chats = []
    for chat in old_chats:
        ret_chats.append(Chat(chat, login))
    return ret_chats
