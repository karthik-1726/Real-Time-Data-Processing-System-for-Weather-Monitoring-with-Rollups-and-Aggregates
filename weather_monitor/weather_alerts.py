import smtplib
from email.mime.text import MIMEText

def send_alert(city, weather_data):
    alert_message = f"Alert! Temperature in {city} exceeded threshold: {weather_data['temperature']}°C."
    print(alert_message)  # Print to console (could also send email)
    
    # Example email sending (uncomment to use):
    # msg = MIMEText(alert_message)
    # msg['Subject'] = 'Weather Alert'
    # msg['From'] = 'your_email@example.com'
    # msg['To'] = 'recipient@example.com'
    #
    # with smtplib.SMTP('smtp.example.com') as server:
    #     server.login('your_email@example.com', 'your_password')
    #     server.send_message(msg)

def check_alerts(weather_data, threshold):
    return weather_data['temperature'] > threshold
