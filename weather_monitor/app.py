from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import time
import requests
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__, static_folder="templates/static")


API_KEY = '31d3a400e2a36403bf53f77377e71fba'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
INTERVAL = 300
temperature_threshold = 35  # Default threshold

DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'weather_data',
}

def init_db():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_weather_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(255),
            date DATE,
            avg_temp FLOAT,
            max_temp FLOAT,
            min_temp FLOAT,
            dominant_weather VARCHAR(255)
        );
    """)
    
    connection.commit()
    cursor.close()
    connection.close()

def save_daily_summary(summary):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO daily_weather_summary (city, date, avg_temp, max_temp, min_temp, dominant_weather)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    cursor.execute(insert_query, (
        summary['city'],
        summary['date'],
        summary['avg_temp'],
        summary['max_temp'],
        summary['min_temp'],
        summary['dominant_weather']
    ))
    
    connection.commit()
    cursor.close()
    connection.close()

def fetch_daily_summaries():
    """Fetch daily summaries from the MySQL database."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM daily_weather_summary;")
    summaries = cursor.fetchall()

    cursor.close()
    connection.close()
    return summaries

def get_weather_data(city):
    try:
        response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY})
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the JSON response from the API
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None  # Return None if there was an error


def process_weather_data(data):
    main = data['main']
    weather_condition = data['weather'][0]['main']
    
    temp_k = main['temp']
    feels_like_k = main['feels_like']
    
    temp_c = temp_k - 273.15
    feels_like_c = feels_like_k - 273.15
    
    return {
        'temperature': temp_c,
        'feels_like': feels_like_c,
        'weather_condition': weather_condition,
        'timestamp': datetime.fromtimestamp(data['dt']),
    }

@app.route('/')
def index():
    return render_template('html/index.html')

@app.route('/current_weather', methods=['GET'])
def fetch_weather_data():
    weather_data = []
    for city in CITIES:
        data = get_weather_data(city)
        if data.get('cod') == 200:
            processed_data = process_weather_data(data)
            weather_data.append({
                'city': city,
                'temperature': processed_data['temperature'],
                'feels_like': processed_data['feels_like'],
                'weather_condition': processed_data['weather_condition']
            })
    return jsonify(weather_data)

@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    data = request.get_json()
    global temperature_threshold  # Use the global variable
    temperature_threshold = data['threshold']
    return jsonify({'threshold': temperature_threshold})  # Return the new threshold


@app.route('/daily_summaries', methods=['GET'])
def get_daily_summaries():
    try:
        summaries = fetch_daily_summaries()
        return jsonify(summaries)  # Return JSON response
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True)