from PyQt6.QtSql import QSqlQuery


class Seed:
    """Represents a seed in the database."""

    def create_seed(self, seed_value: int, user_id: int) -> bool:
        """Create a new seed in the database.

        Args:
            seed_value (int): Seed value.
            user_id (int): user id.

        Returns:
            bool: True if the seed is created successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO seeds (seed_value, user_id) VALUES (?, ?)")
        query.addBindValue(seed_value)
        query.addBindValue(user_id)

        return query.exec()

    def read_seed(self, user_id: int) -> dict | None:
        """Get a seed from the database.

        Args:
            seed_id (int): Seed id.

        Returns:
            dict | None: A dictionary containing the seed information if found, None otherwise.
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM seeds WHERE user_id = ?")
        query.addBindValue(user_id)
        query.exec()

        if query.next():
            return {
                "seed_value": query.value("seed_value"),
                "user_id": query.value("user_id"),
            }

        return None
