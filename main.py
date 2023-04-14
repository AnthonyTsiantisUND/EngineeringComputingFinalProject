import requests
import json
import datetime as dt
import plotly.express as px
import plotly.offline as pyo
import pandas as pd

url = "https://global-warming.org/api/co2-api"
data = requests.get(url).json()['co2']
graph_data = []

for entry in data:
    day = int(entry["day"])
    month = int(entry["month"])
    year = int(entry["year"])
    ppm_CO2 = float(entry["trend"])
    date = dt.date(year, month, day)
    graph_data.append([date, ppm_CO2])

dataframe = pd.DataFrame(graph_data, columns=['Date', 'CO2 Level(ppm)'])
print(dataframe)

fig = px.scatter(dataframe, x='Date', y='CO2 Level(ppm)')
# Save the plot to an HTML file
pyo.plot(fig, filename='co2_emissions.html')




