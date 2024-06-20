# test_with_unittest.py
import unittest
from unittest import TestCase

class TryTesting(unittest.TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    def test_always_fails(self):
        self.assertTrue(False)

