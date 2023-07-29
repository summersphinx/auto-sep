import pandas as pd
import os


class Default:
    def __init__(self):
        data = pd.read_json(f'{os.getenv("LOCALAPPDATA")}/XPlus Games/SEP/settings.json', orient='index').to_dict()[0]
        self.id = data['id']
        self.exclude = data['exclude']
        self.filter = data['filter_songs']

