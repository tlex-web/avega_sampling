from PyQt6.QtSql import QSqlQuery

from library.Logger import log, LogEnvironment


class User:
    """Represents a user in the system."""

    def create_user(self, username: str):
        """Create a new user in the database

        Args:
            username (str): Username of the new user

        Returns:

        """

        query = QSqlQuery()
        query.prepare("INSERT INTO users (username) VALUES (?)")
        query.addBindValue(username)

        if query.exec():
            log.info(f"Created user with username: {username}", LogEnvironment.MODELS)
            return query.lastInsertId()
        else:
            log.error(
                f"Failed to create user: {query.lastError().text()}",
                LogEnvironment.MODELS,
            )
            return None

    def read_user_id(self, user_id: int):
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

                log.info(f"Read user with id: {user_id}", LogEnvironment.MODELS)
                return {
                    "user_id": query.value("user_id"),
                    "username": query.value("username"),
                }

        except Exception as e:
            log.error(f"Error reading user: {e}", LogEnvironment.MODELS)
            return None

    def read_user_username(self, username: str):
        """Read a user from the database

        Args:
            username (str): Username

        Returns:
            QSqlQuery: Query object
        """

        try:
            query = QSqlQuery()
            query.prepare("SELECT * FROM users WHERE username = ?")
            query.addBindValue(username)
            query.exec()

            if query.next():

                log.info(f"Read user with username: {username}", LogEnvironment.MODELS)
                return {
                    "user_id": query.value("user_id"),
                    "username": query.value("username"),
                }
            else:
                log.error(
                    f"User with username: {username} not found", LogEnvironment.MODELS
                )

        except Exception as e:
            log.error(f"Error reading user: {e}", LogEnvironment.MODELS)
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

        log.info(f"Updated user with id: {user_id}", LogEnvironment.MODELS)

        return query.exec()

    def delete_user(self, user_id: int):
        """Delete a user from the database

        Args:
            user_id (int): User id
        """

        query = QSqlQuery()
        query.prepare("DELETE FROM users WHERE user_id = ?")
        query.addBindValue(user_id)

        log.info(f"Deleted user with id: {user_id}", LogEnvironment.MODELS)

        return query.exec()
