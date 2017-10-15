import os
from os.path import join, dirname
from dotenv import load_dotenv


def ENV(key):
    """
    keyの環境変数を返す
    @param  key : API_KEY
    @return 環境変数
    """
    dotenv_path = join(dirname(__file__), '../../.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
