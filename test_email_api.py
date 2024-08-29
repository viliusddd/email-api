import pytest

from email_api import gen_email_body, validate_email_addr


def test_get_email_body():
    assert gen_email_body('see you soon') == \
        '\nHello,\n\ngive me a call, see you soon.\n\nThanks,\nV.'


def test_validate_email_addr():
    assert validate_email_addr('vilius@gmail.com') is True
    assert validate_email_addr('vilius@gmail..com') is None
    assert validate_email_addr('vilius#@gmail.com') is None
    assert validate_email_addr('vilius#@gmail. com') is None

    with pytest.raises(TypeError):
        validate_email_addr(12345)
