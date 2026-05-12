import logging
from http.server import HTTPServer
from web_server import MyHTTPHandler  # Импортируем наш обработчик
from dependencies import repo         # Чтобы инициализировать всё при старте

# Настройка логирования (можно тоже вынести в logger.py)
logging.basicConfig(level=logging.INFO)

SERVER_ADDRESS = ("0.0.0.0", 8000)

def run():
    print(f"🚀 Server starting at http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
    my_http_server = HTTPServer(SERVER_ADDRESS, MyHTTPHandler)
    try:
        my_http_server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        my_http_server.server_close()

if __name__ == "__main__":
    run()
