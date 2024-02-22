# This code is written by Ole Edvard Grov, Skolelaboratoriet i realfag, UiB


#!/usr/bin/env python3


# Importerer et bibliotek, vi skal bruke for å laste ned data.
import requests
import pytz
from datetime import datetime

# Setter lokal tidssone.
lokal_tz = pytz.timezone('Europe/Oslo')

# For å hente et varsel trenger vi koodinater lengdegrad og breddegrad. Disse må endres av hver student som skal 
# kjøre koden for et nytt sted.

lengdegrad = 5.0
breddegrad = 60.0

params = {
  'lat' : breddegrad,
  'lon' : lengdegrad 
}

# Ignorer denne linja....
headers = {
  'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

# URL vi skal hente data fra.
data_url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?'

# Henter data fra stedet vi har oppgitt. 
response = requests.get(data_url, params=params, headers=headers)

# Header
print('Dato/tid\tNedbør (mm)')

# Behandler data vi får tilbake fra serveren.
if response.status_code == 200:
    data = response.json()['properties']['timeseries']
    if len(data) > 0:
        for d in data:
          dato = datetime.strptime(d.get('time'),"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc).astimezone(lokal_tz)
          nedbor = d.get('data', {}).get('next_1_hours',{}).get('details', {}).get('precipitation_amount')
          if nedbor != None:
            print(dato.strftime('%Y-%m-%d %H:%M'), nedbor, sep='\t')       
else:
    print('Nettverksfeil!')
