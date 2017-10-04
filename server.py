import tweepy
import schedule
import time
from datetime import datetime
import os
from flask import Flask
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

executor = ThreadPoolExecutor(max_workers=1)

count = 1 # contador para los nombres de las fotos

def crear_api(): #acceso a twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True, compression=True)
    return api

def tweet_image():
    global count
    api = crear_api()
    message = '#JaneBirkin'
    filename = 'static/fotos/janebirkin' + str(count) + '.jpg'
    api.update_with_media(filename, status=message) #tweet
    print 'tweet: ' + str(datetime.now())
    print filename
    count += 1
    
def diario(): #corre la funcion tweet_image() cada dia
    #schedule.every( 60 ).minutes.do( tweet_image ).run()
    schedule.every().day.at("10:00").do( tweet_image ).run()
    while True:
        schedule.run_pending()
        time.sleep(1)

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def run():
    executor.submit(diario)
    return 'running'
    
    
@app.route('/detener')
def detener():
    
    schedule.cancel_job(tweet_image)
    schedule.clear()
    
    return "detenido"

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 8080)))