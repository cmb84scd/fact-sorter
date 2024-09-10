from eventbus_learning.eb import addition


def test_addition():
    assert addition(2, 3) == 5
