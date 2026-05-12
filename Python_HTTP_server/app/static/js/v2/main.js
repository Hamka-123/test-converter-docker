console.log("Модульная система запущена!");
const moduleName = import.meta.url.split('/').pop();
console.log(`%c[MODULE] ${moduleName} is ready`, "color: #00ff00; font-weight: bold;");

// static/js/v2/main.js
import * as api from './api.js';
import * as ui from './ui.js';
import * as storage from './storage.js';

let debounceTimer;
let currencyList = {};

const init = async () => {
    // 1. Инициализация данных (кэш или API)
    let apiData = storage.getRatesFromLocal();
    if (!apiData) {
        apiData = await api.getRatesInBack();
        if (apiData) storage.saveRatesToLocal(apiData);
    }

    if (apiData) {
        // ... твой код заполнения currencyList и создания options ...
        
        // Функции performConversion и handleInput переезжают сюда
        // Вешаем EventListeners
        document.getElementById('GetAllLogs').addEventListener('click', async () => {
            const logs = await api.getLogsInBack();
            ui.drawLogsTable(logs);
        });

        // Запуск поллинга
        setInterval(async () => {
            const freshData = await api.getRatesInBack();
            if (freshData) {
                storage.saveRatesToLocal(freshData);
                // Обновляем currencyList
            }
        }, 300000);
    }
};

init();