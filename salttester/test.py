from unittest import TestCase
from salttester.deploy import main

class TestConsole(TestCase):
    def test_basic(self):
        main()
