class InvalidDatabaseConnection(Exception):
    def __init__(self, message):
        this.message = message