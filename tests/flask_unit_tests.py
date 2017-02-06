
import unittest

from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app_initalised(self):
        assert app is not None

    def test_app_default_root(self):
        ret = app.config["SECRET_KEY"]
        assert "test_key" in ret

if __name__ == '__main__':
    unittest.main()