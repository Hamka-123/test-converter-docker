import mimetypes
import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from dependencies import repo    
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Conversion logic / write to db and log about it
# def save_conversion(from_curr, to_curr, amount, result, rate):
#     try:
#         with sqlite3.connect(DB_PATH) as conn:
#             conn.execute("""
#                 INSERT INTO conversions (from_currency, to_currency, amount, result, rate) 
#                 VALUES (?, ?, ?, ?, ?)
#             """, (from_curr, to_curr, amount, result, rate))
#         logging.info(f"SUCCESS: {amount} {from_curr} to {result} {to_curr} at rate {rate} saved to DB.")
#     except Exception as e:
#         logging.error(f"DB Error: {e}")
def save_conversion(from_curr, to_curr, amount, result, rate):
    try:
        # Просто вызываем метод репозитория
        repo.add_conversion(from_curr, to_curr, amount, result, rate)
        logging.info(f"SUCCESS: {amount} {from_curr} to {result} {to_curr} at rate {rate} saved to DB.")
    except Exception as e:
        logging.error(f"DB Error: {e}")
    
class MyHTTPHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, code, body, content_type="application/json", extra_headers=None):
        # 1. Подготовка тела (как и раньше)
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        response_data = body.encode('utf-8')

        # 2. Базовые заголовки
        self.send_response(code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(response_data)))

        # 3. Добавляем любые специфические заголовки, если они переданы
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)

        self.end_headers()
        self.wfile.write(response_data)
    
    def do_GET(self):
        # 1. Сначала проверяем системные вещи, которые не относятся к API
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # 2. Определяем путь к файлу для статики
        # Если просят корень '/', отдаем index.html
        relative_path = "index.html" if self.path == "/" else self.path.lstrip("/")
        static_file_path = os.path.join(BASE_DIR, "static", relative_path)

        # 3. Если такой файл физически существует в папке static — отдаем его!
        if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
            self.serve_static_file(static_file_path)
            return

        # 4. Если это не файл, значит это запрос к нашему API
        self.handle_api_requests()

    def serve_static_file(self, file_path):
        try:
            # Автоматически определяем: text/html, application/javascript и т.д.
            mime_type, _ = mimetypes.guess_type(file_path)
            
            with open(file_path, "rb") as f: # Открываем в бинарном виде (rb) для универсальности
                content = f.read()
                
            self.send_response(200)
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def handle_api_requests(self):
        # Вот здесь остается твой чистый match-case только для ДАННЫХ
        match self.path:
                
            case "/get_users":
                # print("Users")
                # headers["Content-Type"] = "application/json; charset=utf-8"
                # with open("data/users.json") as f: resp = f.read()
                with open("data/users.json", "r", encoding="utf-8") as f:
                # Читаем файл как строку и сразу отправляем
                    self._send_response(200, f.read())
            
            case "/draw_users":
                # print("draw users")
                # headers["Content-Type"] = "application/json; charset=utf-8"
                # api_resp = requests.get('https://jsonplaceholder.typicode.com/users')
                # data = api_resp.json() 
                # logging.info(f"Draw users task done. {len(data)} users fetched")
                # resp = json.dumps(data)
                data = requests.get('https://jsonplaceholder.typicode.com/users').json()
                logging.info(f"Draw users task done. {len(data)} fetched")
                self._send_response(200, data)
                
                
            case "/get-rates":
                # print ("Get rates")
                # headers["Content-Type"] = "application/json; charset=utf-8"
                # api_resp = requests.get('https://api.frankfurter.dev/v2/rates')
                # data = api_resp.json() 
                # if isinstance(data, dict): rates_count = len(data.get('rates', {}))
                # else: rates_count = len(data) 
                # logging.info(f"Get rates task done. {rates_count} rates fetched")
                # resp = json.dumps(data)
                data = requests.get('https://api.frankfurter.dev/v2/rates').json()
                # Логику подсчета можно оставить для логов
                rates_count = len(data.get('rates', {})) if isinstance(data, dict) else len(data)
                logging.info(f"Get rates task done. {rates_count} fetched")
                self._send_response(200, data)
                
            case "/get-conversion-logs":
                # with sqlite3.connect(DB_PATH) as conn:
                #     # Эта магия заставляет sqlite возвращать данные в виде словарей {ключ: значение}
                #     conn.row_factory = sqlite3.Row 
                #     cursor = conn.execute("SELECT * FROM conversions ORDER BY timestamp DESC")
                #     # Собираем список словарей
                #     rows = [dict(row) for row in cursor.fetchall()]
                    
                # resp = json.dumps(rows)
                # headers["Content-Type"] = "application/json"
                
                # Репозиторий уже возвращает список словарей, готовый для JSON
                
                # rows = repo.get_all_conversions()
                
                # # Обработка datetime для JSON (MariaDB возвращает объекты datetime)
                # for row in rows:
                #     if hasattr(row.get('timestamp'), 'isoformat'):
                #         row['timestamp'] = row['timestamp'].isoformat()
                
                # resp = json.dumps(rows)
                # headers["Content-Type"] = "application/json"
                rows = repo.get_all_conversions()
                for row in rows:
                    if hasattr(row.get('timestamp'), 'isoformat'):
                        row['timestamp'] = row['timestamp'].isoformat()
                self._send_response(200, rows)
            
            case "/hello":
                self._send_response(200, "Hello, World!", content_type="text/plain")
                
            case "/download_users":
                with open("data/users.json", "r") as f:
                    data = f.read()
                
                # Передаем кастомный заголовок
                custom_headers = {
                    "Content-Disposition": "attachment; filename='users_backup.json'",
                    "Cache-Control": "no-cache"
                }
                
                self._send_response(200, data, extra_headers=custom_headers)
            
            case _:
                # CODE = 404
                # resp = "File not found"
                self._send_response(404, {"error": "File not found"})
    
    # ДОБАВЛЯЕМ МЕТОД ДЛЯ POST
    # def do_POST(self):
    #     if self.path == "/do-conversion":
    #         content_length = int(self.headers['Content-Length'])
    #         post_data = self.rfile.read(content_length)
            
    #         try:
    #             data = json.loads(post_data.decode('utf-8'))
    #             from_curr = data.get("from")
    #             to_curr   = data.get("to")
    #             amount    = float(data.get("amount", 0))
    #             from_rate = float(data.get("fromRate", 1.0))
    #             to_rate   = float(data.get("toRate", 1.0))

    #             # 3. Математика с округлением до 2 знаков для результата
    #             if from_rate > 0:
    #                 # Округляем до 2 знаков для денег (или до 4, если валюта очень дешевая)
    #                 final_rate = round(to_rate / from_rate, 4) if from_rate > 0 else 0
    #                 result = round(amount * final_rate, 2)
    #             else:
    #                 result = 0
    #             save_conversion(from_curr, to_curr, amount, result, final_rate)
    #             # logging.info(f"Success: {amount} {from_curr} -> {result:.2f} {to_curr} (Rate: {final_rate})")    
                
                
    #             self.send_response(200)
    #             self.send_header('Content-Type', 'application/json')
    #             self.end_headers()
    #             self.wfile.write(json.dumps({"status": "success", "result": round(result, 2)}).encode())
                
    #         except Exception as e:
    #             logging.error(f"POST Error: {e}")
    #             self.send_response(400)
    #             self.end_headers()
    #             self.wfile.write(json.dumps({"error": str(e)}).encode())
    def do_POST(self):
        if self.path == "/do-conversion":
            try:
                content_length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(content_length).decode('utf-8'))
                
                # (Твоя математика без изменений)
                amount = float(data.get("amount", 0))
                from_rate = float(data.get("fromRate", 1.0))
                to_rate = float(data.get("toRate", 1.0))
                final_rate = round(to_rate / from_rate, 4) if from_rate > 0 else 0
                result = round(amount * final_rate, 2)

                save_conversion(data.get("from"), data.get("to"), amount, result, final_rate)
                
                # Отправляем успех через наш метод
                self._send_response(200, {"status": "success", "result": result})
                
            except Exception as e:
                logging.error(f"POST Error: {e}")
                self._send_response(400, {"error": str(e)})
        # # 1. Получили данные
        # content_length = int(self.headers.get('Content-Length', 0))
        # data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        # match self.path:
        #     case "/do-conversion":
        #         # 2. Вызвали внешний мозг
        #         result = process_currency_conversion(data)
        #         # 3. Отправили ответ
        #         self._send_response(200, result)

