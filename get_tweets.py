# -*- coding: utf-8 -*-
import tweepy
import csv
import re


def get_all_tweets(screen_name):
    all_tweets = []
    new_tweets = []
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_key, twitter_access_secret)
    client = tweepy.API(auth)
    new_tweets = client.user_timeline(screen_name=screen_name, count=200)
    while len(new_tweets) > 0:
        for tweet in new_tweets:
            all_tweets.append(tweet.text.encode("utf-8"))
        print("We've got %s tweets so far" % (len(all_tweets)))
        max_id = new_tweets[-1].id - 1
        new_tweets = client.user_timeline(screen_name=screen_name,
                                          count=200, max_id=max_id)
    return all_tweets


def clean_tweet(tweet):
    tweet = re.sub("https?\:\/\/", "", tweet)  # links
    tweet = re.sub("#\S+", "", tweet)  # hashtags
    tweet = re.sub("\.?@", "", tweet)  # at mentions
    tweet = re.sub("RT.+", "", tweet)  # Retweets
    tweet = re.sub("Video\:", "", tweet)  # Videos
    tweet = re.sub("\n", "", tweet)  # new lines
    tweet = re.sub("^\.\s.", "", tweet)  # leading whitespace
    tweet = re.sub("\s+", " ", tweet)  # extra whitespace
    tweet = re.sub("&amp;", "and", tweet)  # encoded ampersands
    return tweet


def remove_emoji(tweet):
    """
    去除表情
    :param tweet:
    :return:
    """
    if not tweet:
        return tweet
    if not isinstance(tweet, basestring):
        return tweet
    try:
        # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        # UCS-2
        patt = re.compile(
            u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', tweet)


def write_tweets_to_csv(tweets):
    with open('tweets.csv', 'wb') as f:
        writer = csv.writer(f)
        for tweet in tweets:
            tweet = clean_tweet(tweet)
            tweet = remove_emoji(tweet)
            if tweet:
                writer.writerow([tweet])


if __name__ == "__main__":
    tweets = get_all_tweets("springcoil")
    write_tweets_to_csv(tweets)
