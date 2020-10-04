
from bs4 import BeautifulSoup
import requests
import pandas as pd
import yaml
from langdetect import detect
import datetime, time

def get_time(time_stamp):

    if time_stamp.count(' ')==1:
        past_time=datetime.datetime.strptime(time_stamp, '%b %d')
        past_time = past_time.replace(
            year=datetime.datetime.now().year)
        return "{:%Y-%m-%d}".format(past_time)
    if time_stamp.count(' ')==2:
        past_time=datetime.datetime.strptime(time_stamp, '%d %b %y')
        return "{:%Y-%m-%d}".format(past_time)
    else:
        time_unit={'d':'days','s':'seconds',
                  'm':'minutes', 'h':'hours'}
        value= time_stamp[:-1]
        unit=time_unit[time_stamp[-1]]
        delta=datetime.timedelta(**{unit: float(value)})
        past_time= datetime.datetime.now() - delta
        return "{:%Y-%m-%d %H:%M}".format(past_time)

                              
def get_data(handle):
    temp = requests.get('https://mobile.twitter.com/'+handle)
    bs = BeautifulSoup(temp.text,'lxml')
    result={}
    result['handle']=handle
    statslabels=[]
    statsvalues=[]
    tweets=bs.find_all(class_='tweet-container')
    time_stamps=bs.find_all(class_='timestamp')
    bio = bs.find(class_='bio').text.replace('\n','').strip()
    result['bio']=bio

    stats = bs.find_all(class_='stat')
    for st in stats:
        statslabels.append(st.find(class_="statlabel").text.strip())
        statsvalues.append(st.find(class_="statnum").text.strip())
    statsvalues= [int(value.replace(',','')) for value in statsvalues]
    result.update(dict(zip(statslabels,statsvalues)))


    
    tweet_text=[]
    tweet_id=[]
    for tw in tweets:
        tweet_text.append(tw.text.replace('\n','').strip())
        tweet_id.append(tw.find(class_='tweet-text')['data-id'])    
    result['lan']= detect(bio+' '.join(tweet_text))    
    result['tweet_text']=tweet_text
    result['tweet_id']=tweet_id
    time_stamps=bs.find_all(class_='timestamp')
    


    times=[]
    for ts in time_stamps:
        times.append(ts.text.replace('\n','').strip())
    result['time_stamps']=times
    result['dates']=[get_time(t) for t in times]

    return result

