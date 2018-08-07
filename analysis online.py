import re
import tweepy
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):

    def __init__(self):

        consumer_key = "lXdRI0gmOULb4qWJdD9CsNfsZ"
        consumer_secret = "4EBMS8XqYtpsmwWzBVwC75oAkAg6bZ9CIQ9BEZvG9GmMHGXDtW"
        access_token = "730398591345430529-efFbEKtISCtoCOJm0iAIPkhLr3nZjre"
        access_token_secret = "3k8jlAX95lc5bPpMTjo43fVoeRPqUgfrykY6J50rT6R8m"

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):

        # Utility function to clean tweet text by removing links, special characters using simple regex statements.

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        # Utility function to classify sentiment of passed tweet using textblob's sentiment method

        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):

        # Main function to fetch tweets and parse them.

        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def main():
    api = TwitterClient()
    tweets = api.get_tweets(query = 'Robert Mugabe', count = 200)

    print("Total tweets : {} ".format(len(tweets)))

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Number of Positive tweets : {} ".format(len(ptweets)))
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Number of Negative tweets : {} ".format(len(ntweets)))
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    print("Neutral of Negative tweets : {} ".format(len(neutweets)))
    print("Neutral tweets percentage: {} %".format(100*len(neutweets)/len(tweets)))

    #print("Number of Neutral tweets : {} ".format(len(tweets)-(len(ptweets)+len(ntweets))))
    #print("Neutral tweets percentage: {} % ".format(100 - ((100*len(ntweets)/len(tweets))+(100*len(ptweets)/len(tweets)))))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNeutral tweets:")
    for tweet in neutweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    objects = ('Negative', 'Positive', 'Neutral')
    y_pos = np.arange(len(objects))
    performance = [len(ntweets),len(ptweets),len(tweets)-(len(ntweets) + len(ptweets))]

    plt.bar(y_pos, performance, align='center',color = '#a020f0', alpha=0.5, width=0.4, linewidth=0)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of tweets')
    plt.title('Zimbabwe Political Comments')

    plt.show()

if __name__ == "__main__":
    main()
