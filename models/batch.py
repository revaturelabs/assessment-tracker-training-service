import unittest
from datetime import datetime
from math import floor

from models.codable import Codable


class Batch(Codable):

    def __init__(self,
                 name,
                 training_track,
                 start_date,
                 end_date,
                 id=-1):
        self.id = id
        self.name = name
        self.training_track = training_track
        self.start_date = start_date
        self.end_date = end_date

    def json(self):
        return {
            'id': self.id,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'name': self.name,
            'trainingTrack': self.training_track,
            'currentWeek': self.current_week(),
            'totalWeeks': self.total_weeks()
        }

    @staticmethod
    def json_parse(json):
        batch = Batch()
        batch.id = json["batchId"]
        batch.start_date = json["startDate"]
        batch.end_date = json["endDate"]
        batch.name = json["name"]
        batch.training_track = json["trainingTrack"]
        return batch

    def current_week(self):
        """Returns the current week of training(today - start_date)"""
        return floor(abs((datetime.now().date() - datetime.fromtimestamp(self.start_date).date()).days / 7))

    def total_weeks(self):
        """Returns the total weeks of training(end_date - start_date)"""
        return floor(abs((datetime.fromtimestamp(self.end_date).date() - datetime.fromtimestamp(
            self.start_date).date()).days / 7))


