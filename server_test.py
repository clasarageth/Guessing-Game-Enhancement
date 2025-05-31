import unittest
import socket
import random
from unittest.mock import Mock, patch
from server import GuessingGameServer

class TestGuessingGameServer(unittest.TestCase):

    def setUp(self):
        self.server = GuessingGameServer(host='127.0.0.1', port=8001) 

    def test_incorrect_password(self):
        mock_conn = Mock()
        mock_conn.recv.return_value = b"wrongpassword"
        self.server.handle_client(mock_conn)
        mock_conn.sendall.assert_called_with(b"Incorrect password. Access denied.")
        mock_conn.close.assert_called_once()

    def test_guessing_logic_too_low(self):
        mock_conn = Mock()
        mock_conn.recv.side_effect = [b"admin123", b"20", b"30", b"50"] 
        with patch('random.randint', return_value=50):
            self.server.handle_client(mock_conn)
            mock_conn.sendall.assert_any_call(b"Too low!")
            mock_conn.sendall.assert_any_call(b"Congratulations! You guessed it right in 3 guesses. \n Performance Rating: Excellent")
            mock_conn.close.assert_called_once()

    def test_guessing_logic_too_high(self):
        mock_conn = Mock()
        mock_conn.recv.side_effect = [b"admin123", b"80", b"60", b"50"] 

        with patch('random.randint', return_value=50):
            self.server.handle_client(mock_conn)
            mock_conn.sendall.assert_any_call(b"Too high!")
            mock_conn.sendall.assert_any_call(b"Congratulations! You guessed it right in 3 guesses. \n Performance Rating: Excellent")
            mock_conn.close.assert_called_once()

    def test_guessing_logic_correct_guess(self):
        mock_conn = Mock()
        mock_conn.recv.side_effect = [b"admin123", b"50"] 

        with patch('random.randint', return_value=50):
            self.server.handle_client(mock_conn)
            mock_conn.sendall.assert_any_call(b"Congratulations! You guessed it right in 1 guesses. \n Performance Rating: Excellent")
            mock_conn.close.assert_called_once()

    def test_get_performance_rating(self):
        self.assertEqual(self.server.get_performance_rating(3), "Excellent")
        self.assertEqual(self.server.get_performance_rating(5), "Excellent")
        self.assertEqual(self.server.get_performance_rating(6), "Very Good")
        self.assertEqual(self.server.get_performance_rating(20), "Very Good")
        self.assertEqual(self.server.get_performance_rating(21), "Good/Fair")

if __name__ == '__main__':
    unittest.main()