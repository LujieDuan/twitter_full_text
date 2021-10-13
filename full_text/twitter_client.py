from requests.sessions import Request
from full_text.credential import Credential
from typing import Any, Dict, Optional
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class TwitterClient:
    _BASE_URL = 'https://api.twitter.com/1.1/'
    _AUTH_PATH = 'https://api.twitter.com/oauth2/token'

    def __init__(self, cred: Credential) -> None:
        self._cred = cred
        client = BackendApplicationClient(client_id=cred.consumer_key)
        self._oauth_session = OAuth2Session(client=client)
        self._token = self._oauth_session.fetch_token(
            token_url=self._AUTH_PATH, client_id=cred.consumer_key, client_secret=cred.consumer_secret)

    def get_twitter_by_id(self, id: str, full: bool = False) -> Any:
        response = self._send_request('GET', 'statuses/show.json',
                                      {'id': id, 'tweet_mode': 'extended' if full else 'compact'})
        if response.status_code == 200:
            return response.json()

    def _send_request(self, method: str, path: str, params: Optional[Dict[str, Any]]):
        response = self._oauth_session.request(
            method, self._BASE_URL + path, params=params)
        return response
