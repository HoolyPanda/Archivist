import os
import requests
import pyqrcode
import base64

def SearchForData(title: str):
    path = './Data/'
    for file in os.listdir(path):
        if title.lower() in file.lower():
            return open(f'{path}{file}').read()
    return False

def GetTitles():
    path = './Data/'
    titles = 'Заголовки в базе данных:\n'
    for file in os.listdir(path):
        title = file.replace('.txt', '')
        titles += f'===>{title}'
    return titles

def LoadSecretFile(title: str):
    filesPath = './HiddenDB/Files/'
    for file in os.listdir(filesPath):
        if title in file:
            return open(f'{filesPath}{file}').read()
    return False

def GenerateQR(text: str):
    payload = str(base64.b64encode(bytes(f'{text}', 'utf-8')), 'utf-8')
    a = pyqrcode.create(payload)
    txt = text.replace('.txt', '')
    QRfile = f'./QRs/{txt}.png'
    a.png(QRfile, scale=8, module_color= [0, 0, 0, 255], background=[0xff, 0xff, 0xff])
    pass

def SaveSecretFiles(files: []):
    filesPath = './HiddenDB/Files/'
    a = files
    try:
        for file in files:
            if file['type'] == 'doc' and file['doc']['ext'] == 'txt':
                fileName = file['doc']['title']
                result = requests.get(file['doc']['url'])
                fs = open(f'{filesPath}{fileName}', 'wb+')
                fs.write(result._content)
                fs.close()
                GenerateQR(fileName)
        return True
    except Exception as e:
        return False
