from configparser import ConfigParser, NoSectionError
from exceptions.invalid_database_connection import InvalidDatabaseConnection
from psycopg2 import connect


class Connection():
    def load_conn():
        conn_file = "conn_cred.ini"
        section = "postgresql"
        parser = ConfigParser()
        db = {}

        try:
            with open(conn_file, "r") as f:
                parser.read_file(f)
        except FileNotFoundError:
            raise InvalidDatabaseConnection(
                f"{conn_file} is missing from application root.")

        try:
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        except NoSectionError:
            raise InvalidDatabaseConnection(
                f"{conn_file} missing {section} section.")

        return db

    conn = connect(**load_conn())


if __name__ == "__main__":
    Connection()
