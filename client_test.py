import unittest
import socket
from unittest.mock import Mock, patch
from client import GuessingGameClient

class TestGuessingGameClient(unittest.TestCase):

    def setUp(self):
        self.client = GuessingGameClient(host='127.0.0.1', port=8001) 

    @patch('builtins.input', side_effect=["admin123", "50"]) 
    @patch('socket.socket')
    def test_client_successful_game(self, mock_socket, mock_input):
        mock_sock_instance = Mock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        
        mock_sock_instance.recv.side_effect = [
            b"Password accepted. Start guessing!",
            b"Congratulations! You guessed it right in 1 guesses. \n Performance Rating: Excellent"
        ]

        self.client.start()
        mock_sock_instance.connect.assert_called_with(('127.0.0.1', 8001))
        mock_sock_instance.sendall.assert_any_call(b"admin123")
        mock_sock_instance.sendall.assert_any_call(b"50")
        mock_sock_instance.recv.assert_called()

    @patch('builtins.input', side_effect=["wrongpassword"]) 
    @patch('socket.socket')
    def test_client_access_denied(self, mock_socket, mock_input):
        mock_sock_instance = Mock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        
        mock_sock_instance.recv.return_value = b"Incorrect password. Access denied."

        self.client.start()
        mock_sock_instance.connect.assert_called_with(('127.0.0.1', 8001))
        mock_sock_instance.sendall.assert_called_with(b"wrongpassword")
        mock_sock_instance.recv.assert_called_once()
        self.assertEqual(mock_sock_instance.sendall.call_count, 1)

if __name__ == '__main__':
    unittest.main()