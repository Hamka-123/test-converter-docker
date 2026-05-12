# app/dependencies.py
from data.db_connector import DBConnector
from data.repository import CurrencyRepository

# Создаем объекты один раз при запуске приложения
connector = DBConnector()
repo = CurrencyRepository(connector)