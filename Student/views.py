from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

def show_graph(request,template_name='live_graph.html'):
    return render(request,template_name)

access_token = "2546128268-Bg9TDA4nyUDmJlQ4b9tn7XVMmPkx3gkRaHfqNY8"
access_token_secret =  "9YmyBfOtyGu6Ew5HurFPQpXiFUU8WXqSgbItX65Kc1NIm"
consumer_key =  "SHqDdve6F6XNin24OVpv7WdWa"
consumer_secret =  "OsDKpKzFvfw0NPnt3ztdeRBcyMxeuwm457yqhTXWHwU0rxtWUi"

sentiment = []
count = 0

class StreamListener(StreamListener):   
    def on_status(self, status):
        if status.retweeted:
            return
        text = status.text
        blob = TextBlob(text)
        sent = blob.sentiment
        polar = sent.polarity
        subj = sent.subjectivity
        if(subj>=0.5):
            if(polar>=0.2):
                sentiment.append('1')
            elif(-0.2<polar<0.2):
                sentiment.append('0')
            else:
                sentiment.append('-1')

def fetch_sensor_values_ajax(request):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream_listener = StreamListener()
    stream = Stream(auth=api.auth, listener=stream_listener)
    topic = request.GET.get('id', None)
    stream.filter(track=[topic])
    data={}
    if request.is_ajax():
            sensor_val=sentiment[0]
            sentiment.pop(0)
            sensor_data=[]
            now=datetime.now()
            ok_date=str(now.strftime('%Y-%m-%d %H:%M:%S'))
            try:
                sensor_val=str(''.join(st[:]))
                if(sensor_val):
                    sensor_data.append(str(sensor_val)+','+ok_date)
                else:
                    sensor_data.append(str(sensor_val)+','+ok_date)
            except Exception as e:
                    sensor_data.append(str(sensor_val)+','+ok_date)
            data['result']=sensor_data
    else:
        data['result']='Not Ajax'
    return JsonResponse(data)
