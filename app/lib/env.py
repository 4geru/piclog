import os
from os.path import join, dirname
from dotenv import load_dotenv

class ENV:
    """ 環境変数に関するclass """
    def __init__(key):
        """ keyの環境変数を返す """
        dotenv_path = join(dirname(__file__), '../../.env')
        load_dotenv(dotenv_path)
        return os.environ.get(key)