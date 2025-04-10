import socket
import random
import time

class BotClient:
    def __init__(self, host='127.0.0.1', port=8000, password='admin123'):
        self.host = host
        self.port = port
        self.password = password
        self.number_to_guess = random.randint(1, 100)
        self.guesses = 0

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bot_socket:
            bot_socket.connect((self.host, self.port))
            bot_socket.sendall(self.password.encode())

            response = bot_socket.recv(1024).decode()
            print(response)

            if "Access denied" in response:
                return

            low, high = 1, 100
            while low <= high:
                self.guesses += 1
                guess = (low + high) // 2
                print(f"Bot guesses: {guess}")
                bot_socket.sendall(str(guess).encode())
                response = bot_socket.recv(1024).decode()
                print(response)

                if "Too low!" in response:
                    low = guess + 1
                elif "Too high!" in response:
                    high = guess - 1
                elif "Congratulations" in response:
                    break

if __name__ == "__main__":
    bot = BotClient()
    bot.start()