from PyQt6.QtSql import QSqlQuery


class Project:

    def create_project(self, name: str, user_id: int) -> bool:
        """Create a new project in the database

        Args:
            name (str): Name of the project
            user_id (int): User id
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO projects (project_name, user_id) VALUES (?, ?)")
        query.addBindValue(name)
        query.addBindValue(user_id)

        return query.exec()

    def update_project(self, name: str, project_id: int) -> bool:
        """Update a project in the database

        Args:
            name (str): New project name
            project_id (int): Project id
        """

        query = QSqlQuery()
        query.prepare("UPDATE projects SET project_name = ? WHERE id = ?")
        query.addBindValue(name)
        query.addBindValue(project_id)

        return query.exec()

    def delete_project(self, project_id: int) -> bool:
        """Delete a project from the database

        Args:
            project_id (int): Project id
        """

        query = QSqlQuery()
        query.prepare("DELETE FROM projects WHERE id = ?")
        query.addBindValue(project_id)

        return query.exec()

    def get_project(self, project_id: int) -> dict | None:
        """Get a project from the database

        Args:
            project_id (int): Project id
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM projects WHERE id = ?")
        query.addBindValue(project_id)

        if query.next():
            record = query.record()
            return {
                "id": record.value("id"),
                "project_name": record.value("project_name"),
                "user_id": record.value("user_id"),
            }

        return None
