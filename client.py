import socket

class GuessingGameClient:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            password = input("Enter the password to play the game: ")
            client_socket.sendall(password.encode())

            response = client_socket.recv(1024).decode()
            print(response)

            if "Access denied" in response:
                return

            while True:
                guess = input("Enter your guess (1-100): ")
                client_socket.sendall(guess.encode())
                response = client_socket.recv(1024).decode()
                print(response)
                if "Congratulations" in response:
                    break

if __name__ == "__main__":
    client = GuessingGameClient()
    client.start()