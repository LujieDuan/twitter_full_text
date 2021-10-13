
from full_text.twitter_client import TwitterClient
from full_text.credential import Credential


class TestTwitterClient:
    def test_get_twitter_by_id_success(self):
        cred = Credential()
        client = TwitterClient(cred)
        response = client.get_twitter_by_id('1309949633959993351')
        assert response.status_code == 200
