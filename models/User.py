from PyQt6.QtSql import QSqlQuery

from utils.Logger import Logger

log = Logger()


class User:

    def create_user(self, username: str):
        """Create a new user in the database

        Args:
            username (str): Username of the new user
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO users (username) VALUES (?)")
        query.addBindValue(username)

        log.info(f"Created user with username: {username}")

        return query.exec()

    def read_user(self, user_id: int):
        """Read a user from the database

        Args:
            user_id (int): User id

        Returns:
            QSqlQuery: Query object
        """

        try:
            query = QSqlQuery()
            query.prepare("SELECT * FROM users WHERE user_id = ?")
            query.addBindValue(user_id)
            query.exec()

            if query.next():

                log.info(f"Read user with id: {user_id}")
                return {
                    "user_id": query.value("user_id"),
                    "username": query.value("username"),
                }

        except Exception as e:
            log.error(f"Error reading user: {e}")
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

        log.info(f"Updated user with id: {user_id}")

        return query.exec()

    def delete_user(self, user_id: int):
        """Delete a user from the database

        Args:
            user_id (int): User id
        """

        query = QSqlQuery()
        query.prepare("DELETE FROM users WHERE user_id = ?")
        query.addBindValue(user_id)

        log.info(f"Deleted user with id: {user_id}")

        return query.exec()
