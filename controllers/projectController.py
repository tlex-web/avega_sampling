from models.Projects import Project
from library.Logger import log, LogEnvironment


class ProjectController:
    def __init__(self, client_name, project_year, output_window):
        self.client_name = client_name
        self.project_year = project_year
        self.output_window = output_window
        self.model = Project()
        # Setup signals and slots for project-related actions

    def add_project(self, name, user_id):
        if self.model.create_project(name, user_id):

            self.output_window.show_message("Project added successfully")
        else:
            self.output_window.show_error("Failed to add project")

    def update_project(self, project_id, name, user_id):
        if self.model.update_project(project_id, name, user_id):
            self.output_window.show_message("Project updated successfully")
        else:
            self.output_window.show_error("Failed to update project")

    def delete_project(self, project_id):
        if self.model.delete_project(project_id):
            self.output_window.show_message("Project deleted successfully")
        else:
            self.output_window.show_error("Failed to delete project")
