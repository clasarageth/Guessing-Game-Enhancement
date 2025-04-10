import socket
import random

class GuessingGameServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.correct_password = "admin123"
        self.clients = {}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server started at {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Connected by {addr}")
                self.handle_client(conn)

    
    def get_performance_rating(self, guesses):
        if guesses <= 5:
            return "Excellent"
        elif 6 <= guesses <= 20:
            return "Very Good"
        else:
            return "Good/Fair"

    def handle_client(self, conn):
        password_attempt = conn.recv(1024).decode()
        if password_attempt != self.correct_password:
            conn.sendall(b"Incorrect password. Access denied.")
            conn.close()
            return

        number_to_guess = random.randint(1, 100)
        guesses = 0
        conn.sendall(b"Password accepted. Start guessing!")

        while True:
            guess = conn.recv(1024).decode()
            if not guess:
                break
            guess = int(guess)
            guesses += 1

            if guess < number_to_guess:
                conn.sendall(b"Too low!")
            elif guess > number_to_guess:
                conn.sendall(b"Too high!")
            else:
                performance_rating = self.get_performance_rating(guesses)
                conn.sendall(f"Congratulations! You guessed it right in {guesses} guesses. \n Performance Rating: {performance_rating}".encode())
                break

        conn.close()

    
if __name__ == "__main__":
    server = GuessingGameServer()
    server.start()