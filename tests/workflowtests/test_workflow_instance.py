import unittest
from pathlib import Path


class TestActivateInstance(unittest.TestCase):
    def setUp(self):
        base_path: Path = Path(__file__).parent.absolute()
