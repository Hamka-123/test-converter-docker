console.log("Script running ...");

const f1 = () =>{
    fetch("./get_something")
    .then(resp => {
        console.log(`resp.status = ${resp.status}`)
        return resp.text();
    })
    .then(data => console.log(data))
    .finally();
}

const get_users = () => {
    fetch("./get_users")
    .then(resp => {
        console.log(`resp.status = ${resp.status}`)
        return resp.text();
    })
    .then(data => console.log(data));
}
    // fetch('https://jsonplaceholder.typicode.com/todos/1')
    //   .then(response => response.json())
    //   .then(json => console.log(json))

// const get_users_from_server_and_draw = async () => {
//     const response = await fetch("./draw_users");
    
//     console.log(`resp.status = ${response.status}`);
    
//     // Преобразуем в JSON и возвращаем
//     const data = await response.json(); 
//     drawUsersTable(response); 
// }
const get_users_from_server_and_draw = () => {
    // 1. Делаем запрос
    fetch("./draw_users")
        .then(response => {
            console.log(`resp.status = ${response.status}`);
            // 2. Распаковываем текст в JSON (это тоже возвращает Promise)
            return response.json(); 
        })
        .then(data => {
            // 3. Когда данные распакованы, рисуем таблицу
            drawUsersTable(data);
        })
        .catch(error => {
            // Хорошая практика — добавить обработку ошибок
            console.error("Ошибка при получении данных:", error);
        });
}


const drawUsersTable = (users) => {
    const TROWS = users.map(u => `
        <tr>
            <td>${u.id}</td>
            <td>${u.name}</td>
            <td>${u.username}</td>
            <td>${u.email}</td>
            <td>${u.address.city}</td>
            <td>${u.phone}</td>
        </tr>
    `).join("");

    // document.body.innerHTML += `<table>${TROWS}</table>`;
    document.getElementById('result').innerHTML = `<table>${TROWS}</table>`;
}
const handleTes4 = () => {
    fetch("https://jsonplaceholder.typicode.com/users")
    .then(resp => {
        console.log(`resp.status = ${resp.status}`)
        return resp.text();
    })
    .then(data => console.log(data));
}


