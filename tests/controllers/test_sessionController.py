from controllers.sessionController import SessionController


def test_init_session():
    controller = SessionController()
    user_id = controller.init_session()
    assert isinstance(user_id, int)
