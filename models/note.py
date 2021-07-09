from models.codable import Codable


class Note(Codable):
    def __init__(self, note_id: int, batch_id: int, associate_id: int, week_number: int, content: str):
        self.note_id = note_id
        self.batch_id = batch_id
        self.associate_id = associate_id
        self.week_number = week_number
        self.content = content

    @staticmethod
    def json_parse(json):
        to_return = Note(0, 0, 0, 0, '')
        to_return.note_id = json['id']
        to_return.batch_id = json['batchId']
        to_return.associate_id = json['associateId']
        to_return.week_number = json['weekNumber']
        to_return.content = json['cont']
        return to_return

    def json(self):
        json = {}
        json['id'] = self.note_id
        json['batchId'] = self.batch_id
        json['associateId'] = self.associate_id
        json['weekNumber'] = self.week_number
        json['cont'] = self.content
        return json

    def __str__(self):
        return f'note_id {self.note_id}, batch_id: {self.batch_id}, associate_id: {self.associate_id}, week_number: {self.week_number}, content: {self.content}'