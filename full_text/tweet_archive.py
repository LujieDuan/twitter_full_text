import pandas
import os
from typing import Callable


class TweetArchive:
    _CSV_HEADER = ['user', 'userId', 'userLocation', 'place', 'latitude', 'longitude', 'timeCreated',
                   'tweetId', 'isRetweet', 'approximatedFavoriteCount', 'tweetLanguage', 'isUserGeoLocationEnabled', 'value']
    _tweets = None

    def __init__(self, path: str, out_dir: str) -> None:
        self._path = path
        self._out_dir = out_dir
        self._out_path = self._get_out_path(path, out_dir)
        self._tweets = pandas.read_csv(
            self._path, names=self._CSV_HEADER, dtype=str)

    def create_column(self, name: str, func: Callable[[pandas.Series], str]) -> None:
        self._tweets['name'] = self._tweets.apply(
            lambda row: func(row), axis=1)

    def write(self) -> None:
        if not os.path.exists(self._out_dir):
            os.makedirs(self._out_dir)
        self._tweets.to_csv(self._out_path, header=False, index=True)

    def _get_out_path(self, path: str, out_dir: str) -> str:
        file_name = os.path.basename(path)
        return os.path.join(out_dir, file_name)
