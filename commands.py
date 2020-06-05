import requests
import json
class Comandos:
    def __init__(self, botapi):
        global url
        url = "https://api.telegram.org/bot"
        self.botapi = botapi
    def message(self, text, chat_id):
        smsn = url+"{}/sendMessage?chat_id={}&text={}".format(self.botapi,str(chat_id),text)
        requests.post(smsn)

    def messageKeyword(self, text, chat_id, keyboard):
        smsn = url+"{}/sendMessage".format(self.botapi)
        headers = {'content-type': 'application/json'}
        body = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {
                "keyboard": keyboard,
                "one_time_keyboard": True
                
            }

            }
        response = requests.post(smsn, data=json.dumps(body), headers = headers)
        

    def sendVideo(self, chat_id, nameVideo = '', idVideo = ''):
        if nameVideo != '':
            try:
                files = {'video': open(nameVideo,'rb')}
                tlgurl = url+"{}/sendVideo?chat_id={}".format(self.botapi,str(chat_id))
                response = requests.post(tlgurl, files= files)
            except:
                pass    
            
        if idVideo != '':
            tlgurl = url+"{}/sendVideo?chat_id={}&video={}".format(self.botapi,str(chat_id),idVideo)
            response = requests.post(tlgurl)

    def sendPhoto(self, chat_id, namePhoto = '', idPhoto = ''):
        if namePhoto != '':
            try:
                files = {'photo': open(namePhoto,'rb')}
                tlgurl = url+"{}/sendPhoto?chat_id={}".format(self.botapi,str(chat_id))
                requests.post(tlgurl, files= files)
            except:
                pass
        if idPhoto != '':
            tlgurl = url+"{}/sendPhoto?chat_id={}&photo={}".format(self.botapi,str(chat_id),idPhoto)
            response = requests.post(tlgurl)

        
    
    def animaion(self, chat_id, nameGif = '', idAnimation = ''):
        if nameGif != '':
            try:
                files = {'animation': open(nameGif,'rb')}
                tlgurl = url+"{}/sendAnimation?chat_id={}".format(self.botapi,str(chat_id))
                requests.post(tlgurl, files= files)
            except:
                pass
        if idAnimation != '':
            tlgurl = url+"{}/sendAnimation?chat_id={}&animation={}".format(self.botapi,str(chat_id),idAnimation)
            response = requests.post(tlgurl)

    def chatAction(self, chat_id, action = ''):
        if action == '':
            action = 'typing'
        tlgurl = url+"{}/sendPhoto?chat_id={}&action={}".format(self.botapi,str(chat_id),action)
        response = requests.post(tlgurl)


    
