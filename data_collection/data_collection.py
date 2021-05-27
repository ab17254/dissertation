#!/usr/bin/env python3.8
import csv
import sys

import pandas as pd
import snscrape.modules.twitter as sntwitter
import tweepy

from config import TwitterKeys

consumer_key = TwitterKeys.consumer_key
consumer_secret = TwitterKeys.consumer_secret
access_token = TwitterKeys.access_token
access_token_secret = TwitterKeys.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

users = []
user_df = pd.read_csv('ge2017_cand_data.csv')
# user_df = user_df.iloc[668:]
for name in user_df['screenName']:
    users.append(name)

# with open('twitter_users.txt', 'r') as f:
#     accounts = f.read().split('\n')
#     for account in accounts:
#         account = account[1:]
#         users.append(account)
#         f.close()

'''
Can only search 32 hashtags per query - have to create multiple queries and add those to the list below
Election
Labour
Tories
Corbyn
May
Brexit
NHS
Debates
TV/Radio
For the Many
SNP
Manifesto Launch
Register to Vote
Scottish independence referendum 
UKIP
Policies
'''

query_1 = '#GE2017 OR #GE17 OR #GeneralElection OR #GeneralElection2017 OR #Election2017 OR ' \
          + '#VoteLabour OR #Labour OR #ImVotingLabour OR ' \
          + '#Tories OR #Tory OR #conservatives OR #VoteConservative OR #conservative OR ' \
          + '#JC4PM OR #Corbyn OR #JeremyCorbyn OR ' \
          + '#May OR #TheresaMay OR ' \
          + '#Brexit OR ' \
          + '#NHS OR #VoteNHS OR #SaveOurNHS OR ' \
          + '#BBCDebate OR #BattleForNumber10 OR #ITVDebate OR #LeadersDebate OR #MayvCorbyn'

query_2 = '#BBCQT OR #marr OR #Preston OR #r4today OR #NewsNight OR #BBC OR ' \
          + '#ForTheMany OR #ForTheManyNotTheFew OR ' \
          + '#voteSNP OR #SNP' \
          + '#ToryManifesto OR #LabourManifesto OR ' \
          + '#RegistertoVote OR #Vote OR #WhyVote OR #Register2Vote OR ' \
          + '#ScotRef OR #indyref2 OR #Scotland OR ' \
          + '#Manchester OR #Londonattacks OR #LondonBridge OR #London OR ' \
          + '#UKIP OR ' \
          + '#Socialcare'

queries = [query_1, query_2]


def write_tweet(tweet):
    try:
        tweet_data = [tweet.date, tweet.content.encode('utf-8'), tweet.id, tweet.likeCount,
                      tweet.replyCount,
                      tweet.retweetCount, tweet.quoteCount,
                      tweet.user.username, tweet.user.id, tweet.user.followersCount,
                      tweet.user.friendsCount,
                      tweet.user.statusesCount, tweet.user.verified, tweet.user.url, tweet.url]
        if tweet.mentionedUsers is not None:
            tweet_data.append([tweet.mentionedUsers])
        else:
            tweet_data.append(None)
        if tweet.quotedTweet is not None:
            tweet_data.append(tweet.quotedTweet.id)
            tweet_data.append(tweet.quotedTweet.content.encode('utf-8'))
            tweet_data.append(tweet.quotedTweet.user.username)
            tweet_data.append(tweet.quotedTweet.user.id)
            if tweet.quotedTweet.mentionedUsers is not None:
                tweet_data.append([tweet.quotedTweet.mentionedUsers])
            else:
                tweet_data.append(None)
        else:
            tweet_data.append(None)
            tweet_data.append(None)
            tweet_data.append(None)
            tweet_data.append(None)
        return tweet_data
    except UnicodeEncodeError:
        pass


def scrape_from_list():
    for user in users:
        search = ' from:' + '"{}"'.format(user)
        print(user)
        for query in queries:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + search + 'since:2017-04-18 '
                                                                                      'until:2017-06-09').get_items()):
                tweet_data = write_tweet(tweet)
                try:
                    political_writer.writerow(tweet_data)
                except UnicodeEncodeError:
                    pass


def scrape_all():
    for query in queries:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + 'lang:en' + 'since:2017-04-18 '
                                                                                     'until:2017-06-09').get_items()):
            tweet_data = write_tweet(tweet)
            try:
                all_writer.writerow(tweet_data)
            except UnicodeEncodeError:
                pass


if __name__ == '__main__':
    type = sys.argv[1]
    if type == 'pol':
        political_user_file = open('political_twitter_data.csv',
                                   'a')  # creates a file in which you want to store the data.
        political_writer = csv.writer(political_user_file)
        political_writer.writerow(
            ['tweet_date', 'tweet_content', 'tweet_id', 'tweet_likes', 'tweet_replies', 'tweet_retweets',
             'tweet_quotes', 'user_username', 'user_id', 'user_followers', 'user_friends',
             'user_statuses', 'user_verified', 'user_url', 'tweet_url', 'mentioned_users', 'quotedTweet_id',
             'quotedTweet_content', 'quotedTweet_username', 'quotedTweet_userID', 'quotedTweet_mentionedUsers'])
        scrape_from_list()
        print("tweets collected: " + str(len(list(csv.reader(open('political_twitter_data.csv')))) / 2))

    elif type == 'all':
        all_user_file = open('all_twitter_data.csv', 'w')
        all_writer = csv.writer(all_user_file)
        all_writer.writerow(
            ['tweet_date', 'tweet_content', 'tweet_id', 'tweet_likes', 'tweet_replies', 'tweet_retweets',
             'tweet_quotes', 'user_username', 'user_id', 'user_followers', 'user_friends',
             'user_statuses', 'user_verified', 'user_url', 'tweet_url', 'mentioned_users', 'quotedTweet_id',
             'quotedTweet_content', 'quotedTweet_username', 'quotedTweet_userID', 'quotedTweet_mentionedUsers'])
        scrape_all()
        print("tweets collected: " + str(len(list(csv.reader(open('all_twitter_data.csv')))) / 2))

    else:
        print('Enter "pol" or "all" for either political users or all users')
