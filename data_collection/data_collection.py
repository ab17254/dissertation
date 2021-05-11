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

query = '#GE2017 OR #GE17 OR #GeneralElection OR #GeneralElection2017 OR #Election2017'


def scrape():
    for user in users:
        search = ' from:' + '"{}"'.format(user)
        print(user)
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + search + 'since:2017-05-04 '
                                                                                  'until:2017-06-04').get_items()):
            csvWriter.writerow([tweet.date, tweet.content.encode('utf-8'), tweet.id, tweet.likeCount, tweet.replyCount,
                                tweet.retweetCount, tweet.quoteCount, tweet.user.username, tweet.user.id,
                                tweet.user.followersCount, tweet.user.friendsCount, tweet.user.statusesCount,
                                tweet.user.verified])


if __name__ == '__main__':
    csvFile = open('twitter_data.csv', 'a')  # creates a file in which you want to store the data.
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['tweet_date', 'tweet_content', 'tweet_id', 'tweet_likes', 'tweet_replies', 'tweet_retweets',
                        'tweet_quotes', 'user_username', 'user_id', 'user_followers', 'user_friends', 'user_statuses',
                        'user_verified'])
    scrape()
    print("tweets collected: " + str(len(list(csv.reader(open('twitter_data.csv')))) / 2))
