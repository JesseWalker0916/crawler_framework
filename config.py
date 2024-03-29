import os


class Config(object):
    @staticmethod
    def get_url():
        return os.path.dirname(os.path.realpath(__file__))
