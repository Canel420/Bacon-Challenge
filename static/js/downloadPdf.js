async function downloadPDF() {
    try {
        const inputNumber = document.getElementById('inputNumber').value;
        const messageElement = document.getElementById('message');
        if (!inputNumber) {
            messageElement.textContent = 'Give me a number, bro!';
            return;
        }

        const response = await fetch('http://127.0.0.1:5000/api/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                paragraphsQty: inputNumber
            }),
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'report.pdf';
        document.body.appendChild(a);
        a.click();    
        a.remove();
        messageElement.textContent = 'Your PDF is ready!';
        setTimeout(() => {
            messageElement.textContent = '';
        }, 4000);
    } catch (error) {
        console.error('Error:', error);
    }
}