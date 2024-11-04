from PyQt6.QtSql import QSqlQuery


class Session:
    """
    Represents a session in the database.
    """

    def create_session(
        self,
        user_id: int,
    ) -> bool:
        """Create a new session in the database

        Args:
            user_id (int): User id

        Returns:
            bool: True if the session is created successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO user_sessions (user_id) VALUES (?)")
        query.addBindValue(user_id)

        return query.exec()

    def delete_session(self, user_id: int) -> bool:
        """Delete a session from the database

        Args:
            user_id (int): User id

        Returns:
            bool: True if the session is deleted successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare("DELETE FROM user_sessions WHERE user_id = ?")
        query.addBindValue(user_id)

        return query.exec()

    def get_session(self, user_id: int) -> dict[str, str] | None:
        """Get a session from the database

        Args:
            user_id (int): user id

        Returns:
            dict[str, int] | None: A dictionary containing the session data if the session exists, an empty dictionary otherwise.
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM user_sessions WHERE user_id = ?")
        query.addBindValue(user_id)
        query.exec()

        if query.next():
            return {
                "session_id": query.value("session_id"),
                "user_id": query.value("user_id"),
            }

        return None
