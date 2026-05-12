# Обновленный обработчик логов
import logging
from dependencies import repo

LOG_FILE = "/app/app.log"


class DatabaseHandler(logging.Handler):
    def __init__(self, repository):
        super().__init__()
        self.repo = repository
        # Инициализация таблиц больше не нужна здесь, 
        # так как мы прогнали миграцию через manage.py

    def emit(self, record):
        try:
            # Используем репозиторий для записи системного лога
            # (Добавь метод add_log в свой CurrencyRepository, если его еще нет)
            self.repo.add_system_log(record.asctime, record.levelname, record.message)
        except Exception:
            self.handleError(record)

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler(), # For vivsible logs in 'docker logs'
#         DatabaseHandler(DB_PATH) 
#     ]
# )

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
        DatabaseHandler(repo) # Передаем наш repo сюда
    ]
)