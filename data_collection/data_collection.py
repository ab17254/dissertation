#!/usr/bin/env python3.8
import csv
import tweepy
import snscrape.modules.twitter as sntwitter

consumer_key = '9CtULzOKwtotSBbgmqqF5ZSE1'
consumer_secret = 'SFDNiyOXgkPjQvETZXnQOWemCqrssBsZVe3ACYHF2AkA0giPNm'
access_token = '711310452815503360-SfHfZuJSf5vOLBQQOdZGN7GNxaMTNS0'
access_token_secret = 'ybUU3Sq5lWNMpZAyRgJZIPRW960PtwT2jFrfOAQIKEXp1'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

users = []
with open('twitter_users.txt', 'r') as f:
    accounts = f.read().split('\n')
    for account in accounts:
        account = account[1:]
        users.append(account)
        f.close()


def scrape():
    for user in users:
        search = ' from:' + '"{}"'.format(user)
        print(user)
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('Covid OR pandemic' + search).get_items()):
            csvWriter.writerow([tweet.date, tweet.content.encode('utf-8'), tweet.id,tweet.user.username, tweet.user.id])


if __name__ == '__main__':
    csvFile = open('twitter_data.csv', 'a')  # creates a file in which you want to store the data.
    csvWriter = csv.writer(csvFile)
    scrape()