// 14.04.2026
const drawCurrencyTable = (currencies) => {
    // currencies — это уже массив [{}, {}, {}]
    const TROWS = currencies.map(c => `
        <tr>
            <td>${c.date}</td>
            <td>${c.base}</td>
            <td>${c.quote}</td>
            <td>${c.rate}</td>
        </tr>
    `).join("");

    document.getElementById("result2").innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Base</th>
                    <th>Quote</th>
                    <th>Rate</th>
                </tr>
            </thead>
            <tbody>
                ${TROWS}
            </tbody>
        </table>`;
    }

const GetAllRates = () => {
fetch("./get-rates")
    .then(response => {
        console.log(`resp.status = ${response.status}`);
        return response.json(); 
    })
    .then(data => {
                // 3. Когда данные распакованы, рисуем таблицу
                drawCurrencyTable(data);
    })
    .catch(error => {
            // Хорошая практика — добавить обработку ошибок
            console.error("Ошибка при получении данных:", error);
    });
}
document.getElementById('GetAllRates')
        .addEventListener('click', GetAllRates)




// ------------- Local Storage -------------
// Сохранение в память браузера
const saveRatesToLocal = (data) => {
    const cache = {
        rates: data,
        timestamp: Date.now()
    };
    localStorage.setItem('currency_cache', JSON.stringify(cache));
    // console.log("Данные в кеше обновлены")
};

// Загрузка из памяти
const getRatesFromLocal = () => {
    const cached = localStorage.getItem('currency_cache');
    if (!cached) return null;
    
    const parsed = JSON.parse(cached);
    // Считаем кэш валидным 24 часа (86400000 мс)
    if (Date.now() - parsed.timestamp < 86400000) {
        return parsed.rates;
    }
    return null;
};        
// ------------- Conversions -------------

document.getElementById('Converter')
        .addEventListener('click', () => {
    document.getElementById("ConverterBlock").classList.toggle("active")
})

const CalculateConversion = async (fromCurr, toCurr, amount, fromRate, toRate) => {
    // Формируем объект из чистых аргументов
    const payload = {
        from: fromCurr,
        to: toCurr,
        amount: amount,
        fromRate: fromRate,
        toRate: toRate
    };

    try {
        const response = await fetch("./do-conversion", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json(); 
        return data.result; 
    } catch (error) {
        console.error("Ошибка при выполнении конвертации:", error);
    }
}

// 1. Помечаем функцию как async
const getRatesInBack = async () => {
    try {
        const response = await fetch("./get-rates");
        console.log(`resp.status = ${response.status}`);
        
        const data = await response.json(); 
        console.log("Данные получены:", data);
        return data; // Теперь функция возвращает Promise с данными
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    }
}

// 2. Чтобы использовать результат, нам тоже нужна async-обертка
const init = async () => {
    let debounceTimer;

    // 1. Проверяем, есть ли данные в кэше
    let apiData = getRatesFromLocal();
    if (apiData) {
        console.log("Данные загружены из LocalStorage (мгновенно)");
    } else {
        console.log("Кэш пуст, запрашиваем сервер...");
        apiData = await getRatesInBack(); // Ждем, пока данные придут
        if (apiData) saveRatesToLocal(apiData); // сохраняем в кеш обновление
    }

    if (apiData && apiData.length > 0) {
        // Формируем словарь курсов
        const currencyList = {};

        // 1. Сначала вручную добавляем Евро, так как её нет в списке rates
        // Мы берем base из первого элемента (там обычно "EUR")
        const baseCurr = apiData[0].base;
        currencyList[baseCurr] = {
            rate: 1.0, // Относительно самой себя курс всегда 1
            meta: { date: apiData[0].date, base: baseCurr }
        };
        console.log("Успех! Базовая валюта:", apiData[0].base);
        
        // 2. Добавляем все остальные валюты из пришедшего списка
        apiData.forEach(item => {
            currencyList[item.quote] = {
                rate: item.rate,
                meta: { date: item.date, base: item.base }
            };
        });
            // Теперь можно достать вот так: console.log(currencyList['AED'].rate); // 4.3074

        // Генерируем опции для селектов
        const options = Object.entries(currencyList)
        .map(([code, data]) => {
            return `<option value="${code}" data-rate="${data.rate}">${code}</option>`;
        })
        .join('');

        // Находим элементы формы
        const currFromInput = document.querySelector('[name="currFrom"]')
        const currToInput = document.querySelector('[name="currTo"]')
        const FromAmountInput = document.querySelector('[name="FromAmount"]')
        const ToAmountInput = document.querySelector('[name="ToAmount"]')
        const rateDisplay = document.querySelector('#ConverterBlock h3 span');

        currFromInput.innerHTML = options; 
        currToInput.innerHTML = options;  

        // ФУНКЦИЯ РАСЧЕТА
        // 1. Создаем универсальную функцию с параметром direction
        const performConversion = async (direction = 'from') => {
            const from = currFromInput.value;
            const to = currToInput.value;
            const fRate = parseFloat(currFromInput.options[currFromInput.selectedIndex].dataset.rate);
            const tRate = parseFloat(currToInput.options[currToInput.selectedIndex].dataset.rate);

            // Считаем кросс-курс для заголовка
            const currentPairRate = (tRate / fRate).toFixed(4);
            rateDisplay.textContent = `1 ${from} = ${currentPairRate} ${to}`;

            if (direction === 'from') {
                const amount = FromAmountInput.value;
                if (amount > 0) {
                    // Считаем слева направо (стандартно)
                    const res = await CalculateConversion(from, to, amount, fRate, tRate);
                    ToAmountInput.value = res;
                } else { ToAmountInput.value = ""; }
            } else {
                const amount = ToAmountInput.value;
                if (amount > 0) {
                    // Считаем справа налево (обратный расчет)
                    // Внимание: теперь меняем местами рейты в функции
                    const res = await CalculateConversion(to, from, amount, tRate, fRate);
                    FromAmountInput.value = res;
                } else { FromAmountInput.value = ""; }
            }
        };

        // Функция-обертка для задержки
        const handleInput = (direction) => {
            // Очищаем предыдущий таймер, если пользователь нажал клавишу снова
            clearTimeout(debounceTimer);

            // Устанавливаем новый таймер на 300мс 
            debounceTimer = setTimeout(() => {
                performConversion(direction);
            }, 300); 
        };

        // Вешаем на инпуты
        FromAmountInput.addEventListener('input', (e) => {
            // Если ввели минус, мгновенно убираем его
            if (e.target.value < 0) e.target.value = 0; 
            handleInput('from');
        });
        ToAmountInput.addEventListener('input', (e) => {
            if (e.target.value < 0) e.target.value = 0; 
            handleInput('to')});

        // При смене валюты логичнее пересчитывать от "базового" (левого) поля
        currFromInput.addEventListener('change', () => performConversion('from'));
        currToInput.addEventListener('change', () => performConversion('to'));
        
        // Кнопка Toggle (реверс)
        document.getElementById('toogleCurr').addEventListener('click', (e) => {
            e.preventDefault();
            
            // 1. Меняем местами коды валют
            const tempCurr = currFromInput.value;
            currFromInput.value = currToInput.value;
            currToInput.value = tempCurr;

            // 2. Меняем местами значения в полях ввода
            const tempAmount = FromAmountInput.value;
            FromAmountInput.value = ToAmountInput.value;
            ToAmountInput.value = tempAmount;

            // 3. Пересчитываем всё (теперь данные в инпутах уже на новых местах)
            performConversion('from');
        });
        // store rate data in localStorage and use it (read and update by websocket 1 time per 5 minutes)
        // --- ЗАПУСКАЕМ ПОЛЛИНГ (Имитация веб-сокетов) ---
        setInterval(async () => {
            console.log("Автоматическое обновление курсов...");
            const freshData = await getRatesInBack();
            
            if (freshData) {
                saveRatesToLocal(freshData);
                // Обновляем текущие рейты в объекте currencyList, 
                // по которому считает функция performConversion
                freshData.forEach(item => {
                    if (currencyList[item.quote]) {
                        currencyList[item.quote].rate = item.rate;
                    }
                });
                console.log("Курсы успешно обновлены в фоне!");
                
                // Если нужно, чтобы визуально пересчиталось сразу после обновления:
                // performConversion('from'); 
            }
        }, 5 * 60 * 1000); // 5 минут
    }  
}

init();

// ----------- LOGS ------------------
const drawLogsTable = (currencies) => {
    const TROWS = currencies.map(c => `
        <tr>
            <td>${c.timestamp}</td>
            <td>${c.amount} ${c.from_currency}</td>
            <td>${c.rate}</td> 
            <td>${c.result} ${c.to_currency}</td>
        </tr>
    `).join("");

    document.getElementById("result2").innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>From</th>
                    <th>Exchange Rate</th> 
                    <th>To</th>
                </tr>
            </thead>
            <tbody>
                ${TROWS}
            </tbody>
        </table>`;
}

const GetAllLogs = () => {
    fetch("./get-conversion-logs")
    .then(response => {
        console.log(`resp.status = ${response.status}`);
        return response.json(); 
    })
    .then(data => { drawLogsTable(data);})
    .catch(error => { console.error("Ошибка при получении данных:", error);});
}

document.getElementById('GetAllLogs')
        .addEventListener('click', GetAllLogs)

