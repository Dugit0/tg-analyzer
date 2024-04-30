"""
Special module for creating class of messages.
"""
import json


#Constants and arrays

DATA_PATH = "/home/artiomka/Desktop/tg-data/result.json"


#extra functions

def game_finder(login, message):
    for line in message["text"]:
        if type(line) is str and line.find(login) != -1:
            return line[1: line.find(".")]


#main module classes

class Extraction():

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


    def messages_ex_all(self):
        """
        Return iterator of all messages.
        """
        for chat in self.chats:
            for message in chat['messages']:
                yield message


    def message_filter(self, message):
        """
        Filter for excluding system messages.
        """
        return message['type'] != 'service'


    def message_keys_ex(self):
        """
        Function for finding keys in messages.
        """
        self.message_keys = sorted(list({str(list(message.keys())) for message in self.messages_ex_all() if self.message_filter(message)}))
        return self.message_keys


    def req_opt_params_ex(self):
        self.required_params = []
        self.optional_params = []
        message_keys = sorted(list({tuple(message.keys()) for message in self.messages_ex_all() if self.message_filter(message)}))
        params = sorted(list({par for keys in message_keys for par in keys }))
        for par in params:
            if all(map(lambda keys: par in keys, self.message_keys)):
                self.required_params.append(par)
            else:
                self.optional_params.append(par)
        return (self.required_params, self.optional_params)

class MessClass():
    """
    Message class.
    """
    #main params
    msg_login = None
    msg_type = None
    msg_game_tables = {}

    #chat_params
    chat_name = None
    chat_id = None
    chat_type = None

    #required_params
    mes_date = None
    mes_date_unixtime = None
    mes_from = None 
    mes_from_id = None 
    mes_id = None
    mes_text = None
    mes_text_entities = None
    mes_type = None

    #optional_params
    mes_author = None   #anonim group message
    mes_contact_information = None   #send to someone else smbd's contact
    mes_duration_seconds = None   #for gs/circles/videos/audio
    mes_edited = None   #if edited
    mes_edited_unixtime = None   #when edited
    mes_file = None   #data for gs/circles etc
    mes_forwarded_from = None   #if forwarded
    mes_game_description = None   #\
    mes_game_link = None          #| - game messages
    mes_game_title = None         #/
    mes_height = None   #stickers + photos
    mes_inline_bot_buttons = None   #bot buttons under the message
    mes_location_information = None   #locations
    mes_media_type = None   #gs, circles, photos, audio, video
    mes_mime_type = None   #exact type of video, audio etc file
    mes_performer = None   #singer for audio files
    mes_photo = None   #if it has photo
    mes_poll = None   #questionnaire
    mes_reply_to_message_id = None   #if is it a reply
    mes_reply_to_peer_id = None   #if it is a reply id version
    mes_saved_from = None   #reply from another chat
    mes_self_destruct_period_seconds = None   #destruct message
    mes_sticker_emoji = None   #not a sticker, but an emoji
    mes_thumbnail = None   #file, example: pdf
    mes_title = None   #song title
    mes_via_bot = None   #bot using
    mes_width = None   #stickers + photos

    def __init__(self, message, chat, login):
        for key in chat.keys():
            self.__dict__[f"chat_{key}"] = chat[key]
        for key in message.keys():
            self.__dict__[f"mes_{key}"] = message[key]
        self.msg_login =  self.mes_from
        if self.mes_forwarded_from is None and \
                self.mes_media_type in ["sticker",  #obvious
                                        "voice_message",  #gs
                                        "video_message",  #circle
                                        "audio_file",  #song etc
                                        "video_file",  #video
                                        "animation"]:  #gifs
            self.msg_type = self.mes_media_type
        elif self.mes_self_destruct_period_seconds:   #maybe for future
            self.msg_type = "self_destruct"
        elif self.mes_contact_information:   #maybe for fututre
            self.msg_type = "send_contact"
        elif self.mes_location_information:   #maybe for future
            self.msg_type = "send_location"
        elif self.mes_photo:   #photo
            self.msg_type = "photo"
        elif self.mes_via_bot:   #using a bot
            self.msg_type = "bot usage"
        if self.mes_game_title and (place := game_finder(login, message)):   #competition tables
            self.msg_type = "game"
            self.msg_game_tables[self.mes_game_title] = place


types = set()
def start_api(login):
    extractor = Extraction()
    data = extractor.data_ex()
    chats = extractor.chats_ex()
    message_keys = extractor.message_keys_ex()
    required_params, optional_params = extractor.req_opt_params_ex()
    messages_classes = []

    for chat in chats:
        for message in chat['messages']:
            if message["type"] != "service":
                types.add(tuple(message.keys()))
                tmp_mes = MessClass(message, chat, login)
                messages_classes.append(tmp_mes)
    for i in messages_classes:
        print(i.msg_login, i.msg_type, i.msg_game_tables)
    print(len(types))
