from PyQt6.QtSql import QSqlQuery


class Seed:

    def create_seed(self, seed_value: str, project_id: int) -> bool:
        """Create a new seed in the database

        Args:
            seed_value (str): Seed value
            project_id (int): Project id
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO seeds (seed_value, project_id) VALUES (?, ?)")
        query.addBindValue(seed_value)
        query.addBindValue(project_id)

        return query.exec()

    def get_seed(self, seed_id: int) -> dict | None:
        """Get a seed from the database

        Args:
            seed_id (int): Seed id
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM seeds WHERE id = ?")
        query.addBindValue(seed_id)

        if query.next():
            record = query.record()
            return {
                "id": record.value("id"),
                "seed_value": record.value("seed_value"),
                "project_id": record.value("project_id"),
            }

        return None
