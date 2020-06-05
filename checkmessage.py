from datetime import datetime
import requests
import os.path as path
from actions import Acciones
from commands import Comandos
import time
from internetok import InternetOk
import subprocess
import sys
import botandchat
#from pymongo import MongoClient
import gc

botkey = botandchat.config['botKey']
url = ""
ts = 0 #ultimo time


acc = Acciones()
inter = InternetOk()

try:
    inicio = Comandos(botkey)
    inicio.message("se acaba de iniciar",botandchat.config['admin'])
    while True:
        inter.Internet()
        # guardamos un archivo con el ultimo update_id de telegram
        if path.exists("/home/pi/Documents/ucdate.txt"):
                f = open("/home/pi/Documents/ucdate.txt", "r")
                ts = int(f.read())
                f.close()
        else:
            ts = 0
        #cada vuelta pedimos a la api de telegram que nos borre los mensajes leidos y contestados
        url = "https://api.telegram.org/bot"+ botkey + "/getUpdates?offset="+ str(ts)
        #verificamos que hay internet
        rq = requests.get(url)
        if rq.status_code == 200:
            r = rq.json()
            # recorremos todos los mensajes 
            for results in r['result']:
                try:
                    if (ts == 0 or results['update_id'] > ts):
                        # pasa por cada mensaje y busca 
                        for mensajes in results['message']:
                            ett = 0
                            if "entities" in mensajes:
                                #buscamos que la palabra bot_command para identificar que es un comando /comando
                                if results['message']['entities'][0]['type'] == 'bot_command':
                                    ett = 1
                                    # esto es si necesito responder y hacer una accion mediante un comando
                                    if results['message']['text'] == '/start':
                                        try:
                                            # si es /start paso  el nombre completo para guardarlo en una BD
                                            if results['message']['chat']['last_name']:
                                                lastName = results['message']['chat']['last_name']
                                        except:
                                            lastName = ''

                                        try:
                                            if results['message']['chat']['first_name']:
                                                firstName = results['message']['chat']['first_name']
                                        except:
                                            firstName = 'user'+results['message']['chat']['id']
                                        
                                        acc.myCommand(results['message']['chat']['id'], command = results['message']['text'], params= firstName + ' ' + lastName )
                                    else: 
                                        #si no es start enviamos el comando a nuestra clase actions
                                        acc.myCommand(results['message']['chat']['id'], command = results['message']['text'])
                                    #guarda el date del mensaje
                                    f = open("/home/pi/Documents/ucdate.txt","w+")
                                    f.write(str(results['update_id']))
                                    f.close()
                                    
                                    #fin
                                break
                        if ett == 0:
                            #revisamos nuevamente los mensajes buscando que sean solo de tipo text
                            for mensajes2 in results['message']:
                                #si es tipo texto enviamos a actions
                                if 'text' in mensajes2:
                                    acc.myCommand(results['message']['chat']['id'],params = results['message']['text'])
                                    f = open("/home/pi/Documents/ucdate.txt","w+")
                                    f.write(str(results['update_id']))
                                    f.close()

                                #si son animaciones pasamos el parametro del file id para que nosotros lo procesamos, si no aceptamos animaciones, solo guarda el update_id
                                if 'animation' in mensajes2:
                                    #acc.myCommand(results['message']['chat']['id'], params = results['message']['animation']['file_id'])
                                    f = open("/home/pi/Documents/ucdate.txt","w+")
                                    f.write(str(results['update_id']))
                                    f.close()
                except:
                    #si falla guardamos el resultado para no ciclar nuestro bot y enviamos al usuario un mensaje de error
                    if (ts == 0 or results['update_id'] > ts):
                        f = open("/home/pi/Documents/ucdate.txt","w+")
                        f.write(str(results['update_id']))
                        f.close()
                        inicio.message("Los errores pasan 😥 prueba otra vez o comunicate con @shingrey1 si se repite el error",results['message']['chat']['id'])

        #borramos basura            
        gc.collect()
        time.sleep(5)        
    
except:
    #si por algun motivo falla todo nos enviamos un correo diciendo que error sucedio y tratamos de alzar el servicio nuevamente por consola
    errores = Comandos(botkey)
    errores.message("se detuvo el bot por alguna razon",botandchat.config['chatAdmin'])
    errores.message(str(sys.exc_info()[0]),botandchat.config['chatAdmin'])
    subprocess.call("python3 /home/pi/Documents/checkmessage.py &",shell=True)

    
    


