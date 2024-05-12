from pyutilkit.classes import Singleton


def test_singleton() -> None:
    class A(metaclass=Singleton):
        pass

    assert A() is A()
