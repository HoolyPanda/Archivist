import random
from assets.Controller.DataController import SearchForData, GetTitles, LoadSecretFile, SaveSecretFiles
import base64
import threading
import time

class MainView():
    def __init__(self, session, id, event):
        self.vkID = id
        self.session = session
        pass

    def DeleteMsg(self, msgID: []):
        time.sleep(300)
        for id in msgID:
            self.session.method('messages.delete', {
                'message_ids': id,
                'delete_for_all': 1
            })
        pass

    def ParseEvent(self, event):
        if len(event['attachments']) > 0:
            if str(event['from_id']) in open('./whitelist.cred', 'r').readlines():
                if SaveSecretFiles(event['attachments']):
                    self.session.method('messages.send', {
                        'message': f'Файлы успешно загружены',
                        'peer_id': self.vkID,
                        'random_id': random.randint(1, 10000000000000)
                    })
                else:
                    self.session.method('messages.send', {
                        'message': f'Во время загрузки файлов произошла ошибка',
                        'peer_id': self.vkID,
                        'random_id': random.randint(1, 10000000000000)
                    })
        
        try:
            text =  event['text']
            decodedText = base64.b64decode(text)
            fileName = str(decodedText, encoding= 'utf-8')
            responce = LoadSecretFile(fileName)
            if responce:
                msgIDs = []
                # msgIDs.append(event['id'])
                a = self.session.method('messages.send', {
                    'message': f'Получен доступ к секретному файлу {fileName}',
                    'peer_id': self.vkID,
                    'random_id': random.randint(1, 10000000000000)
                })
                msgIDs.append(a)
                a = self.session.method('messages.send', {
                    'message': f'{responce}',
                    'peer_id': self.vkID,
                    'random_id': random.randint(1, 10000000000000)
                })
                msgIDs.append(a)
                b = 0
                t = threading.Thread(target= self.DeleteMsg, kwargs={'msgID': msgIDs}, daemon= True)
                t.start()
            elif not responce:
                self.session.method('messages.send', {
                    'message': f'Код отсутствует в Базе Данных',
                    'peer_id': self.vkID,
                    'random_id': random.randint(1, 10000000000000)
                })
            return True
        except Exception as e:
            if event['text'] != '':
                result = SearchForData(event['text'])
                if result:
                    self.session.method('messages.send', {
                        'message': f'{result}',
                        'peer_id': self.vkID,
                        'random_id': random.randint(1, 10000000000000)
                    })
                else:
                    title = event['text']
                    self.session.method('messages.send', {
                        'message': f'Записей с заголовком {title} не найдено',
                        'peer_id': self.vkID,
                        'random_id': random.randint(1, 10000000000000)
                    })
                    self.session.method('messages.send', {
                        'message': f'{GetTitles()}',
                        'peer_id': self.vkID,
                        'random_id': random.randint(1, 10000000000000)
                    })        
            return True