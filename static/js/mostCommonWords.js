async function mostCommonWords() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/metrics', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        console.log(data);
        const words = data.map(item => item.word);
        const wordsString = words.join(', ');
        document.getElementById('commonWords').innerHTML = wordsString;
    } catch (error) {
        console.error('Error:', error);
    }
}