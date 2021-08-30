#!/usr/bin/env python3.8
# Import libaries
import csv
import sys

import pandas as pd
import snscrape.modules.twitter as sntwitter
import tweepy

from config import TwitterKeys

# Twitter authorization and connection to API
consumer_key = TwitterKeys.consumer_key
consumer_secret = TwitterKeys.consumer_secret
access_token = TwitterKeys.access_token
access_token_secret = TwitterKeys.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Creates user list for when scraping certain users - Uncomment and add file if needed
# users = []
# user_df = pd.read_csv('ge2017_cand_data.csv')
# for name in user_df['screenName']:
#     users.append(name)

# Lists of hashtags to be collected
'''
Can only search 32 hashtags per query - have to create multiple queries and add those to the list below
'''

query_1 = '#GE2019 OR #GE19 OR #GeneralElection OR #GeneralElection2019 OR #Election2019 OR ' \
          + '#VoteLabour OR #Labour OR #ImVotingLabour OR ' \
          + '#Tories OR #Tory OR #conservatives OR #VoteConservative OR #conservatives OR' \
          + '#JC4PM OR #Corbyn OR #JeremyCorbyn OR' \
          + '#borisjohnson OR #Brexit OR' \
          + '#NHS OR #VoteNHS OR #SaveOurNHS OR ' \
          + '#BBCDebate OR #BattleForNumber10 OR #ITVDebate OR #LeadersDebate'

query_2 = '#BBCQT OR #marr OR #Preston OR #r4today OR #NewsNight OR #BBC OR ' \
          + '#ForTheMany OR #ForTheManyNotTheFew OR ' \
          + '#voteSNP OR #SNP' \
          + '#ToryManifesto OR #LabourManifesto OR ' \
          + '#RegistertoVote OR #Vote OR #WhyVote OR #Register2Vote OR '

# Merges the two queries so a larger search can be performed
queries = [query_1, query_2]


def write_tweet(tweet):
    """
    Function to form tweet data to an list, for the line to be written in the csv file. Called in scrape_all and scrape_from_list
    :param tweet: (object)
    :return tweet_data (list): list of values from tweet
    """
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

''' Used in scraping specific users
def scrape_from_list():
    """
    Calls sntwitter library to scrape tweets using the formed query. Only scrapes users whose username appear in user list
    """
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
'''

def scrape_all():
    """
    Calls sntwitter library to scrape tweets using the formed query.
    """
    for query in queries:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + 'lang:en' + 'since:2019-11-06 '
                                                                                     'until:2019-12-13').get_items()):
            tweet_data = write_tweet(tweet)
            try:
                all_writer.writerow(tweet_data)
            except UnicodeEncodeError:
                pass


if __name__ == '__main__':
    type = sys.argv[1]
    # Parameter either 'pol' or 'all'. Pol will call scrape_from_list(). all will call scrape_all()
    if type == 'pol':
        political_user_file = open('political_twitter_data.csv',
                                   'a')  # creates a file in which you want to store the data.
        political_writer = csv.writer(political_user_file)
        # Header row
        political_writer.writerow(
            ['tweet_date', 'tweet_content', 'tweet_id', 'tweet_likes', 'tweet_replies', 'tweet_retweets',
             'tweet_quotes', 'user_username', 'user_id', 'user_followers', 'user_friends',
             'user_statuses', 'user_verified', 'user_url', 'tweet_url', 'mentioned_users', 'quotedTweet_id',
             'quotedTweet_content', 'quotedTweet_username', 'quotedTweet_userID', 'quotedTweet_mentionedUsers'])
        scrape_from_list()
        # Prints the total number of tweets collected - divided by 2 due to newline in file
        print("tweets collected: " + str(len(list(csv.reader(open('political_twitter_data.csv')))) / 2))

    elif type == 'all':
        all_user_file = open('2019_all_twitter_data.csv', 'w')
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
