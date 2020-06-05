from commands import Comandos
# import os.path as path
# import os
from pymongo import MongoClient
from datetime import datetime
import botandchat
# import pprint
# from bson.son import SON
import random
import gc

botkey = botandchat.config['botKey']
admin = botandchat.config['chatAdmin']
global x
global usuario
x = Comandos(botkey)
meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
now = datetime.now()
client = MongoClient('localhost',27027)
db = client['kmtrn']
posts = db.kmuser

class Acciones:
    def myCommand(self, chat_priv, command = '', params = ''):
        if command == '/start':
            yes = posts.find_one({"idtg": chat_priv})
            #si existe no hacemos nada
            if yes:
                print('hola?')
            else:
                # aqui colocamos el registro del usuario por el chat_id y guardamos si tenemos una espera de resultado o no 
                if params != '':
                    users = {"name": params ,"idtg": chat_priv,"esperando":"","actualizar":""}
                    
                    posts.insert_one(users)
                    x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/24cbiZwzSW8Kc/giphy.gif')
                    x.message('Hola '+ params +' 👋, este es un bot <nombre del bot>',chat_priv)

        #sacamos informacion del usuario para ver si esta esperando una respuesta o ya tenemos alguna informacion
        usuario = posts.find_one({"idtg": chat_priv})
        if command == '' and usuario['esperando'] != '':
            command = usuario['esperando']

        if command == '' and params != '':
            x.chatAction(chat_priv)
            #palabra claves para alguna accion
            if params.find('amo') > -1 or params.find('quiero') > -1  or params.find('el mejor') > -1 or params.find('super bien') > -1 or params.find('chido') > -1:
                x.message('gracias 😘', chat_priv)
                x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/yoJC2El7xJkYCadlWE/giphy.gif')
                x.message(usuario['name'] + ' le gusto :)', admin)
            else:
                if params.find('chiste') > -1:
                        x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/143DwZ9lvbQcbS/giphy.gif')
                        x.message('estamos trabajando en esto gracias 🤠',chat_priv)
                
                else:
                    if params.find('odio') > -1 or params.find('error') > -1  or params.find('basura') > -1 or params.find('falla') > -1 or params.find('fallo') > -1 or params.find('mejorar') > -1:
                        x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif')
                        x.message('Estamos mejorando contactate con @shingrey1 para decirle que problema tienes', chat_priv)
                        x.message(usuario['name'] + ' no le gusto algo', admin)
                        
                    else:                                    
                        x.message('estos son los comandos para interactuar con el bot',chat_priv)
                        x.message('comandos: \n /micomando \n /micomando1 \n /micomando2 \n /micomando3 \n /micomando4 \n /micomando5', chat_priv)

        if command == '/micomando':
            x.chatAction(chat_priv)
            if params == '':
                if(usuario['idtg'] == chat_priv):
                    posts.find_one_and_update({"idtg": chat_priv},{"$set": {"esperando": "/micomando"} })
                    x.message('Pon tu nombre, te recuerdo que es la forma como te vamos a identificar',chat_priv)
            else:
                posts.find_one_and_update({"idtg": chat_priv},{"$set": {"name": params} })
                posts.find_one_and_update({"idtg": chat_priv},{"$set": {"esperando": ""} })
                x.message('💾 guardado',chat_priv)

        
        #ejemplo para cuando modificamos el teclado y esperamos resultados extras
        if command == '/micommando2':
            x.chatAction(chat_priv)
            if params == '':
                if(usuario['idtg'] == chat_priv):
                    posts.find_one_and_update({"idtg": chat_priv},{"$set": {"esperando": "/micommando2"} })
                    keyboard = []
                    count = 0
                    uarray =[]
                    '''
                    para hacer un teclado 
                    [p1][p2][p3]
                    [p4][p5][p6]
                    debemos llenar un array con 3 objetos {text: "quequieresque diga"} y luego agregarlo a la variable keyboard
                    si queremos un teclado
                    [p1]
                    [p2]
                    [p3]
                    [p4]
                    [p5]
                    [p6]
                    podemos agregar elementos a nuestro array keyboard directamente
                    '''
                    while count < now.month:
                        if count == 0:
                            uarray.append({"text": meses[count]})
                            count = count + 1
                        else:
                            if count % 3 == 0:
                                keyboard.append(uarray)
                                uarray = []
                                uarray.append({"text": meses[count]})
                            else:
                                uarray.append({"text": meses[count]})
                                
                            count = count + 1
                            if count >= now.month:
                                keyboard.append(uarray)

                    x.messageKeyword('Mes que te gustaria cambiar',chat_priv, keyboard)
            else:
                if usuario['actualizar'] != "":
                    try:
                        float(params)
                    except :
                        x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/mq5y2jHRCAqMo/giphy.gif')
                        x.message('pon un texto para actualizar :) ',chat_priv)

                    posts.find_one_and_update({"idtg": chat_priv},{"$set": {"esperando": ""} })
                    posts.find_one_and_update({"idtg": chat_priv},{"$set": {"actualizar": ""} })
                    x.message('Gracias 🏃🏻‍♀️🏃🏽‍♂️',chat_priv)
                else:
                    try:
                            
                        if meses.index(params) > -1:  
                            posts.find_one_and_update({"idtg": chat_priv},{"$set": {"actualizar": params} })
                            x.message('pon una actualizacion numerica',chat_priv)
                        else:
                            x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/IhWQ8Uw1JOQgM/giphy.gif')
                            x.message('pon una actualizacion numerica 🤨👇🏽 ',chat_priv)
                    except:
                    
                        x.animaion(chat_priv, idAnimation= 'https://media.giphy.com/media/IhWQ8Uw1JOQgM/giphy.gif')
                        x.message('pon una actualizacion numerica 🤨👇🏽 ',chat_priv)
        

        
        gc.collect()
                    

# y = Acciones()
# y.myCommand(235614699, params='boby')


            
