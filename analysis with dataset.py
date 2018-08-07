import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob



def main():
    tweet_file = open("RobertMugabe_2017-04-20_to_2017-04-26.json")

    tweet_data = []
    for line in tweet_file:
        response = json.loads(line)
        '''if "lang" in response.keys():
            print response["lang"]'''
        if "text" in response.keys():
            tweet_data.append(response["text"])


    print("Total tweets : {} ".format(len(tweet_data)))

    ptweets = [tweet for tweet in tweet_data if TextBlob(tweet).sentiment.polarity > 0]
    print("Number of Positive tweets : {} ".format(len(ptweets)))
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweet_data)))

    ntweets = [tweet for tweet in tweet_data if TextBlob(tweet).sentiment.polarity < 0]
    print("Number of Negative tweets : {} ".format(len(ntweets)))
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweet_data)))

    neutweets = [tweet for tweet in tweet_data if TextBlob(tweet).sentiment.polarity == 0]
    print("Number of Neutral tweets : {} ".format(len(neutweets)))
    print("Neutral tweets percentage: {} %".format(100*len(neutweets)/len(tweet_data)))

    objects = ('Negative', 'Positive', 'Neutral')
    y_pos = np.arange(len(objects))
    performance = [len(ntweets),len(ptweets),len(neutweets)]

    plt.bar(y_pos, performance, align='center',color = '#a020f0', alpha=0.5, width=0.4, linewidth=0)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of tweets')
    plt.title('Zimbabwe Political Comments')

    plt.show()

if __name__ == "__main__":
    main()
