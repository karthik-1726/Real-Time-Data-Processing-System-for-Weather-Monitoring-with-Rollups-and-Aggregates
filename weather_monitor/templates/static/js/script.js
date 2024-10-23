const API_URL = 'http://localhost:5000'; // If you're running a local backend on port 5001

// Set alert threshold
document.getElementById('set-threshold').addEventListener('click', () => {
    const thresholdInput = document.getElementById('threshold');
    const threshold = parseFloat(thresholdInput.value);  // Ensure it's parsed as a number

    if (!isNaN(threshold)) {  // Check if the threshold is a valid number
        fetch(`${API_URL}/set_threshold`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ threshold }),
        })
        .then(response => response.json())
        .then(data => alert(`Threshold set to ${data.threshold}°C`))
        .catch(err => console.error(err));
    } else {
        alert('Please enter a valid threshold value.');  // Handle invalid input
    }
});


function loadWeatherData() {
    fetch(`${API_URL}/current_weather`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const weatherDataContainer = document.getElementById('weather-data');
            weatherDataContainer.innerHTML = '';
            data.forEach(cityWeather => {
                const row = `<tr>
                    <td>${cityWeather.city}</td>
                    <td>${cityWeather.temperature.toFixed(2)}</td>
                    <td>${cityWeather.feels_like.toFixed(2)}</td>
                    <td>${cityWeather.weather_condition}</td>
                </tr>`;
                weatherDataContainer.innerHTML += row;
            });
        })
        .catch(err => console.error('Error loading weather data:', err));
}

// Load daily summaries with inline styling
document.getElementById('load-summaries').addEventListener('click', () => {
    fetch(`${API_URL}/daily_summaries`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const summariesContainer = document.getElementById('summaries');
            summariesContainer.innerHTML = ''; // Clear previous summaries
            if (data.length === 0) {
                summariesContainer.innerHTML = '<p>No summaries available.</p>';
                return;
            }
            data.forEach(summary => {
                const summaryDiv = `<div>
                    <strong>Date:</strong> ${summary.date} |
                    <strong>City:</strong> ${summary.city} |
                    <strong>Avg Temp:</strong> ${summary.avg_temp.toFixed(2)}°C |
                    <strong>Max Temp:</strong> ${summary.max_temp.toFixed(2)}°C |
                    <strong>Min Temp:</strong> ${summary.min_temp.toFixed(2)}°C |
                    <strong>Dominant Weather:</strong> ${summary.dominant_weather}
                </div>`;
                summariesContainer.innerHTML += summaryDiv;
            });
        })
        .catch(err => console.error('Error loading summaries:', err));
});


// Load current weather on page load
window.onload = loadWeatherData;