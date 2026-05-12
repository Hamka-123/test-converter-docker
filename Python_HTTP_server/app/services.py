# вынести сюда все методы из Distributed_Monolith_Currency_System/Python_HTTP_server/app/web_server.py

# сложить сюда всю логику приложения
# когда тут станет слишком тесно - сделать папку в которой всё разбить на отдельные сервисы

# app/services.py
# from dependencies import repo

# def process_currency_conversion(data):
#     # Вся математика здесь
#     from_curr = data.get("from")
#     to_curr = data.get("to")
#     amount = float(data.get("amount", 0))
#     # ... расчеты ...
    
#     # Сохранение
#     repo.add_conversion(from_curr, to_curr, amount, result, final_rate)
    
#     return {"status": "success", "result": result}