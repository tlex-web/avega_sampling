import pytest
from unittest.mock import Mock
from controllers.projectController import ProjectController


@pytest.fixture
def output_window():
    return Mock()


@pytest.fixture
def project_controller(output_window):
    return ProjectController("Client", 2022, output_window)


def test_add_project(project_controller):
    project_controller.model.create_project = Mock(return_value=True)
    project_controller.output_window.show_message = Mock()

    project_controller.add_project("Project 1", 1)

    project_controller.model.create_project.assert_called_once_with("Project 1", 1)
    project_controller.output_window.show_message.assert_called_once_with(
        "Project added successfully"
    )


def test_add_project_failure(project_controller):
    project_controller.model.create_project = Mock(return_value=False)
    project_controller.output_window.show_error = Mock()

    project_controller.add_project("Project 1", 1)

    project_controller.model.create_project.assert_called_once_with("Project 1", 1)
    project_controller.output_window.show_error.assert_called_once_with(
        "Failed to add project"
    )


def test_update_project(project_controller):
    project_controller.model.update_project = Mock(return_value=True)
    project_controller.output_window.show_message = Mock()

    project_controller.update_project(1, "Project 1", 1)

    project_controller.model.update_project.assert_called_once_with(1, "Project 1", 1)
    project_controller.output_window.show_message.assert_called_once_with(
        "Project updated successfully"
    )


def test_update_project_failure(project_controller):
    project_controller.model.update_project = Mock(return_value=False)
    project_controller.output_window.show_error = Mock()

    project_controller.update_project(1, "Project 1", 1)

    project_controller.model.update_project.assert_called_once_with(1, "Project 1", 1)
    project_controller.output_window.show_error.assert_called_once_with(
        "Failed to update project"
    )


def test_delete_project(project_controller):
    project_controller.model.delete_project = Mock(return_value=True)
    project_controller.output_window.show_message = Mock()

    project_controller.delete_project(1)

    project_controller.model.delete_project.assert_called_once_with(1)
    project_controller.output_window.show_message.assert_called_once_with(
        "Project deleted successfully"
    )


def test_delete_project_failure(project_controller):
    project_controller.model.delete_project = Mock(return_value=False)
    project_controller.output_window.show_error = Mock()

    project_controller.delete_project(1)

    project_controller.model.delete_project.assert_called_once_with(1)
    project_controller.output_window.show_error.assert_called_once_with(
        "Failed to delete project"
    )
