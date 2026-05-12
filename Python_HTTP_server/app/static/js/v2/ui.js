const moduleName = import.meta.url.split('/').pop();
console.log(`%c[MODULE] ${moduleName} is ready`, "color: #00ff00; font-weight: bold;");
// static/js/v2/ui.js
export const drawLogsTable = (logs) => {
    const TROWS = logs.map(c => `
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
                    <th>Date</th><th>From</th><th>Exchange Rate</th><th>To</th>
                </tr>
            </thead>
            <tbody>${TROWS}</tbody>
        </table>`;
};

export const updateRateDisplay = (element, text) => {
    element.textContent = text;
};