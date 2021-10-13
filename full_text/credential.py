import configparser


class Credential:

    def __init__(self, path: str = 'credentials/twitter_api_keys.ini', section: str = 'DEFAULT') -> None:
        cred = configparser.ConfigParser()
        cred.read(path)
        values = cred[section]
        self.consumer_key = values['consumer_key']
        self.consumer_secret = values['consumer_secret']
