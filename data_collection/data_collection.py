#!/usr/bin/env python3.8
import csv
import sys
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


def scrape_from_list():
    for user in users:
        search = ' from:' + '"{}"'.format(user)
        print(user)
        for query in queries:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + search + 'since:2017-04-18 '
                                                                                      'until:2017-06-09').get_items()):
                political_writer.writerow(
                    [tweet.date, tweet.content.encode('utf-8'), tweet.id, tweet.likeCount, tweet.replyCount,
                     tweet.retweetCount, tweet.quoteCount, tweet.user.username, tweet.user.id,
                     tweet.user.followersCount, tweet.user.friendsCount, tweet.user.statusesCount,
                     tweet.user.verified])


def scrape_all():
    for query in queries:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + 'lang:en' + 'since:2017-04-18 '
                                                                                     'until:2017-06-09').get_items()):
            all_writer.writerow(
                [tweet.date, tweet.content.encode('utf-8'), tweet.id, tweet.likeCount, tweet.replyCount,
                 tweet.retweetCount, tweet.quoteCount, tweet.user.username, tweet.user.id,
                 tweet.user.followersCount, tweet.user.friendsCount, tweet.user.statusesCount,
                 tweet.user.verified])


if __name__ == '__main__':
    type = sys.argv[1]
    if type == 'pol':
        political_user_file = open('political_twitter_data.csv',
                                   'w')  # creates a file in which you want to store the data.
        political_writer = csv.writer(political_user_file)
        political_writer.writerow(
            ['tweet_date', 'tweet_content', 'tweet_id', 'tweet_likes', 'tweet_replies', 'tweet_retweets',
             'tweet_quotes', 'user_username', 'user_id', 'user_followers', 'user_friends', 'user_statuses',
             'user_verified'])
        scrape_from_list()
        print("tweets collected: " + str(len(list(csv.reader(open('political_twitter_data.csv')))) / 2))

    elif type == 'all':
        all_user_file = open('all_twitter_data.csv', 'w')
        all_writer = csv.writer(all_user_file)
        all_writer.writerow(
            ['tweet_date', 'tweet_content', 'tweet_id', 'tweet_likes', 'tweet_replies', 'tweet_retweets',
             'tweet_quotes', 'user_username', 'user_id', 'user_followers', 'user_friends', 'user_statuses',
             'user_verified'])
        scrape_all()
        print("tweets collected: " + str(len(list(csv.reader(open('all_twitter_data.csv')))) / 2))

    else:
        print('Enter "pol" or "all" for either political users or all users')
