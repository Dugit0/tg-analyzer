"""
Special module for creating class of messages.
"""
import json


#Constants and arrays

DATA_PATH = "/home/artiomka/Desktop/tg-data/result.json"


#extra functions

def game_finder(login, message):
    '''
    Finds a place of login in the game.
    '''
    for line in message["text"]:
        if type(line) is str and line.find(login) != -1:
            return line[1: line.find(".")]


#main module classes

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
        '''
        Finds the requirement params (that are used in every single message) and optional params (that are in specific types of messages)
	'''
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

class Message():
    """
    Message object consists of telegram's fields + some useful extra fields, like a type, game table etc.
    """
    #main params
    msg_login = None   #about who info is
    msg_type = None   #type of a message
    '''
    Available types:
    "simple_text", "sticker", "voice_message", "video_message", "audio_file", "video_file", "animation", "file", 
    "photo", "poll", "sticker_emoji", "send_contact", "send_location", 'bot_usage", "game", "unknown"
    '''
    msg_game_tables = {}   #game results

    #chat_params
    chat_name = None   #name of a chat of this message
    chat_id = None   #id of a chat of this message
    chat_type = None   #type of a chat of this message

    #required_params
    mes_date = None   #when it was sent
    mes_date_unixtime = None   #when it was sent in unixtime
    mes_from = None   #who sent it
    mes_from_id = None   #who sent it in id
    mes_id = None   #message's id
    mes_text = None   #text in this message
    mes_text_entities = None
    '''
    'bot_command', 'email', 'spoiler', 'mention_name', 'blockquote', 'bold', 'code', 'underline', 'strikethrough', 
    'phone', 'cashtag', 'text_link', 'italic', 'hashtag', 'plain', 'pre', 'mention', 'custom_emoji', 'link'
    '''
    mes_type = None   #telegram type of a message

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

    def __init__(self, message, chat, login, req_params):
        for key in chat.keys():   #its dinamic because we find these params dynamic
            self.__dict__[f"chat_{key}"] = chat[key]
        tmp_simple_text = True   #flag for simple text message
        for key in message.keys():
            if key not in req_params:
                if key not in ['edited', 'edited_unixtime', 'forwarded_from', \
                               'reply_to_message_id', 'reply_to_peer_id']:
                    tmp_simple_text = False
            self.__dict__[f"mes_{key}"] = message[key]
        self.msg_login =  self.mes_from
        if tmp_simple_text:
            self.msg_type = "simple_text"
        elif self.mes_forwarded_from is None and \
                self.mes_media_type in ["sticker",  #sticker message
                                        "voice_message",  #gs message
                                        "video_message",  #circle message
                                        "audio_file",  #message with an audio file
                                        "video_file",  #message with a video
                                        "animation"]:  #message with a gif
            self.msg_type = self.mes_media_type
        elif self.mes_mime_type:   #message with a file
            self.msg_type = "file"
        elif self.mes_photo:   #message with a photo
            self.msg_type = "photo"
        elif self.mes_poll:   #questionnaire
            self.msg_type = "poll"
        elif self.mes_sticker_emoji:   #sticker emoji
            self.msg_type = "sticker_emoji"
        elif self.mes_contact_information:   #maybe for future
            self.msg_type = "send_contact"
        elif self.mes_location_information:   #maybe for future
            self.msg_type = "send_location"
        elif self.mes_via_bot:   #using a bot
            self.msg_type = "bot_usage"
        elif self.mes_game_title and (place := game_finder(login, message)):   #competition tables
            self.msg_type = "game"
            self.msg_game_tables[self.mes_game_title] = place
        else:
            self.msg_type = "unknown"
        '''
        elif self.mes_self_destruct_period_seconds:   #maybe for future
            self.msg_type = "self_destruct"
        '''   #not sure if its needed
	


def start_api(login):
    '''
    Function, that analyses json file and returns an array with Message objects.
    params:
    - login: user's login, about who the main info is (game stats, geolocation etc)
    return params:
    - messages: an array with Message objects.
    '''
    extractor = Extraction()
    data = extractor.data_ex()
    chats = extractor.chats_ex()
    message_keys = extractor.message_keys_ex()
    required_params, optional_params = extractor.req_opt_params_ex()
    messages = []
    #print(required_params, "\n-------------\n", optional_params)
    for chat in chats:
        for message in chat['messages']:
            if message["type"] != "service":
                tmp_mes = Message(message, chat, login, required_params)
                messages.append(tmp_mes)
    return messages
