import json
import csv
import tweepy
import re
import io
import emoji

# Enter your twitter credentials here
consumer_key = "ismfrK5GE7ZR6A7ij5oNosMeN"
consumer_secret = "TfuPmSrso27wrASom3bmgqf6kwKrluWfHeEq2ocqW6ncNCwKlN"
access_token = "1426192239341056002-RjOxzNJ2ck5UvygkakpvPaK4DMXGXz"
access_token_secret = "qHhocJ1SKcOB51MznMpjRshN1VQKS2EB6K3W8aPHfRGAf"


def create_dataset(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    # Twitter authentication and the connection to Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Initializing Tweepy API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Name of csv file to be created
    fname = "57"

    # Open the spreadsheet
    with open('Limpios/%s.csv' % (fname), 'w', encoding="utf-8") as file:
        w = csv.writer(file)

        # Write header row (feature column names of your choice)
        w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'location',
                    'followers_count', 'retweet_count', 'favorite_count'])

        # For each tweet matching hashtag, write relevant info to the spreadsheet
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase + ' -filter:retweets', lang="en",
                                   tweet_mode='extended').items(2000):
            text_tweet = tweet.full_text
            allchars = [str for str in text_tweet]
            emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
            clean_text = ' '.join([str for str in text_tweet.split() if not any(i in str for i in emoji_list)])

            w.writerow([tweet.created_at.date(),
                        clean_text,
                        tweet.user.screen_name.encode('utf-8'),
                        [e['text'] for e in tweet._json['entities']['hashtags']],
                        tweet.user.location,
                        tweet.user.followers_count,
                        tweet.retweet_count,
                        tweet.favorite_count])


# Enter your hashtag here
hashtag_phrase = '"work stress" OR "alcoholism" OR "alcohol" OR "drugs" OR "hopelessness" OR "negativity" OR ' \
                 '"inevitable pain" OR "uncontrollable pain" OR "emotional pain" OR "pain" OR "pessimistic" OR ' \
                 '"pessimism" OR "worry" OR "worrying" OR "afraid" OR "fear" OR "uncertainty" OR "adversity" '
if __name__ == '__main__':
    create_dataset(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
