import pickle
from apiclient.discovery import build

DRIVERS = {}

PROCESS = {}
WAIT = {}
EVENTS = {}

SEMANA = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

"""credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']"""