import unittest
import socket
from unittest.mock import Mock, patch
from botclient import BotClient

class TestBotClient(unittest.TestCase):

    def setUp(self):
        self.bot = BotClient(host='127.0.0.1', port=8001, password='admin123') 

    @patch('socket.socket')
    def test_bot_successful_game(self, mock_socket):
        mock_sock_instance = Mock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        
        
        mock_sock_instance.recv.side_effect = [
            b"Password accepted. Start guessing!", 
            b"Too high!",  
            b"Too low!",   
            b"Too low!",   
            b"Too high!",   
            b"Congratulations! You guessed it right in 5 guesses. \n Performance Rating: Excellent" 
        ]

        self.bot.start()
        mock_sock_instance.connect.assert_called_with(('127.0.0.1', 8001))
        mock_sock_instance.sendall.assert_any_call(b"admin123")
        self.assertIn(b"50", mock_sock_instance.sendall.call_args_list[1][0]) 
        self.assertIn(b"25", mock_sock_instance.sendall.call_args_list[2][0]) 
        self.assertIn(b"37", mock_sock_instance.sendall.call_args_list[3][0]) 
        self.assertIn(b"43", mock_sock_instance.sendall.call_args_list[4][0])
        self.assertIn(b"40", mock_sock_instance.sendall.call_args_list[5][0]) 
        self.assertEqual(mock_sock_instance.recv.call_count, 6) 

    @patch('socket.socket')
    def test_bot_access_denied(self, mock_socket):
        mock_sock_instance = Mock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        
        mock_sock_instance.recv.return_value = b"Incorrect password. Access denied."

        self.bot.password = "wrongpassword" 
        self.bot.start()
        mock_sock_instance.connect.assert_called_with(('127.0.0.1', 8001))
        mock_sock_instance.sendall.assert_called_with(b"wrongpassword")
        mock_sock_instance.recv.assert_called_once()
        self.assertEqual(mock_sock_instance.sendall.call_count, 1)

if __name__ == '__main__':
    unittest.main()