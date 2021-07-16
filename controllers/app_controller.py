from controllers import batch_controller, associate_controller, trainer_controller, note_controller


def route(ans, ins):
    batch_controller.route(ans, ins)
    associate_controller.route(ans, ins)
    trainer_controller.route(ans, ins)
    note_controller.route(ans, ins)
