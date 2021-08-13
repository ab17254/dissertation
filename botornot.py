# Import libaries
import botometer
import pandas as pd
import tweepy
from tweepy import OAuthHandler

from config import TwitterKeys, RapidApiKey

# Twitter authorization and connection to API
consumer_key = TwitterKeys.consumer_key
consumer_secret = TwitterKeys.consumer_secret
access_token = TwitterKeys.access_token
access_token_secret = TwitterKeys.access_token_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret,
}

# Connected to RapidAPI and the botometer API
rapidapi_key = RapidApiKey.rapidapi_key

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Reads file containg tweets
df = pd.read_csv('all_2019.csv')

results_score = []
results_name = []

# Creates an list of users to be parsed through the API
user_freq = df['quotedTweet_username'].value_counts()
user_list = []
for user in user_freq.index:
    user_list.append(user)

# Parses users through API. Returns their name and score as an list.
for screen_name, result in bom.check_accounts_in(user_list):
    try:
        name = result['user']['user_data']['screen_name']
        # Using raw_score as so the value is between 0 and 1 to assist in analysis
        score = result['raw_scores']['english']['overall']
        results_name.append(name)
        results_score.append(score)
        print(score, name)
    except KeyError:
        pass

# Parses the score and name list to an Pandas DataFrame and saves as an CSV file
bot_score_df = pd.DataFrame(list(zip(results_name, results_score)), columns=['result_name', 'result_score'])
bot_score_df.to_csv('bot_score.csv')
