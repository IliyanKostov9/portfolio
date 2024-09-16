import unittest

from mockito import mock, verify

from src.dummy_src import dummy_fun


class DummyTest(unittest.TestCase):
    def test_issue_hello(self):

        out = mock()
        dummy_fun(out)

        verify(out).write("Hello")
