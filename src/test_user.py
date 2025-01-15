import unittest
from unittest.mock import mock_open, patch
from user_manager import UserManager
from user import User

class TestUserManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="Username,Password\nuser1,pass1\nuser2,pass2")
    def test_load_users(self, mock_file):
        """
        Test loading users from a CSV file.
        """
        manager = UserManager()
        self.assertEqual(len(manager.users), 2)
        self.assertEqual(manager.users[0].username, "user1")
        self.assertEqual(manager.users[1].username, "user2")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_users(self, mock_file):
        """
        Test saving users to a CSV file.
        """
        manager = UserManager()

        manager.users = [
            User("user1", "pass1"),
            User("user2", "pass2")
        ]

        manager.save_users()

        mock_file.assert_any_call("../csv_files/users.csv", mode="w", newline="")

        handle = mock_file()
        written_calls = [call.args[0] for call in handle.write.call_args_list]

        expected_calls = [
            "Username,Password\n",
            "user1,pass1\n",
            "user2,pass2\n"
        ]

        normalized_calls = [line.replace("\r\n", "\n") for line in written_calls]
        normalized_expected = [line.replace("\r\n", "\n") for line in expected_calls]

        self.assertEqual(normalized_calls, normalized_expected)

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_success(self, mock_file):
        """
        Test adding a new user successfully.
        """
        manager = UserManager()
        manager.users = []
        result = manager.add_user("new_user", "new_pass")

        self.assertTrue(result)
        self.assertEqual(len(manager.users), 1)
        self.assertEqual(manager.users[0].username, "new_user")
        self.assertEqual(manager.users[0].original_password, "new_pass")

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_duplicate(self, mock_file):
        """
        Test adding a user with an existing username.
        """
        manager = UserManager()
        manager.users = [User(username="existing_user", password="password")]

        result = manager.add_user("existing_user", "new_pass")

        self.assertFalse(result)
        self.assertEqual(len(manager.users), 1)  # No new user should be added

    @patch("builtins.open", new_callable=mock_open)
    def test_authenticate_user_success(self, mock_file):
        """
        Test successful user authentication.
        """
        manager = UserManager()
        manager.users = [User(username="test_user", password="test_pass")]

        user = manager.authenticate_user("test_user", "test_pass")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test_user")

    @patch("builtins.open", new_callable=mock_open)
    def test_authenticate_user_failure(self, mock_file):
        """
        Test user authentication failure.
        """
        manager = UserManager()
        manager.users = [User(username="test_user", password="test_pass")]

        user = manager.authenticate_user("wrong_user", "test_pass")
        self.assertIsNone(user)

        user = manager.authenticate_user("test_user", "wrong_pass")
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()