import snscrape.modules.twitter as sntwitter
import pandas as pd
import csv
import os
import tweepy

consumer_key = '9CtULzOKwtotSBbgmqqF5ZSE1'
consumer_secret = 'SFDNiyOXgkPjQvETZXnQOWemCqrssBsZVe3ACYHF2AkA0giPNm'
access_token = '711310452815503360-SfHfZuJSf5vOLBQQOdZGN7GNxaMTNS0'
access_token_secret = 'ybUU3Sq5lWNMpZAyRgJZIPRW960PtwT2jFrfOAQIKEXp1'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

users = ['Conservatives',
         'theresa_may',
         'DamianGreen',
         'PhilipHammondUK',
         'AmberRuddUK',
         'DavidDavisMP',
         'BorisJohnson',
         'Jeremy_Hunt',
         'DLidington',
         'JustineGreening',
         'LiamFox',
         'GregClarkMP',
         'michaelgove',
         'sajidjavid',
         'pritipatel',
         'andrealeadsom',
         'GavinWilliamson',
         'DominicRaab',
         'MattHancock',
         'UKLabour',
         'jeremycorbyn',
         'tom_watson',
         'angelaeagle',
         'EmilyThornberry',
         'johnmcdonnellMP',
         'hilarybennmp',
         'HackneyAbbott',
         'labourlewis',
         'RLong_Bailey',
         'JonAshworth',
         'AngelaRayner',
         'Keir_Starmer',
         'RichardBurgon',
         'DawnButlerBrent',
         'lisanandy',
         'DavidLammy',
         'LibDems',
         'timfarron',
         'vincecable',
         'joswinson',
         'EdwardJDavey',
         'theSNP',
         'NicolaSturgeon',
         'Ianblackford_MP',
         'AngusRobertson',
         'UKIP',
         'paulnuttalukips',
         'Nigel_Farage',
         'TheGreenParty',
         'natalieben',
         'BBCNews',
         'bbclaurak',
         'skynews',
         'LBC',
         'YouGov',
         'guardian']

csvFile = open('output.csv', 'a') #creates a file in which you want to store the data.
csvWriter = csv.writer(csvFile)

for user in users:
    search = ' from:'+'"{}"'.format(user)
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('Covid'+search).get_items()):
        csvWriter.writerow([tweet.date, tweet.content.encode('utf-8'), tweet.username, tweet.id, tweet.user.id])
        print(tweet.username)