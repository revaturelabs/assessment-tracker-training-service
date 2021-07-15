from flask_cors import CORS
from controllers import batch_controller, associate_controller, trainer_controller, note_controller


def route(api):
    batch_controller.route(api)
    associate_controller.route(api)
    trainer_controller.route(api)
    note_controller.route(api)
