"""Special module for creating class of messages."""
import json


# Constants and arrays

DATA_PATH = "/home/artiomka/Desktop/tg-data/result.json"
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

# extra functions


def game_finder(login, message):
    """
    Helping function, that just finding a login's place at the game.
    """
    for line in message["text"]:
        if type(line) is str and line.find(login) != -1:
            return line[1: line.find(".")]


# main module classes


class Extraction():
    '''
    This class is extracting information from json file.
    '''
    def data_ex(self, data_path=DATA_PATH):
        """
        Extract data from json.
        """
        with open(data_path) as f:
            self.data = json.load(f)
        return self.data

    def chats_ex(self):
        """
        Return chats dictionary.
        """
        self.chats = self.data['chats']['list']
        return self.chats


class Chat():
    """
    Chat object consists of telegram's chat field's +
    an array of Message objects.
    """
    name = None
    id = None
    type = None
    messages = None

    def __init__(self, chat, login):
        self.name = chat["name"] if "name" in chat.keys() else None
        self.id = chat["id"]
        self.type = chat["type"]
        messages = []
        for message in chat['messages']:
            if message["type"] == "service" and \
                    message["action"] != "phone_call" and \
                    message["action"] != "group_call":
                continue
            messages.append(Message(message, chat, login))
        self.messages = messages


class Message():
    """
    Message object consists of telegram's fields +
    some useful extra fields, like a type, game table etc.
    """
    author = None
    send_time = None
    type = None
    text = None
    edited = None
    forwarded = None

    def __init__(self, message, chat, login):
        self.send_time = message["date"]
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
                self.edit_time = message["edited"]
            else:
                self.edited = False
            if "forwarded_from" in message.keys():
                self.forwarded = True
                self.forwarded_from = message["forwarded_from"]
            else:
                self.forwarded = False
            tmp_simple_text = True   # flag for simple text message
            for key in message.keys():
                if key not in required_fields_message:
                    if key not in ['edited',
                                   'edited_unixtime',
                                   'forwarded_from',
                                   'reply_to_message_id',
                                   'reply_to_peer_id']:
                        tmp_simple_text = False
            if tmp_simple_text:
                self.type = "simple_text"
            elif "media_type" in message.keys() and \
                    message["media_type"] in ["sticker",  # sticker
                                              "voice_message",  # gs
                                              "video_message",  # circle
                                              "audio_file",  # audio file
                                              "video_file",  # video
                                              "animation"]:  # gif
                self.type = message["media_type"]
                if "duration_seconds" in message.keys():
                    self.duration = message["duration_seconds"]
            elif "mime_type" in message.keys():   # message with a file
                self.type = "file"
            elif "photo" in message.keys():   # message with a photo
                self.type = "photo"
            elif "poll" in message.keys():   # questionnaire
                self.type = "poll"
            elif "contact_information" in message.keys():   # for future
                self.type = "contact"
            elif "location_information" in message.keys():   # for future
                self.type = "location"
            elif "via_bot" in message.keys():   # using a bot
                self.type = "bot_usage"
            elif "game_title" in message.keys() and \
                    (place := game_finder(login, message)):   # games
                self.type = "game"
                self.game_title = message["game_title"]
                self.game_place = place
            self.type = "unknown"


def start_api(login):
    '''
    Function, that analyses json file and returns
    an array with Message objects.
    params:
    - login: user's login, about who the main info is
    (game stats, geolocation etc)
    return params:
    - messages: an array with Message objects.
    '''
    extractor = Extraction()
    extractor.data_ex()
    old_chats = extractor.chats_ex()
    ret_chats = []
    for chat in old_chats:
        ret_chats.append(Chat(chat, login))
    return ret_chats
