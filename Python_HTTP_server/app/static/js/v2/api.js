const moduleName = import.meta.url.split('/').pop();
console.log(`%c[MODULE] ${moduleName} is ready`, "color: #00ff00; font-weight: bold;");
// static/js/v2/api.js
export const getRatesInBack = async () => {
    const response = await fetch("./get-rates");
    return await response.json();
};

export const getLogsInBack = async () => {
    const response = await fetch("./get-conversion-logs");
    return await response.json();
};

export const CalculateConversion = async (payload) => {
    const response = await fetch("./do-conversion", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    return data.result;
};