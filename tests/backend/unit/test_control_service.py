from function.backend.services.control_service import ControlService


def test_should_activate_switch_logic():
    cs = ControlService()
    cs.set_mode("auto")
    assert cs.should_activate_switch(15, 10) is True
    assert cs.should_activate_switch(22, 10) is True
    assert cs.should_activate_switch(22, 30) is False
