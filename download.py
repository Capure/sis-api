import requests
import os

LOGIN_URL = "https://logowanie.pg.edu.pl/login?service=https%3a%2f%2fsis.eti.pg.edu.pl%2f"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def download_timetable():
	s = requests.Session()

	# Login

	r = s.get("https://sis.eti.pg.edu.pl/")
	html = r.content.decode("utf-8")
	execution_value = html.split('name="execution" value="')[1].split('"')[0]

	r = s.post(LOGIN_URL, data={ "username": USERNAME, "password": PASSWORD, "execution": execution_value, "geolocation":"", "_eventId": "submit", "submit": "Zaloguj" })
	html = r.content.decode("utf-8")
	execution_value = html.split('name="execution" value="')[1].split('"')[0]

	# Continue to SIS

	r = s.post(LOGIN_URL, data={ "execution": execution_value, "_eventId": "submit", "submit": "Kontynuuj" })
	html = r.content.decode("utf-8")

	# Get the timetable
	r = s.get("https://sis.eti.pg.edu.pl/Planner/ScheduleForGroup/E2301I--0/6")
	html = r.content.decode("utf-8")

	return html