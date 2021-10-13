from full_text.tweet_archive import TweetArchive
from full_text.credential import Credential
from full_text.twitter_client import TwitterClient
import requests
from requests.exceptions import ConnectionError
from http import HTTPStatus
import re
import pandas


class GetFullText:
    _T_CO_SHORTENED_LINK_PATTERN = r'https:\/\/t\.co\/[a-zA-Z0-9]*$'
    _TWEET_LINK_PATTERN = r'^https:\/\/twitter\.com\/i\/web\/status\/([0-9]*)$'

    def __init__(self, client: TwitterClient) -> None:
        self._client = client

    def update_tweet(self, tweet_row: pandas.Series) -> None:
        shortened_link = self.extract_shortened_link(tweet_row['value'])
        if shortened_link is not None:
            destination = self.get_redirected_link(shortened_link)
            if destination is not None:
                shortened_tweet_id = self.get_twitter_id(destination)
                if shortened_tweet_id is not None and shortened_tweet_id == tweet_row['tweetId']:
                    full_text = self.get_full_twitter_text(shortened_tweet_id)
                    return full_text
        return tweet_row['value']

    def get_full_twitter_text(self, id: str) -> str:
        tweet = self._client.get_twitter_by_id(id, True)
        if tweet is not None and 'full_text' in tweet:
            return tweet['full_text']

    def is_twitter_link(self, link: str):
        return re.match(self._TWEET_LINK_PATTERN, link) is not None

    def get_twitter_id(self, link: str):
        if self.is_twitter_link(link):
            return re.match(self._TWEET_LINK_PATTERN, link).group(1)

    def get_redirected_link(self, short_link: str):
        try:
            rsp = requests.get(short_link)
            if rsp.status_code == HTTPStatus.OK:
                return rsp.url
        except ConnectionError:
            print('Failed to connect to link: %s' % short_link)

    def extract_shortened_link(self, tweet: str):
        matchs = re.findall(self._T_CO_SHORTENED_LINK_PATTERN, tweet)
        if matchs:
            return matchs[0]


if __name__ == '__main__':
    client = TwitterClient(Credential())
    gft = GetFullText(client)
    tweet_archive = TweetArchive('./data/tweets/2.csv', './output/tweets/')
    tweet_archive.create_column('full_text', gft.update_tweet)
    tweet_archive.write()
