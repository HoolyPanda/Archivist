from vk_api import bot_longpoll
import keyboards
import random
import threading
import json
import payloads


class LongPollServer(threading.Thread):
    
    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session = session
        self.lps = bot_longpoll.VkBotLongPoll(session, 172301854)
        pass

    def run(self):
        for event in bot_longpoll.VkBotLongPoll.listen(self.lps):
            print(str(event))
            if event.type.value == 'message_new':
                self.sender = event.raw['object']['from_id']
                if 'payload' in event.raw['object']:
                    if event.raw['object']['payload'] == "{\"command\":\"start\"}":
                        self.session.method('messages.send', {
                                                            'message':'Выберите тему', 
                                                            'peer_id':self.sender,  
                                                            'random_id': random.randint(1, 100000000000), 
                                                            'keyboard': keyboards.beginKeyboard})
                    self.payload = json.loads(event.raw['object']['payload'])
                    print(event.raw['object']['payload'])
                    data = payloads.GetDataByTheme(theme= self.payload['button'])
                    if data:
                        self.session.method('messages.send',
                                            {
                                                'message': data,
                                                'peer_id': self.sender,
                                                'random_id': random.randint(1, 100000000),
                                                'keyboard': keyboards.beginKeyboard
                                            }) 
                    else:
                        self.session.method('messages.send', {
                                                            'message':'Это невозможно. Должно быть, архивы неполные.', 
                                                            'peer_id':self.sender,  
                                                            'random_id': random.randint(1, 100000000000), 
                                                            'keyboard': keyboards.beginKeyboard})
                if event.raw['object']['text'] == '!Начать':
                    self.session.method('messages.send', {
                                                            'message':'Выберите тему', 
                                                            'peer_id':self.sender,  
                                                            'random_id': random.randint(1, 100000000000), 
                                                            'keyboard': keyboards.beginKeyboard})
                    
            pass
        pass
