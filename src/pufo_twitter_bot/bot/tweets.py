"""Download all historical tweets from PUFO BOT."""

import csv
import datetime
import json
from pathlib import Path

import tweepy

from pufo_twitter_bot.bot.twitter import TwitterBot


def get_tweets(client, username: str = "BotPufo"):
    """Pulls 3,200 most recent tweets for specified username and saves to file."""
    # client = tweepy.Client(TWITTER_BEARER_TOKEN)
    user_id = client.client.get_user(username=username).data.id
    responses = tweepy.Paginator(
        client.client.get_users_tweets, user_id, max_results=100, limit=100
    )
    tweets_list = [["link", "username" "tweet"]]
    currentime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    counter = 0
    for response in responses:
        counter += 1
        try:
            for tweet in response.data:
                tweets_list.append(
                    [
                        f"https://twitter.com/anyuser/status/{tweet.id}",
                        username,
                        tweet.text,
                    ]
                )
        except Exception as e:
            print(e)

    fname = f"tweets_{username}_{currentime}.csv"
    fpath = Path("data") / fname

    with open(fpath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(tweets_list)

    print("Done!")


def get_all_tweets(client, username="BotPufo"):
    """Download recent tweets by username."""
    # Initialize a list to hold all the tweepy Tweets
    alltweets = []

    # Make initial request for most recent tweets (200 is the maximum allowed count)
    # timeline_tweets = client.client.get_users_tweets(id=username)

    new_tweets = client.user_timeline(
        username=username, count=200, tweet_mode="extended"
    )

    # Save most recent tweets
    alltweets.extend(new_tweets)

    # Save the id of the oldest tweet less one to keep fetching older tweets
    oldest = alltweets[-1].id - 1

    # Keep fetching tweets until there are no tweets left
    while len(new_tweets) > 0:
        print(f"Getting tweets before {oldest}")

        # All subsequent requests use the max_id param to prevent duplicates
        new_tweets = client.user_timeline(
            username=username, count=200, max_id=oldest, tweet_mode="extended"
        )

        # Save most recent tweets
        alltweets.extend(new_tweets)

        # Update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")

    # Transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [
        [tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")]
        for tweet in alltweets
    ]

    fname = f"tweets_{username}.json"
    fpath = Path("data") / fname

    # Write the json
    with open(fpath, "w") as f:
        json.dump(outtweets, f, indent=4)

    print("Saved all tweets to file.")


if __name__ == "__main__":
    twb = TwitterBot(tweet="Test")  # "Test" as placeholder to initialize twb
    get_tweets(client=twb)
