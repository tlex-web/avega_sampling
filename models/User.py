from PyQt6.QtSql import QSqlQuery


class User:

    def create_user(self, username: str):
        """Create a new user in the database

        Args:
            username (str): Username of the new user
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO users (username) VALUES (?)")
        query.addBindValue(username)

        return query.exec()

    def read_user(self, user_id: int):
        """Read a user from the database

        Args:
            user_id (int): User id

        Returns:
            QSqlQuery: Query object
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE user_id = ?")
        query.addBindValue(user_id)

        if query.next():
            record = query.record()
            return {
                "user_id": record.value("user_id"),
                "username": record.value("username"),
            }

        return None

    def update_user(self, user_id: int, username: str):
        """Update a user in the database

        Args:
            user_id (int): User id
            username (str): New username
        """

        query = QSqlQuery()
        query.prepare("UPDATE users SET username = ? WHERE user_id = ?")
        query.addBindValue(username)
        query.addBindValue(user_id)

        return query.exec()

    def delete_user(self, user_id: int):
        """Delete a user from the database

        Args:
            user_id (int): User id
        """

        query = QSqlQuery()
        query.prepare("DELETE FROM users WHERE user_id = ?")
        query.addBindValue(user_id)

        return query.exec()
