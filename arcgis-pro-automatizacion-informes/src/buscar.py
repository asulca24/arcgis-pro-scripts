import requests
import pandas as pd

# Define la URL con las coordenadas y el radio de San Martín de Porres
url = "https://apis.geodir.co/maps/data?lat=-11.988362&lng=-77.097845&radius=YOUR_RADIUS&key=YOUR_API_KEY"

# Realiza la solicitud GET
print("Realizando la solicitud GET a la URL:", url)
response = requests.get(url)
data = response.json()

# Verifica la estructura del JSON
print("Datos JSON recibidos:")
print(data)
