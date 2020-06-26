import tweepy
import string
import pandas as pd
import datetime
import re
import nltk
import string
from prob_class_model import *
from district_finder import *
from cred import *
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

#Specify credientials for drive and sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'ibm-hack-281412-af7fffea1c18.json', scope)
gc = gspread.authorize(credentials)

#specify sheet
spreadsheet_key = '1uqktGbmG3PrhgH5OP5Lv_sBa6_JhrocxNQ8owxOT9ng'
wks_name = 'Master'

#tokenize string
def clean_text(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", text).split()) 

#find sentiment
def sentiment_analyzer_scores(text):
    key,url = get_ibm_cred()#get ibm watson sentiment analyzer API credentials
    authenticator = IAMAuthenticator(key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2020-06-21',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text=text,features=Features(sentiment=SentimentOptions(document=True))).get_result()
    #result= print(json.dumps(response, indent=2))
    return(response["sentiment"]["document"]["label"])

#specify credentials for twitter API
consumer_key,consumer_secret, access_token, access_token_secret = get_twitter_cred()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=False)

#find id for india
places = api.geo_search(query="INDIA", granularity="country")
place_id = places[0].id
#previous_tweets = pd.DataFrame(columns=['tweetid','content','place','district','date','problem','sentiment'])
#previous_tweets = pd.read_csv('tweetsy.csv')

#open sheet of previous tweets
ws = gc.open("Tweets").worksheet("Master")
previous_tweets = pd.DataFrame(ws.get_all_records())
end = len(previous_tweets) -1
last_tweet = previous_tweets.loc[end].tweetid - 1
date = previous_tweets.loc[end].date
print(last_tweet ,date)
while(date != '2020-06-15'):
        tweets = api.search(q="place:%s AND covid OR lockdown" % place_id, count=100,lang='en',max_id = last_tweet,)
        for tweet in tweets:
                print(tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")
                try:
                        if(sentiment_analyzer_scores(clean_text(tweet.text)) == 'negative'):
                                problem = classify(tweet.text)
                        else:
                                problem = 'null'
                        if(problem == ''):
                                problem = "null"
                        if(tweet.user.verified):
                                #find district of the place
                                district = place_to_district(tweet.text)
                        else:
                                district = place_to_district(tweet.place.name)
                        if(district==''):
                                continue
                        previous_tweets.loc[len(previous_tweets)]=[tweet.id_str,tweet.text,tweet.place.name,district,tweet.created_at.strftime('%Y-%m-%d'),problem,sentiment_analyzer_scores(clean_text(tweet.text))]
                except:
                        continue
        end = len(previous_tweets) -1
        last_tweet = previous_tweets.loc[end].tweetid
        date = previous_tweets.loc[end].date
        
        print(date)
        d2g.upload(previous_tweets, spreadsheet_key, wks_name, credentials=credentials, row_names=True)

#previous_tweets.to_csv(r'E:/programs/Projects/Twitter Sentiment Analysis/tweetsy.csv',index=False,header= True)
#d2g.upload(previous_tweets, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
  