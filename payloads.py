import os

def GetDataByTheme(theme:str):
    # a = os.listdir('./Data/')
    if (theme + '.txt') in os.listdir('./Data/'):
        return open('./Data/' + theme + '.txt', 'r').read()
    else:
        return None
