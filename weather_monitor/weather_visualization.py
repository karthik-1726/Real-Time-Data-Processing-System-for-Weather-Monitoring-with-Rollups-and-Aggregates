import matplotlib.pyplot as plt
import mysql.connector

def plot_weather_summary():
    conn = mysql.connector.connect(
        host='localhost',    # Replace with your MySQL host
        user='root', # Replace with your MySQL username
        password='', # Replace with your MySQL password
        database='weather_data' # Replace with your MySQL database name
    )
    c = conn.cursor()
    
    # Execute the query to fetch average temperatures by date
    c.execute('SELECT date, AVG(avg_temp) FROM daily_summaries GROUP BY date')
    data = c.fetchall()
    
    # Separate the fetched data into lists for plotting
    dates = [row[0] for row in data]
    avg_temps = [row[1] for row in data]
    
    # Plot the data
    plt.plot(dates, avg_temps, marker='o')
    plt.title('Daily Average Temperature')
    plt.xlabel('Date')
    plt.ylabel('Average Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    conn.close()
