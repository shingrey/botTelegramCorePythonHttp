import time
import urllib.request as request
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
   getattr(ssl, '_create_unverified_context', None)): 
   ssl._create_default_https_context = ssl._create_unverified_context

class InternetOk():
    def Internet(self):
        siInternet = False
        while not siInternet:    
            try :
                web = "https://www.google.com/"
                data = request.urlopen(web)
                siInternet = True
                break
            except:
                siInternet = False
                time.sleep(20)
        return  siInternet
# inter = InternetOk()
# print (inter.Internet())