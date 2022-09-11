from mysql import connector


class ConnectionDB:
    def __init__(self):
        config = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "port": "3306",
            "database": "Music"
        }
        self.connection = connector.connect(**config)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
    
    def _execute(self, sql: str, fetch_one: bool) -> list | None:
        self.cursor.execute(sql)
        response = self.cursor.fetchone() if fetch_one else self.cursor.fetchmany()
        self.cursor.reset()
        return response
    
    def select(self, table: str, key: str, where: str, fetch_one: bool) -> list:
        return self._execute(f"SELECT * FROM {table} WHERE {key} = '{where}'", fetch_one)
    
    def insert(self, table: str, keys: list[str], values: list[str], fetch_one: bool):
        values = [value.replace("'", "\\'") for value in values]
        self._execute(f"INSERT INTO {table} (\'{'\', \''.join([key for key in keys])}\') "
                      + f"VALUES (\'{'\', \''.join([value for value in values])}\')", fetch_one)
 