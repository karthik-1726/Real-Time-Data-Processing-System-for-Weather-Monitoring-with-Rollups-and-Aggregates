import mysql.connector

def init_db():
    conn = mysql.connector.connect(
        host='localhost',    # Replace with your MySQL host
        user='root', # Replace with your MySQL username
        password='', # Replace with your MySQL password
        database='weather_data' # Replace with your MySQL database name
    )
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            avg_temp FLOAT,
            max_temp FLOAT,
            min_temp FLOAT,
            dominant_weather VARCHAR(255)
        )
    ''')
    conn.commit()
    conn.close()

def save_daily_summary(summary):
    conn = mysql.connector.connect(
        host='localhost',    # Replace with your MySQL host
        user='root', # Replace with your MySQL username
        password='', # Replace with your MySQL password
        database='weather_data' # Replace with your MySQL database name
    )
    c = conn.cursor()
    c.execute('''
        INSERT INTO daily_summaries (city, date, avg_temp, max_temp, min_temp, dominant_weather)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (summary['city'], summary['date'], summary['avg_temp'], summary['max_temp'], summary['min_temp'], summary['dominant_weather']))
    conn.commit()
    conn.close()
