from fixtures import menu_controller


def test_save(menu_controller, capsys):
    menu_controller.save()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Save"


def test_save_as(menu_controller, capsys):
    menu_controller.save_as()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Save as"


def test_about(menu_controller):
    menu_controller.about()
    menu_controller.about_window.show.assert_called_once()


def test_how_to(menu_controller):
    menu_controller.how_to()
    menu_controller.help_window.show.assert_called_once()
