import json
import random

from core.analyzer import trains


def load_settings():
    with open('settings.json', 'r') as read_file:
        return json.load(read_file)


def load_train_ids(settings):
    train_ids = settings['train_ids']
    random.shuffle(train_ids)
    return train_ids


def load_trains(crawler_settings):
    return trains.SetOfTrains.from_file(crawler_settings['train_data_file_path'])
