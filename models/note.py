from models.codable import Codable


class Note(Codable):
    def __init__(self, note_id: int, batch_id: int, trainee_id: int, week_number: int, content: str):
        self.note_id = note_id
        self.batch_id = batch_id
        self.trainee_id = trainee_id
        self.week_number = week_number
        self.content = content

    @staticmethod
    def json_parse(json):
        to_return = Note(0, 0, 0, 0, '')
        to_return.note_id = json['noteId']
        to_return.batch_id = json['batchId']
        to_return.trainee_id = json['traineeId']
        to_return.week_number = json['weekNumber']
        to_return.content = json['content']

    def json(self):
        json = {}
        json['noteId'] = self.note_id
        json['batchId'] = self.batch_id
        json['traineeId'] = self.trainee_id
        json['weekNumber'] = self.week_number
        json['content'] = self.content