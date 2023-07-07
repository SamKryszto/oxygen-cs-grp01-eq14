import unittest
from unittest.mock import patch, MagicMock, ANY
from src.main import Main, Event


# pylint: disable=protected-access
class TestMain(unittest.TestCase):
    def test_env_all_setted(self):
        main = Main()
        self.assertNotEqual(main.HOST, None)
        self.assertNotEqual(main.TOKEN, None)
        self.assertNotEqual(main.TICKETS, None)
        self.assertNotEqual(main.T_MAX, None)
        self.assertNotEqual(main.T_MIN, None)
        self.assertNotEqual(main.DATABASE, None)

    @patch.dict(
        "src.main.os.environ",
        {"TOKEN": "TOKEN"},
        clear=True,
    )
    def test_env_default_values(self):
        main = Main()
        self.assertEqual(main.HOST, "http://34.95.34.5")
        self.assertEqual(main.TICKETS, 100)
        self.assertEqual(main.T_MAX, 30)
        self.assertEqual(main.T_MIN, 10)

    @patch.dict(
        "src.main.os.environ",
        {},
        clear=True,
    )
    def test_env_no_token(self):
        with self.assertRaises(Exception) as cm:
            main = Main()
        self.assertEqual("No token defined", str(cm.exception))

    @patch.dict(
        "src.main.os.environ",
        {"TOKEN": "TOKEN"},
        clear=True,
    )
    def test_send_event_to_database_valid_input(self):
        session = MagicMock()
        main = Main()
        main._session = session
        main.send_event_to_database("timestamp", "event")
        session.add.assert_called_once()
        # call_args[0][0] is first parameter of first call
        self.assertIsInstance(session.add.call_args[0][0], Event)
        self.assertEqual(session.add.call_args[0][0].timestamp, "timestamp")
        self.assertEqual(session.add.call_args[0][0].event, "event")
        session.commit.assert_called_once()

    @patch.dict(
        "src.main.os.environ",
        {"TOKEN": "TOKEN"},
        clear=True,
    )
    def test_send_event_to_database_with_exception(self):
        session = MagicMock()
        main = Main()
        main._session = session
        session.add.side_effect = Exception()
        with self.assertRaises(Exception) as cm:
            main.send_event_to_database(ANY, ANY)
        self.assertEqual("Error sending event to database", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
