const moduleName = import.meta.url.split('/').pop();
console.log(`%c[MODULE] ${moduleName} is ready`, "color: #00ff00; font-weight: bold;");
// static/js/v2/storage.js
export const saveRatesToLocal = (data) => {
    const cache = {
        rates: data,
        timestamp: Date.now()
    };
    localStorage.setItem('currency_cache', JSON.stringify(cache));
};

export const getRatesFromLocal = () => {
    const cached = localStorage.getItem('currency_cache');
    if (!cached) return null;
    
    const parsed = JSON.parse(cached);
    // 24 часа валидности
    if (Date.now() - parsed.timestamp < 86400000) {
        return parsed.rates;
    }
    return null;
};