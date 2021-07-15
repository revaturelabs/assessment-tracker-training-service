from models.codable import Codable


class Trainer(Codable):

    def __init__(self, first_name, last_name, email, role="", id=-1, admin=False):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.admin = admin

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'role': self.role,
            'admin': self.admin
        }

    @staticmethod
    def json_parse(json):
        trainer = Trainer()
        trainer.id = json["id"]
        trainer.email = json["email"]
        trainer.first_name = json["firstName"]
        trainer.last_name = json["lastName"]
        trainer.role = json["role"]
        trainer.admin = json["admin"]

        return trainer
