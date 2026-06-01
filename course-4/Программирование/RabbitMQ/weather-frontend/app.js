document.getElementById('getWeatherBtn').addEventListener('click', async () => {
    const citiesInput = document.getElementById('cities').value;
    if (!citiesInput.trim()) {
        alert('Please enter at least one city.');
        return;
    }

    const cities = citiesInput.split(',').map(city => city.trim()).filter(city => city);
    
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const tableBody = document.querySelector('#weatherTable tbody');

    loader.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    tableBody.innerHTML = '';

    try {
        const response = await fetch('http://localhost:8080/api/weather/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cities: cities })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch weather data');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        errorDiv.textContent = 'An error occurred while fetching weather data. Please try again.';
        errorDiv.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const tableBody = document.querySelector('#weatherTable tbody');
    const weatherData = data.weatherData;

    for (const [city, info] of Object.entries(weatherData)) {
        const row = document.createElement('tr');
        
        const cityCell = document.createElement('td');
        cityCell.textContent = city;
        row.appendChild(cityCell);

        const tempCell = document.createElement('td');
        if (info.error) {
            tempCell.textContent = 'N/A';
        } else {
            tempCell.textContent = info.temperature;
        }
        row.appendChild(tempCell);

        const descCell = document.createElement('td');
        if (info.error) {
            descCell.textContent = `Error: ${info.error}`;
            descCell.style.color = 'red';
        } else {
            descCell.textContent = info.description;
        }
        row.appendChild(descCell);

        tableBody.appendChild(row);
    }

    resultsDiv.classList.remove('hidden');
}
