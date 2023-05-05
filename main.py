import requests
import json
import datetime as dt
import plotly.express as px
import plotly.offline as pyo
import pandas as pd

# CO2 Emissions
url="https://global-warming.org/api/co2-api"
CO2_text=requests.get(url).json()['co2']
data=[]

for i in CO2_text:
  temp=[]
  temp.append(i['month']+'/'+i['day']+'/'+i['year'])
  temp.append(float(i['trend']))
  data.append(temp)

df = pd.DataFrame(data, columns=['Date', 'CO2 Level(ppm)'])
fig = px.line(df, x='Date', y="CO2 Level(ppm)")
pyo.plot(fig, filename='co2_emissions.html')

# NO Emissions
url = "https://global-warming.org/api/nitrous-oxide-api"
NO_text = requests.get(url).json()['nitrous'][1:]
data=[]
for i in NO_text:
  temp=[]
  temp.append(i['date'][5:]+'/'+i['date'][:4])
  temp.append(float(i['average']))
  data.append(temp)

df = pd.DataFrame(data, columns=['Date', 'NO Level(ppm)'])
fig = px.line(df, x='Date', y="NO Level(ppm)")
pyo.plot(fig, filename='no_emissions.html')

#Methane
url='https://global-warming.org/api/methane-api'
CH4_text=requests.get(url).json()['methane'][1:]
data=[]
for i in CH4_text:
  temp=[]
  temp.append(i['date'][5:]+'/'+i['date'][:4])
  temp.append(float(i['average']))
  data.append(temp)

df = pd.DataFrame(data, columns=['Date', 'CH4 Level(ppm)'])
fig = px.line(df, x='Date', y="CH4 Level(ppm)")
pyo.plot(fig, filename='ch4_emissions.html')

#Temperature
url="https://global-warming.org/api/temperature-api"
temperature_text=requests.get(url).json()['result']
data=[]
for i in temperature_text:
  temp=[]
  temp.append(i['time'][:])
  temp.append(float(i['station']))
  data.append(temp)

df = pd.DataFrame(data, columns=['Date', 'Temperature Increase (Celsius)'])
fig = px.line(df, x='Date', y="Temperature Increase (Celsius)")
pyo.plot(fig, filename='temp_change.html')

# Modified CO2 Dataframe
url="https://global-warming.org/api/co2-api"
CO2_text=requests.get(url).json()['co2']
data=[]
dates=[]

for i in CO2_text:
  temp=[]
  temp.append(i['month']+'/'+i['year'])
  year = int(i['year'])
  temp.append(float(i['trend']))
  if(not(temp[0] in dates) and year<2023):
    dates.append(temp[0])
    data.append(temp)

df_CO2 = pd.DataFrame(data, columns=['Date', 'CO2 Level(ppm)'])

# modified NO Dataframe
url='https://global-warming.org/api/nitrous-oxide-api'
NO_text=requests.get(url).json()['nitrous'][1:]
data=[]
for i in NO_text:
  temp=[]
  temp.append(i['date'][5:]+'/'+i['date'][:4])
  temp.append(float(i['average']))
  if(int(i['date'][:4])>=2013 and int(i['date'][:4])<=2022):
    data.append(temp)

df_NO= pd.DataFrame(data, columns=['Date', 'NO Level(ppm)'])


# modified ch4 dataframe
url='https://global-warming.org/api/methane-api'
CH4_text=requests.get(url).json()['methane'][1:]
data=[]
for i in CH4_text:
  temp=[]
  temp.append(i['date'][5:]+'/'+i['date'][:4])
  temp.append(float(i['average']))
  if(int(i['date'][:4])>=2013 and int(i['date'][:4])<=2022):
    data.append(temp)

df_CH4 = pd.DataFrame(data, columns=['Date', 'CH4 Level(ppm)'])


# modified temperature dataframe
url="https://global-warming.org/api/temperature-api"
temperature_text=requests.get(url).json()['result']
data=[]
for i in temperature_text:
  temp=[]
  year=int(i['time'][:4])
  if(year>=2013 and year<=2022):
    temp.append(str(len(data)%12+1)+'/'+str(year))
    temp.append(float(i['station']))
    data.append(temp)

df_temperature = pd.DataFrame(data, columns=['Date', 'Temperature Increase (Celsius)'])


# Temperature x emission
from plotly.subplots import make_subplots
data_all = {'Date': df_temperature['Date'],
          'CO2': df_CO2['CO2 Level(ppm)'],
          'NO' : df_NO['NO Level(ppm)'],
          'CH4': df_CH4['CH4 Level(ppm)']}
df_all=pd.DataFrame(data_all)

subfig = make_subplots(specs=[[{"secondary_y": True}]])
fig1 = px.line(df_all, x='Date', y=df_all.columns[1:4])
fig2 = px.line(df_temperature, x='Date', y=df_temperature['Temperature Increase (Celsius)'])
fig2.update_traces(yaxis='y2', line_color='#ff00ff')
subfig.layout.xaxis.title="Date"
subfig.layout.yaxis.title="Gas Emission (ppm)"
subfig.layout.yaxis2.title="Temperature Increase (Celsius)"
subfig.layout.yaxis2.color='magenta'
subfig.add_traces(fig1.data+fig2.data)
pyo.plot(subfig, filename='temp_emiss.html')

# Countries Chloropleth
countries_raw=[{"name":"Afghanistan","alpha-2":"AF","alpha-3":"AFG","country-code":"004","iso_3166-2":"ISO 3166-2:AF","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Åland Islands","alpha-2":"AX","alpha-3":"ALA","country-code":"248","iso_3166-2":"ISO 3166-2:AX","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Albania","alpha-2":"AL","alpha-3":"ALB","country-code":"008","iso_3166-2":"ISO 3166-2:AL","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Algeria","alpha-2":"DZ","alpha-3":"DZA","country-code":"012","iso_3166-2":"ISO 3166-2:DZ","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"American Samoa","alpha-2":"AS","alpha-3":"ASM","country-code":"016","iso_3166-2":"ISO 3166-2:AS","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Andorra","alpha-2":"AD","alpha-3":"AND","country-code":"020","iso_3166-2":"ISO 3166-2:AD","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Angola","alpha-2":"AO","alpha-3":"AGO","country-code":"024","iso_3166-2":"ISO 3166-2:AO","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Anguilla","alpha-2":"AI","alpha-3":"AIA","country-code":"660","iso_3166-2":"ISO 3166-2:AI","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Antarctica","alpha-2":"AQ","alpha-3":"ATA","country-code":"010","iso_3166-2":"ISO 3166-2:AQ","region":"","sub-region":"","intermediate-region":"","region-code":"","sub-region-code":"","intermediate-region-code":""},{"name":"Antigua and Barbuda","alpha-2":"AG","alpha-3":"ATG","country-code":"028","iso_3166-2":"ISO 3166-2:AG","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Argentina","alpha-2":"AR","alpha-3":"ARG","country-code":"032","iso_3166-2":"ISO 3166-2:AR","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Armenia","alpha-2":"AM","alpha-3":"ARM","country-code":"051","iso_3166-2":"ISO 3166-2:AM","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Aruba","alpha-2":"AW","alpha-3":"ABW","country-code":"533","iso_3166-2":"ISO 3166-2:AW","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Australia","alpha-2":"AU","alpha-3":"AUS","country-code":"036","iso_3166-2":"ISO 3166-2:AU","region":"Oceania","sub-region":"Australia and New Zealand","intermediate-region":"","region-code":"009","sub-region-code":"053","intermediate-region-code":""},{"name":"Austria","alpha-2":"AT","alpha-3":"AUT","country-code":"040","iso_3166-2":"ISO 3166-2:AT","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Azerbaijan","alpha-2":"AZ","alpha-3":"AZE","country-code":"031","iso_3166-2":"ISO 3166-2:AZ","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Bahamas","alpha-2":"BS","alpha-3":"BHS","country-code":"044","iso_3166-2":"ISO 3166-2:BS","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Bahrain","alpha-2":"BH","alpha-3":"BHR","country-code":"048","iso_3166-2":"ISO 3166-2:BH","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Bangladesh","alpha-2":"BD","alpha-3":"BGD","country-code":"050","iso_3166-2":"ISO 3166-2:BD","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Barbados","alpha-2":"BB","alpha-3":"BRB","country-code":"052","iso_3166-2":"ISO 3166-2:BB","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Belarus","alpha-2":"BY","alpha-3":"BLR","country-code":"112","iso_3166-2":"ISO 3166-2:BY","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Belgium","alpha-2":"BE","alpha-3":"BEL","country-code":"056","iso_3166-2":"ISO 3166-2:BE","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Belize","alpha-2":"BZ","alpha-3":"BLZ","country-code":"084","iso_3166-2":"ISO 3166-2:BZ","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Benin","alpha-2":"BJ","alpha-3":"BEN","country-code":"204","iso_3166-2":"ISO 3166-2:BJ","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Bermuda","alpha-2":"BM","alpha-3":"BMU","country-code":"060","iso_3166-2":"ISO 3166-2:BM","region":"Americas","sub-region":"Northern America","intermediate-region":"","region-code":"019","sub-region-code":"021","intermediate-region-code":""},{"name":"Bhutan","alpha-2":"BT","alpha-3":"BTN","country-code":"064","iso_3166-2":"ISO 3166-2:BT","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Bolivia (Plurinational State of)","alpha-2":"BO","alpha-3":"BOL","country-code":"068","iso_3166-2":"ISO 3166-2:BO","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Bonaire, Sint Eustatius and Saba","alpha-2":"BQ","alpha-3":"BES","country-code":"535","iso_3166-2":"ISO 3166-2:BQ","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Bosnia and Herzegovina","alpha-2":"BA","alpha-3":"BIH","country-code":"070","iso_3166-2":"ISO 3166-2:BA","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Botswana","alpha-2":"BW","alpha-3":"BWA","country-code":"072","iso_3166-2":"ISO 3166-2:BW","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Southern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"018"},{"name":"Bouvet Island","alpha-2":"BV","alpha-3":"BVT","country-code":"074","iso_3166-2":"ISO 3166-2:BV","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Brazil","alpha-2":"BR","alpha-3":"BRA","country-code":"076","iso_3166-2":"ISO 3166-2:BR","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"British Indian Ocean Territory","alpha-2":"IO","alpha-3":"IOT","country-code":"086","iso_3166-2":"ISO 3166-2:IO","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Brunei Darussalam","alpha-2":"BN","alpha-3":"BRN","country-code":"096","iso_3166-2":"ISO 3166-2:BN","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Bulgaria","alpha-2":"BG","alpha-3":"BGR","country-code":"100","iso_3166-2":"ISO 3166-2:BG","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Burkina Faso","alpha-2":"BF","alpha-3":"BFA","country-code":"854","iso_3166-2":"ISO 3166-2:BF","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Burundi","alpha-2":"BI","alpha-3":"BDI","country-code":"108","iso_3166-2":"ISO 3166-2:BI","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Cabo Verde","alpha-2":"CV","alpha-3":"CPV","country-code":"132","iso_3166-2":"ISO 3166-2:CV","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Cambodia","alpha-2":"KH","alpha-3":"KHM","country-code":"116","iso_3166-2":"ISO 3166-2:KH","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Cameroon","alpha-2":"CM","alpha-3":"CMR","country-code":"120","iso_3166-2":"ISO 3166-2:CM","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Canada","alpha-2":"CA","alpha-3":"CAN","country-code":"124","iso_3166-2":"ISO 3166-2:CA","region":"Americas","sub-region":"Northern America","intermediate-region":"","region-code":"019","sub-region-code":"021","intermediate-region-code":""},{"name":"Cayman Islands","alpha-2":"KY","alpha-3":"CYM","country-code":"136","iso_3166-2":"ISO 3166-2:KY","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Central African Republic","alpha-2":"CF","alpha-3":"CAF","country-code":"140","iso_3166-2":"ISO 3166-2:CF","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Chad","alpha-2":"TD","alpha-3":"TCD","country-code":"148","iso_3166-2":"ISO 3166-2:TD","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Chile","alpha-2":"CL","alpha-3":"CHL","country-code":"152","iso_3166-2":"ISO 3166-2:CL","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"China","alpha-2":"CN","alpha-3":"CHN","country-code":"156","iso_3166-2":"ISO 3166-2:CN","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Christmas Island","alpha-2":"CX","alpha-3":"CXR","country-code":"162","iso_3166-2":"ISO 3166-2:CX","region":"Oceania","sub-region":"Australia and New Zealand","intermediate-region":"","region-code":"009","sub-region-code":"053","intermediate-region-code":""},{"name":"Cocos (Keeling) Islands","alpha-2":"CC","alpha-3":"CCK","country-code":"166","iso_3166-2":"ISO 3166-2:CC","region":"Oceania","sub-region":"Australia and New Zealand","intermediate-region":"","region-code":"009","sub-region-code":"053","intermediate-region-code":""},{"name":"Colombia","alpha-2":"CO","alpha-3":"COL","country-code":"170","iso_3166-2":"ISO 3166-2:CO","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Comoros","alpha-2":"KM","alpha-3":"COM","country-code":"174","iso_3166-2":"ISO 3166-2:KM","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Congo","alpha-2":"CG","alpha-3":"COG","country-code":"178","iso_3166-2":"ISO 3166-2:CG","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Congo, Democratic Republic of the","alpha-2":"CD","alpha-3":"COD","country-code":"180","iso_3166-2":"ISO 3166-2:CD","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Cook Islands","alpha-2":"CK","alpha-3":"COK","country-code":"184","iso_3166-2":"ISO 3166-2:CK","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Costa Rica","alpha-2":"CR","alpha-3":"CRI","country-code":"188","iso_3166-2":"ISO 3166-2:CR","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Côte d'Ivoire","alpha-2":"CI","alpha-3":"CIV","country-code":"384","iso_3166-2":"ISO 3166-2:CI","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Croatia","alpha-2":"HR","alpha-3":"HRV","country-code":"191","iso_3166-2":"ISO 3166-2:HR","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Cuba","alpha-2":"CU","alpha-3":"CUB","country-code":"192","iso_3166-2":"ISO 3166-2:CU","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Curaçao","alpha-2":"CW","alpha-3":"CUW","country-code":"531","iso_3166-2":"ISO 3166-2:CW","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Cyprus","alpha-2":"CY","alpha-3":"CYP","country-code":"196","iso_3166-2":"ISO 3166-2:CY","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Czechia","alpha-2":"CZ","alpha-3":"CZE","country-code":"203","iso_3166-2":"ISO 3166-2:CZ","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Denmark","alpha-2":"DK","alpha-3":"DNK","country-code":"208","iso_3166-2":"ISO 3166-2:DK","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Djibouti","alpha-2":"DJ","alpha-3":"DJI","country-code":"262","iso_3166-2":"ISO 3166-2:DJ","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Dominica","alpha-2":"DM","alpha-3":"DMA","country-code":"212","iso_3166-2":"ISO 3166-2:DM","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Dominican Republic","alpha-2":"DO","alpha-3":"DOM","country-code":"214","iso_3166-2":"ISO 3166-2:DO","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Ecuador","alpha-2":"EC","alpha-3":"ECU","country-code":"218","iso_3166-2":"ISO 3166-2:EC","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Egypt","alpha-2":"EG","alpha-3":"EGY","country-code":"818","iso_3166-2":"ISO 3166-2:EG","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"El Salvador","alpha-2":"SV","alpha-3":"SLV","country-code":"222","iso_3166-2":"ISO 3166-2:SV","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Equatorial Guinea","alpha-2":"GQ","alpha-3":"GNQ","country-code":"226","iso_3166-2":"ISO 3166-2:GQ","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Eritrea","alpha-2":"ER","alpha-3":"ERI","country-code":"232","iso_3166-2":"ISO 3166-2:ER","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Estonia","alpha-2":"EE","alpha-3":"EST","country-code":"233","iso_3166-2":"ISO 3166-2:EE","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Eswatini","alpha-2":"SZ","alpha-3":"SWZ","country-code":"748","iso_3166-2":"ISO 3166-2:SZ","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Southern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"018"},{"name":"Ethiopia","alpha-2":"ET","alpha-3":"ETH","country-code":"231","iso_3166-2":"ISO 3166-2:ET","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Falkland Islands (Malvinas)","alpha-2":"FK","alpha-3":"FLK","country-code":"238","iso_3166-2":"ISO 3166-2:FK","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Faroe Islands","alpha-2":"FO","alpha-3":"FRO","country-code":"234","iso_3166-2":"ISO 3166-2:FO","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Fiji","alpha-2":"FJ","alpha-3":"FJI","country-code":"242","iso_3166-2":"ISO 3166-2:FJ","region":"Oceania","sub-region":"Melanesia","intermediate-region":"","region-code":"009","sub-region-code":"054","intermediate-region-code":""},{"name":"Finland","alpha-2":"FI","alpha-3":"FIN","country-code":"246","iso_3166-2":"ISO 3166-2:FI","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"France","alpha-2":"FR","alpha-3":"FRA","country-code":"250","iso_3166-2":"ISO 3166-2:FR","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"French Guiana","alpha-2":"GF","alpha-3":"GUF","country-code":"254","iso_3166-2":"ISO 3166-2:GF","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"French Polynesia","alpha-2":"PF","alpha-3":"PYF","country-code":"258","iso_3166-2":"ISO 3166-2:PF","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"French Southern Territories","alpha-2":"TF","alpha-3":"ATF","country-code":"260","iso_3166-2":"ISO 3166-2:TF","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Gabon","alpha-2":"GA","alpha-3":"GAB","country-code":"266","iso_3166-2":"ISO 3166-2:GA","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Gambia","alpha-2":"GM","alpha-3":"GMB","country-code":"270","iso_3166-2":"ISO 3166-2:GM","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Georgia","alpha-2":"GE","alpha-3":"GEO","country-code":"268","iso_3166-2":"ISO 3166-2:GE","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Germany","alpha-2":"DE","alpha-3":"DEU","country-code":"276","iso_3166-2":"ISO 3166-2:DE","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Ghana","alpha-2":"GH","alpha-3":"GHA","country-code":"288","iso_3166-2":"ISO 3166-2:GH","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Gibraltar","alpha-2":"GI","alpha-3":"GIB","country-code":"292","iso_3166-2":"ISO 3166-2:GI","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Greece","alpha-2":"GR","alpha-3":"GRC","country-code":"300","iso_3166-2":"ISO 3166-2:GR","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Greenland","alpha-2":"GL","alpha-3":"GRL","country-code":"304","iso_3166-2":"ISO 3166-2:GL","region":"Americas","sub-region":"Northern America","intermediate-region":"","region-code":"019","sub-region-code":"021","intermediate-region-code":""},{"name":"Grenada","alpha-2":"GD","alpha-3":"GRD","country-code":"308","iso_3166-2":"ISO 3166-2:GD","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Guadeloupe","alpha-2":"GP","alpha-3":"GLP","country-code":"312","iso_3166-2":"ISO 3166-2:GP","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Guam","alpha-2":"GU","alpha-3":"GUM","country-code":"316","iso_3166-2":"ISO 3166-2:GU","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Guatemala","alpha-2":"GT","alpha-3":"GTM","country-code":"320","iso_3166-2":"ISO 3166-2:GT","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Guernsey","alpha-2":"GG","alpha-3":"GGY","country-code":"831","iso_3166-2":"ISO 3166-2:GG","region":"Europe","sub-region":"Northern Europe","intermediate-region":"Channel Islands","region-code":"150","sub-region-code":"154","intermediate-region-code":"830"},{"name":"Guinea","alpha-2":"GN","alpha-3":"GIN","country-code":"324","iso_3166-2":"ISO 3166-2:GN","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Guinea-Bissau","alpha-2":"GW","alpha-3":"GNB","country-code":"624","iso_3166-2":"ISO 3166-2:GW","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Guyana","alpha-2":"GY","alpha-3":"GUY","country-code":"328","iso_3166-2":"ISO 3166-2:GY","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Haiti","alpha-2":"HT","alpha-3":"HTI","country-code":"332","iso_3166-2":"ISO 3166-2:HT","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Heard Island and McDonald Islands","alpha-2":"HM","alpha-3":"HMD","country-code":"334","iso_3166-2":"ISO 3166-2:HM","region":"Oceania","sub-region":"Australia and New Zealand","intermediate-region":"","region-code":"009","sub-region-code":"053","intermediate-region-code":""},{"name":"Holy See","alpha-2":"VA","alpha-3":"VAT","country-code":"336","iso_3166-2":"ISO 3166-2:VA","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Honduras","alpha-2":"HN","alpha-3":"HND","country-code":"340","iso_3166-2":"ISO 3166-2:HN","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Hong Kong","alpha-2":"HK","alpha-3":"HKG","country-code":"344","iso_3166-2":"ISO 3166-2:HK","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Hungary","alpha-2":"HU","alpha-3":"HUN","country-code":"348","iso_3166-2":"ISO 3166-2:HU","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Iceland","alpha-2":"IS","alpha-3":"ISL","country-code":"352","iso_3166-2":"ISO 3166-2:IS","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"India","alpha-2":"IN","alpha-3":"IND","country-code":"356","iso_3166-2":"ISO 3166-2:IN","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Indonesia","alpha-2":"ID","alpha-3":"IDN","country-code":"360","iso_3166-2":"ISO 3166-2:ID","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Iran (Islamic Republic of)","alpha-2":"IR","alpha-3":"IRN","country-code":"364","iso_3166-2":"ISO 3166-2:IR","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Iraq","alpha-2":"IQ","alpha-3":"IRQ","country-code":"368","iso_3166-2":"ISO 3166-2:IQ","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Ireland","alpha-2":"IE","alpha-3":"IRL","country-code":"372","iso_3166-2":"ISO 3166-2:IE","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Isle of Man","alpha-2":"IM","alpha-3":"IMN","country-code":"833","iso_3166-2":"ISO 3166-2:IM","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Israel","alpha-2":"IL","alpha-3":"ISR","country-code":"376","iso_3166-2":"ISO 3166-2:IL","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Italy","alpha-2":"IT","alpha-3":"ITA","country-code":"380","iso_3166-2":"ISO 3166-2:IT","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Jamaica","alpha-2":"JM","alpha-3":"JAM","country-code":"388","iso_3166-2":"ISO 3166-2:JM","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Japan","alpha-2":"JP","alpha-3":"JPN","country-code":"392","iso_3166-2":"ISO 3166-2:JP","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Jersey","alpha-2":"JE","alpha-3":"JEY","country-code":"832","iso_3166-2":"ISO 3166-2:JE","region":"Europe","sub-region":"Northern Europe","intermediate-region":"Channel Islands","region-code":"150","sub-region-code":"154","intermediate-region-code":"830"},{"name":"Jordan","alpha-2":"JO","alpha-3":"JOR","country-code":"400","iso_3166-2":"ISO 3166-2:JO","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Kazakhstan","alpha-2":"KZ","alpha-3":"KAZ","country-code":"398","iso_3166-2":"ISO 3166-2:KZ","region":"Asia","sub-region":"Central Asia","intermediate-region":"","region-code":"142","sub-region-code":"143","intermediate-region-code":""},{"name":"Kenya","alpha-2":"KE","alpha-3":"KEN","country-code":"404","iso_3166-2":"ISO 3166-2:KE","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Kiribati","alpha-2":"KI","alpha-3":"KIR","country-code":"296","iso_3166-2":"ISO 3166-2:KI","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Korea (Democratic People's Republic of)","alpha-2":"KP","alpha-3":"PRK","country-code":"408","iso_3166-2":"ISO 3166-2:KP","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Korea, Republic of","alpha-2":"KR","alpha-3":"KOR","country-code":"410","iso_3166-2":"ISO 3166-2:KR","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Kuwait","alpha-2":"KW","alpha-3":"KWT","country-code":"414","iso_3166-2":"ISO 3166-2:KW","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Kyrgyzstan","alpha-2":"KG","alpha-3":"KGZ","country-code":"417","iso_3166-2":"ISO 3166-2:KG","region":"Asia","sub-region":"Central Asia","intermediate-region":"","region-code":"142","sub-region-code":"143","intermediate-region-code":""},{"name":"Lao People's Democratic Republic","alpha-2":"LA","alpha-3":"LAO","country-code":"418","iso_3166-2":"ISO 3166-2:LA","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Latvia","alpha-2":"LV","alpha-3":"LVA","country-code":"428","iso_3166-2":"ISO 3166-2:LV","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Lebanon","alpha-2":"LB","alpha-3":"LBN","country-code":"422","iso_3166-2":"ISO 3166-2:LB","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Lesotho","alpha-2":"LS","alpha-3":"LSO","country-code":"426","iso_3166-2":"ISO 3166-2:LS","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Southern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"018"},{"name":"Liberia","alpha-2":"LR","alpha-3":"LBR","country-code":"430","iso_3166-2":"ISO 3166-2:LR","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Libya","alpha-2":"LY","alpha-3":"LBY","country-code":"434","iso_3166-2":"ISO 3166-2:LY","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"Liechtenstein","alpha-2":"LI","alpha-3":"LIE","country-code":"438","iso_3166-2":"ISO 3166-2:LI","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Lithuania","alpha-2":"LT","alpha-3":"LTU","country-code":"440","iso_3166-2":"ISO 3166-2:LT","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Luxembourg","alpha-2":"LU","alpha-3":"LUX","country-code":"442","iso_3166-2":"ISO 3166-2:LU","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Macao","alpha-2":"MO","alpha-3":"MAC","country-code":"446","iso_3166-2":"ISO 3166-2:MO","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Madagascar","alpha-2":"MG","alpha-3":"MDG","country-code":"450","iso_3166-2":"ISO 3166-2:MG","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Malawi","alpha-2":"MW","alpha-3":"MWI","country-code":"454","iso_3166-2":"ISO 3166-2:MW","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Malaysia","alpha-2":"MY","alpha-3":"MYS","country-code":"458","iso_3166-2":"ISO 3166-2:MY","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Maldives","alpha-2":"MV","alpha-3":"MDV","country-code":"462","iso_3166-2":"ISO 3166-2:MV","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Mali","alpha-2":"ML","alpha-3":"MLI","country-code":"466","iso_3166-2":"ISO 3166-2:ML","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Malta","alpha-2":"MT","alpha-3":"MLT","country-code":"470","iso_3166-2":"ISO 3166-2:MT","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Marshall Islands","alpha-2":"MH","alpha-3":"MHL","country-code":"584","iso_3166-2":"ISO 3166-2:MH","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Martinique","alpha-2":"MQ","alpha-3":"MTQ","country-code":"474","iso_3166-2":"ISO 3166-2:MQ","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Mauritania","alpha-2":"MR","alpha-3":"MRT","country-code":"478","iso_3166-2":"ISO 3166-2:MR","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Mauritius","alpha-2":"MU","alpha-3":"MUS","country-code":"480","iso_3166-2":"ISO 3166-2:MU","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Mayotte","alpha-2":"YT","alpha-3":"MYT","country-code":"175","iso_3166-2":"ISO 3166-2:YT","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Mexico","alpha-2":"MX","alpha-3":"MEX","country-code":"484","iso_3166-2":"ISO 3166-2:MX","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Micronesia (Federated States of)","alpha-2":"FM","alpha-3":"FSM","country-code":"583","iso_3166-2":"ISO 3166-2:FM","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Moldova, Republic of","alpha-2":"MD","alpha-3":"MDA","country-code":"498","iso_3166-2":"ISO 3166-2:MD","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Monaco","alpha-2":"MC","alpha-3":"MCO","country-code":"492","iso_3166-2":"ISO 3166-2:MC","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Mongolia","alpha-2":"MN","alpha-3":"MNG","country-code":"496","iso_3166-2":"ISO 3166-2:MN","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Montenegro","alpha-2":"ME","alpha-3":"MNE","country-code":"499","iso_3166-2":"ISO 3166-2:ME","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Montserrat","alpha-2":"MS","alpha-3":"MSR","country-code":"500","iso_3166-2":"ISO 3166-2:MS","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Morocco","alpha-2":"MA","alpha-3":"MAR","country-code":"504","iso_3166-2":"ISO 3166-2:MA","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"Mozambique","alpha-2":"MZ","alpha-3":"MOZ","country-code":"508","iso_3166-2":"ISO 3166-2:MZ","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Myanmar","alpha-2":"MM","alpha-3":"MMR","country-code":"104","iso_3166-2":"ISO 3166-2:MM","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Namibia","alpha-2":"NA","alpha-3":"NAM","country-code":"516","iso_3166-2":"ISO 3166-2:NA","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Southern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"018"},{"name":"Nauru","alpha-2":"NR","alpha-3":"NRU","country-code":"520","iso_3166-2":"ISO 3166-2:NR","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Nepal","alpha-2":"NP","alpha-3":"NPL","country-code":"524","iso_3166-2":"ISO 3166-2:NP","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Netherlands","alpha-2":"NL","alpha-3":"NLD","country-code":"528","iso_3166-2":"ISO 3166-2:NL","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"New Caledonia","alpha-2":"NC","alpha-3":"NCL","country-code":"540","iso_3166-2":"ISO 3166-2:NC","region":"Oceania","sub-region":"Melanesia","intermediate-region":"","region-code":"009","sub-region-code":"054","intermediate-region-code":""},{"name":"New Zealand","alpha-2":"NZ","alpha-3":"NZL","country-code":"554","iso_3166-2":"ISO 3166-2:NZ","region":"Oceania","sub-region":"Australia and New Zealand","intermediate-region":"","region-code":"009","sub-region-code":"053","intermediate-region-code":""},{"name":"Nicaragua","alpha-2":"NI","alpha-3":"NIC","country-code":"558","iso_3166-2":"ISO 3166-2:NI","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Niger","alpha-2":"NE","alpha-3":"NER","country-code":"562","iso_3166-2":"ISO 3166-2:NE","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Nigeria","alpha-2":"NG","alpha-3":"NGA","country-code":"566","iso_3166-2":"ISO 3166-2:NG","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Niue","alpha-2":"NU","alpha-3":"NIU","country-code":"570","iso_3166-2":"ISO 3166-2:NU","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Norfolk Island","alpha-2":"NF","alpha-3":"NFK","country-code":"574","iso_3166-2":"ISO 3166-2:NF","region":"Oceania","sub-region":"Australia and New Zealand","intermediate-region":"","region-code":"009","sub-region-code":"053","intermediate-region-code":""},{"name":"North Macedonia","alpha-2":"MK","alpha-3":"MKD","country-code":"807","iso_3166-2":"ISO 3166-2:MK","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Northern Mariana Islands","alpha-2":"MP","alpha-3":"MNP","country-code":"580","iso_3166-2":"ISO 3166-2:MP","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Norway","alpha-2":"NO","alpha-3":"NOR","country-code":"578","iso_3166-2":"ISO 3166-2:NO","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Oman","alpha-2":"OM","alpha-3":"OMN","country-code":"512","iso_3166-2":"ISO 3166-2:OM","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Pakistan","alpha-2":"PK","alpha-3":"PAK","country-code":"586","iso_3166-2":"ISO 3166-2:PK","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Palau","alpha-2":"PW","alpha-3":"PLW","country-code":"585","iso_3166-2":"ISO 3166-2:PW","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Palestine, State of","alpha-2":"PS","alpha-3":"PSE","country-code":"275","iso_3166-2":"ISO 3166-2:PS","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Panama","alpha-2":"PA","alpha-3":"PAN","country-code":"591","iso_3166-2":"ISO 3166-2:PA","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Central America","region-code":"019","sub-region-code":"419","intermediate-region-code":"013"},{"name":"Papua New Guinea","alpha-2":"PG","alpha-3":"PNG","country-code":"598","iso_3166-2":"ISO 3166-2:PG","region":"Oceania","sub-region":"Melanesia","intermediate-region":"","region-code":"009","sub-region-code":"054","intermediate-region-code":""},{"name":"Paraguay","alpha-2":"PY","alpha-3":"PRY","country-code":"600","iso_3166-2":"ISO 3166-2:PY","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Peru","alpha-2":"PE","alpha-3":"PER","country-code":"604","iso_3166-2":"ISO 3166-2:PE","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Philippines","alpha-2":"PH","alpha-3":"PHL","country-code":"608","iso_3166-2":"ISO 3166-2:PH","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Pitcairn","alpha-2":"PN","alpha-3":"PCN","country-code":"612","iso_3166-2":"ISO 3166-2:PN","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Poland","alpha-2":"PL","alpha-3":"POL","country-code":"616","iso_3166-2":"ISO 3166-2:PL","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Portugal","alpha-2":"PT","alpha-3":"PRT","country-code":"620","iso_3166-2":"ISO 3166-2:PT","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Puerto Rico","alpha-2":"PR","alpha-3":"PRI","country-code":"630","iso_3166-2":"ISO 3166-2:PR","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Qatar","alpha-2":"QA","alpha-3":"QAT","country-code":"634","iso_3166-2":"ISO 3166-2:QA","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Réunion","alpha-2":"RE","alpha-3":"REU","country-code":"638","iso_3166-2":"ISO 3166-2:RE","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Romania","alpha-2":"RO","alpha-3":"ROU","country-code":"642","iso_3166-2":"ISO 3166-2:RO","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Russian Federation","alpha-2":"RU","alpha-3":"RUS","country-code":"643","iso_3166-2":"ISO 3166-2:RU","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Rwanda","alpha-2":"RW","alpha-3":"RWA","country-code":"646","iso_3166-2":"ISO 3166-2:RW","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Saint Barthélemy","alpha-2":"BL","alpha-3":"BLM","country-code":"652","iso_3166-2":"ISO 3166-2:BL","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Saint Helena, Ascension and Tristan da Cunha","alpha-2":"SH","alpha-3":"SHN","country-code":"654","iso_3166-2":"ISO 3166-2:SH","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Saint Kitts and Nevis","alpha-2":"KN","alpha-3":"KNA","country-code":"659","iso_3166-2":"ISO 3166-2:KN","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Saint Lucia","alpha-2":"LC","alpha-3":"LCA","country-code":"662","iso_3166-2":"ISO 3166-2:LC","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Saint Martin (French part)","alpha-2":"MF","alpha-3":"MAF","country-code":"663","iso_3166-2":"ISO 3166-2:MF","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Saint Pierre and Miquelon","alpha-2":"PM","alpha-3":"SPM","country-code":"666","iso_3166-2":"ISO 3166-2:PM","region":"Americas","sub-region":"Northern America","intermediate-region":"","region-code":"019","sub-region-code":"021","intermediate-region-code":""},{"name":"Saint Vincent and the Grenadines","alpha-2":"VC","alpha-3":"VCT","country-code":"670","iso_3166-2":"ISO 3166-2:VC","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Samoa","alpha-2":"WS","alpha-3":"WSM","country-code":"882","iso_3166-2":"ISO 3166-2:WS","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"San Marino","alpha-2":"SM","alpha-3":"SMR","country-code":"674","iso_3166-2":"ISO 3166-2:SM","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Sao Tome and Principe","alpha-2":"ST","alpha-3":"STP","country-code":"678","iso_3166-2":"ISO 3166-2:ST","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Middle Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"017"},{"name":"Saudi Arabia","alpha-2":"SA","alpha-3":"SAU","country-code":"682","iso_3166-2":"ISO 3166-2:SA","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Senegal","alpha-2":"SN","alpha-3":"SEN","country-code":"686","iso_3166-2":"ISO 3166-2:SN","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Serbia","alpha-2":"RS","alpha-3":"SRB","country-code":"688","iso_3166-2":"ISO 3166-2:RS","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Seychelles","alpha-2":"SC","alpha-3":"SYC","country-code":"690","iso_3166-2":"ISO 3166-2:SC","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Sierra Leone","alpha-2":"SL","alpha-3":"SLE","country-code":"694","iso_3166-2":"ISO 3166-2:SL","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Singapore","alpha-2":"SG","alpha-3":"SGP","country-code":"702","iso_3166-2":"ISO 3166-2:SG","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Sint Maarten (Dutch part)","alpha-2":"SX","alpha-3":"SXM","country-code":"534","iso_3166-2":"ISO 3166-2:SX","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Slovakia","alpha-2":"SK","alpha-3":"SVK","country-code":"703","iso_3166-2":"ISO 3166-2:SK","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"Slovenia","alpha-2":"SI","alpha-3":"SVN","country-code":"705","iso_3166-2":"ISO 3166-2:SI","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Solomon Islands","alpha-2":"SB","alpha-3":"SLB","country-code":"090","iso_3166-2":"ISO 3166-2:SB","region":"Oceania","sub-region":"Melanesia","intermediate-region":"","region-code":"009","sub-region-code":"054","intermediate-region-code":""},{"name":"Somalia","alpha-2":"SO","alpha-3":"SOM","country-code":"706","iso_3166-2":"ISO 3166-2:SO","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"South Africa","alpha-2":"ZA","alpha-3":"ZAF","country-code":"710","iso_3166-2":"ISO 3166-2:ZA","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Southern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"018"},{"name":"South Georgia and the South Sandwich Islands","alpha-2":"GS","alpha-3":"SGS","country-code":"239","iso_3166-2":"ISO 3166-2:GS","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"South Sudan","alpha-2":"SS","alpha-3":"SSD","country-code":"728","iso_3166-2":"ISO 3166-2:SS","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Spain","alpha-2":"ES","alpha-3":"ESP","country-code":"724","iso_3166-2":"ISO 3166-2:ES","region":"Europe","sub-region":"Southern Europe","intermediate-region":"","region-code":"150","sub-region-code":"039","intermediate-region-code":""},{"name":"Sri Lanka","alpha-2":"LK","alpha-3":"LKA","country-code":"144","iso_3166-2":"ISO 3166-2:LK","region":"Asia","sub-region":"Southern Asia","intermediate-region":"","region-code":"142","sub-region-code":"034","intermediate-region-code":""},{"name":"Sudan","alpha-2":"SD","alpha-3":"SDN","country-code":"729","iso_3166-2":"ISO 3166-2:SD","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"Suriname","alpha-2":"SR","alpha-3":"SUR","country-code":"740","iso_3166-2":"ISO 3166-2:SR","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Svalbard and Jan Mayen","alpha-2":"SJ","alpha-3":"SJM","country-code":"744","iso_3166-2":"ISO 3166-2:SJ","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Sweden","alpha-2":"SE","alpha-3":"SWE","country-code":"752","iso_3166-2":"ISO 3166-2:SE","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"Switzerland","alpha-2":"CH","alpha-3":"CHE","country-code":"756","iso_3166-2":"ISO 3166-2:CH","region":"Europe","sub-region":"Western Europe","intermediate-region":"","region-code":"150","sub-region-code":"155","intermediate-region-code":""},{"name":"Syrian Arab Republic","alpha-2":"SY","alpha-3":"SYR","country-code":"760","iso_3166-2":"ISO 3166-2:SY","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Taiwan, Province of China","alpha-2":"TW","alpha-3":"TWN","country-code":"158","iso_3166-2":"ISO 3166-2:TW","region":"Asia","sub-region":"Eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"030","intermediate-region-code":""},{"name":"Tajikistan","alpha-2":"TJ","alpha-3":"TJK","country-code":"762","iso_3166-2":"ISO 3166-2:TJ","region":"Asia","sub-region":"Central Asia","intermediate-region":"","region-code":"142","sub-region-code":"143","intermediate-region-code":""},{"name":"Tanzania, United Republic of","alpha-2":"TZ","alpha-3":"TZA","country-code":"834","iso_3166-2":"ISO 3166-2:TZ","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Thailand","alpha-2":"TH","alpha-3":"THA","country-code":"764","iso_3166-2":"ISO 3166-2:TH","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Timor-Leste","alpha-2":"TL","alpha-3":"TLS","country-code":"626","iso_3166-2":"ISO 3166-2:TL","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Togo","alpha-2":"TG","alpha-3":"TGO","country-code":"768","iso_3166-2":"ISO 3166-2:TG","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Western Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"011"},{"name":"Tokelau","alpha-2":"TK","alpha-3":"TKL","country-code":"772","iso_3166-2":"ISO 3166-2:TK","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Tonga","alpha-2":"TO","alpha-3":"TON","country-code":"776","iso_3166-2":"ISO 3166-2:TO","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Trinidad and Tobago","alpha-2":"TT","alpha-3":"TTO","country-code":"780","iso_3166-2":"ISO 3166-2:TT","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Tunisia","alpha-2":"TN","alpha-3":"TUN","country-code":"788","iso_3166-2":"ISO 3166-2:TN","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"Turkey","alpha-2":"TR","alpha-3":"TUR","country-code":"792","iso_3166-2":"ISO 3166-2:TR","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Turkmenistan","alpha-2":"TM","alpha-3":"TKM","country-code":"795","iso_3166-2":"ISO 3166-2:TM","region":"Asia","sub-region":"Central Asia","intermediate-region":"","region-code":"142","sub-region-code":"143","intermediate-region-code":""},{"name":"Turks and Caicos Islands","alpha-2":"TC","alpha-3":"TCA","country-code":"796","iso_3166-2":"ISO 3166-2:TC","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Tuvalu","alpha-2":"TV","alpha-3":"TUV","country-code":"798","iso_3166-2":"ISO 3166-2:TV","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Uganda","alpha-2":"UG","alpha-3":"UGA","country-code":"800","iso_3166-2":"ISO 3166-2:UG","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Ukraine","alpha-2":"UA","alpha-3":"UKR","country-code":"804","iso_3166-2":"ISO 3166-2:UA","region":"Europe","sub-region":"Eastern Europe","intermediate-region":"","region-code":"150","sub-region-code":"151","intermediate-region-code":""},{"name":"United Arab Emirates","alpha-2":"AE","alpha-3":"ARE","country-code":"784","iso_3166-2":"ISO 3166-2:AE","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"United Kingdom of Great Britain and Northern Ireland","alpha-2":"GB","alpha-3":"GBR","country-code":"826","iso_3166-2":"ISO 3166-2:GB","region":"Europe","sub-region":"Northern Europe","intermediate-region":"","region-code":"150","sub-region-code":"154","intermediate-region-code":""},{"name":"United States of America","alpha-2":"US","alpha-3":"USA","country-code":"840","iso_3166-2":"ISO 3166-2:US","region":"Americas","sub-region":"Northern America","intermediate-region":"","region-code":"019","sub-region-code":"021","intermediate-region-code":""},{"name":"United States Minor Outlying Islands","alpha-2":"UM","alpha-3":"UMI","country-code":"581","iso_3166-2":"ISO 3166-2:UM","region":"Oceania","sub-region":"Micronesia","intermediate-region":"","region-code":"009","sub-region-code":"057","intermediate-region-code":""},{"name":"Uruguay","alpha-2":"UY","alpha-3":"URY","country-code":"858","iso_3166-2":"ISO 3166-2:UY","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Uzbekistan","alpha-2":"UZ","alpha-3":"UZB","country-code":"860","iso_3166-2":"ISO 3166-2:UZ","region":"Asia","sub-region":"Central Asia","intermediate-region":"","region-code":"142","sub-region-code":"143","intermediate-region-code":""},{"name":"Vanuatu","alpha-2":"VU","alpha-3":"VUT","country-code":"548","iso_3166-2":"ISO 3166-2:VU","region":"Oceania","sub-region":"Melanesia","intermediate-region":"","region-code":"009","sub-region-code":"054","intermediate-region-code":""},{"name":"Venezuela (Bolivarian Republic of)","alpha-2":"VE","alpha-3":"VEN","country-code":"862","iso_3166-2":"ISO 3166-2:VE","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"South America","region-code":"019","sub-region-code":"419","intermediate-region-code":"005"},{"name":"Viet Nam","alpha-2":"VN","alpha-3":"VNM","country-code":"704","iso_3166-2":"ISO 3166-2:VN","region":"Asia","sub-region":"South-eastern Asia","intermediate-region":"","region-code":"142","sub-region-code":"035","intermediate-region-code":""},{"name":"Virgin Islands (British)","alpha-2":"VG","alpha-3":"VGB","country-code":"092","iso_3166-2":"ISO 3166-2:VG","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Virgin Islands (U.S.)","alpha-2":"VI","alpha-3":"VIR","country-code":"850","iso_3166-2":"ISO 3166-2:VI","region":"Americas","sub-region":"Latin America and the Caribbean","intermediate-region":"Caribbean","region-code":"019","sub-region-code":"419","intermediate-region-code":"029"},{"name":"Wallis and Futuna","alpha-2":"WF","alpha-3":"WLF","country-code":"876","iso_3166-2":"ISO 3166-2:WF","region":"Oceania","sub-region":"Polynesia","intermediate-region":"","region-code":"009","sub-region-code":"061","intermediate-region-code":""},{"name":"Western Sahara","alpha-2":"EH","alpha-3":"ESH","country-code":"732","iso_3166-2":"ISO 3166-2:EH","region":"Africa","sub-region":"Northern Africa","intermediate-region":"","region-code":"002","sub-region-code":"015","intermediate-region-code":""},{"name":"Yemen","alpha-2":"YE","alpha-3":"YEM","country-code":"887","iso_3166-2":"ISO 3166-2:YE","region":"Asia","sub-region":"Western Asia","intermediate-region":"","region-code":"142","sub-region-code":"145","intermediate-region-code":""},{"name":"Zambia","alpha-2":"ZM","alpha-3":"ZMB","country-code":"894","iso_3166-2":"ISO 3166-2:ZM","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"},{"name":"Zimbabwe","alpha-2":"ZW","alpha-3":"ZWE","country-code":"716","iso_3166-2":"ISO 3166-2:ZW","region":"Africa","sub-region":"Sub-Saharan Africa","intermediate-region":"Eastern Africa","region-code":"002","sub-region-code":"202","intermediate-region-code":"014"}]

countries = {
	'AD': 'Andorra',
	'AE': 'United Arab Emirates',
	'AF': 'Afghanistan',
	'AG': 'Antigua & Barbuda',
	'AI': 'Anguilla',
	'AL': 'Albania',
	'AM': 'Armenia',
	'AN': 'Netherlands Antilles',
	'AO': 'Angola',
	'AQ': 'Antarctica',
	'AR': 'Argentina',
	'AS': 'American Samoa',
	'AT': 'Austria',
	'AU': 'Australia',
	'AW': 'Aruba',
	'AZ': 'Azerbaijan',
	'BA': 'Bosnia and Herzegovina',
	'BB': 'Barbados',
	'BD': 'Bangladesh',
	'BE': 'Belgium',
	'BF': 'Burkina Faso',
	'BG': 'Bulgaria',
	'BH': 'Bahrain',
	'BI': 'Burundi',
	'BJ': 'Benin',
	'BM': 'Bermuda',
	'BN': 'Brunei Darussalam',
	'BO': 'Bolivia (Plurinational State of)',
	'BR': 'Brazil',
	'BS': 'Bahama',
	'BT': 'Bhutan',
	'BU': 'Burma (no longer exists)',
	'BV': 'Bouvet Island',
	'BW': 'Botswana',
	'BY': 'Belarus',
	'BZ': 'Belize',
	'CA': 'Canada',
	'CC': 'Cocos (Keeling) Islands',
	'CD': 'Congo, Democratic Republic of the',
	'CF': 'Central African Republic',
	'CG': 'Congo',
	'CH': 'Switzerland',
	'CI': 'Côte d\'Ivoire',
	'CK': 'Cook Iislands',
	'CL': 'Chile',
	'CM': 'Cameroon',
	'CN': 'China',
	'CO': 'Colombia',
	'CR': 'Costa Rica',
	'CS': 'Czechoslovakia (no longer exists)',
	'CU': 'Cuba',
	'CV': 'Cape Verde',
	'CX': 'Christmas Island',
	'CY': 'Cyprus',
	'CZ': 'Czech Republic',
	'DD': 'German Democratic Republic (no longer exists)',
	'DE': 'Germany',
	'DJ': 'Djibouti',
	'DK': 'Denmark',
	'DM': 'Dominica',
	'DO': 'Dominican Republic',
	'DZ': 'Algeria',
	'EC': 'Ecuador',
	'EE': 'Estonia',
	'EG': 'Egypt',
	'EH': 'Western Sahara',
	'ER': 'Eritrea',
	'ES': 'Spain',
	'ET': 'Ethiopia',
	'FI': 'Finland',
	'FJ': 'Fiji',
	'FK': 'Falkland Islands (Malvinas)',
	'FM': 'Micronesia',
	'FO': 'Faroe Islands',
	'FR': 'France',
	'FX': 'France, Metropolitan',
	'GA': 'Gabon',
	'GB': 'United Kingdom of Great Britain and Northern Ireland',
	'GD': 'Grenada',
	'GE': 'Georgia',
	'GF': 'French Guiana',
	'GH': 'Ghana',
	'GI': 'Gibraltar',
	'GL': 'Greenland',
	'GM': 'Gambia',
	'GN': 'Guinea',
	'GP': 'Guadeloupe',
	'GQ': 'Equatorial Guinea',
	'GR': 'Greece',
	'GS': 'South Georgia and the South Sandwich Islands',
	'GT': 'Guatemala',
	'GU': 'Guam',
	'GW': 'Guinea-Bissau',
	'GY': 'Guyana',
	'HK': 'Hong Kong',
	'HM': 'Heard & McDonald Islands',
	'HN': 'Honduras',
	'HR': 'Croatia',
	'HT': 'Haiti',
	'HU': 'Hungary',
	'ID': 'Indonesia',
	'IE': 'Ireland',
	'IL': 'Israel',
	'IN': 'India',
	'IO': 'British Indian Ocean Territory',
	'IQ': 'Iraq',
	'IR': 'Iran (Islamic Republic of)',
	'IS': 'Iceland',
	'IT': 'Italy',
	'JM': 'Jamaica',
	'JO': 'Jordan',
	'JP': 'Japan',
	'KE': 'Kenya',
	'KG': 'Kyrgyzstan',
	'KH': 'Cambodia',
	'KI': 'Kiribati',
	'KM': 'Comoros',
	'KN': 'St. Kitts and Nevis',
	'KP': 'Korea, Democratic People\'s Republic of',
	'KR': 'Korea, Republic of',
	'KW': 'Kuwait',
	'KY': 'Cayman Islands',
	'KZ': 'Kazakhstan',
	'LA': 'Lao People\'s Democratic Republic',
	'LB': 'Lebanon',
	'LC': 'Saint Lucia',
	'LI': 'Liechtenstein',
	'LK': 'Sri Lanka',
	'LR': 'Liberia',
	'LS': 'Lesotho',
	'LT': 'Lithuania',
	'LU': 'Luxembourg',
	'LV': 'Latvia',
	'LY': 'Libya',
	'MA': 'Morocco',
	'MC': 'Monaco',
	'MD': 'Moldova, Republic of',
	'MG': 'Madagascar',
	'MH': 'Marshall Islands',
	'ML': 'Mali',
	'MN': 'Mongolia',
	'MM': 'Myanmar',
	'MO': 'Macau',
	'MP': 'Northern Mariana Islands',
	'MQ': 'Martinique',
	'MR': 'Mauritania',
	'MS': 'Monserrat',
	'MT': 'Malta',
	'MU': 'Mauritius',
	'MV': 'Maldives',
	'MW': 'Malawi',
	'MX': 'Mexico',
	'MY': 'Malaysia',
	'MZ': 'Mozambique',
	'NA': 'Namibia',
	'NC': 'New Caledonia',
	'NE': 'Niger',
	'NF': 'Norfolk Island',
	'NG': 'Nigeria',
	'NI': 'Nicaragua',
	'NL': 'Netherlands',
	'NO': 'Norway',
	'NP': 'Nepal',
	'NR': 'Nauru',
	'NT': 'Neutral Zone (no longer exists)',
	'NU': 'Niue',
	'NZ': 'New Zealand',
	'OM': 'Oman',
	'PA': 'Panama',
	'PE': 'Peru',
	'PF': 'French Polynesia',
	'PG': 'Papua New Guinea',
	'PH': 'Philippines',
	'PK': 'Pakistan',
	'PL': 'Poland',
	'PM': 'St. Pierre & Miquelon',
	'PN': 'Pitcairn',
	'PR': 'Puerto Rico',
	'PT': 'Portugal',
	'PW': 'Palau',
	'PY': 'Paraguay',
	'QA': 'Qatar',
	'RE': 'Réunion',
	'RO': 'Romania',
	'RS': 'Serbia',
	'RU': 'Russian Federation',
	'RW': 'Rwanda',
	'SA': 'Saudi Arabia',
	'SB': 'Solomon Islands',
	'SC': 'Seychelles',
	'SD': 'Sudan',
	'SE': 'Sweden',
	'SG': 'Singapore',
	'SH': 'St. Helena',
	'SI': 'Slovenia',
	'SJ': 'Svalbard & Jan Mayen Islands',
	'SK': 'Slovakia',
	'SL': 'Sierra Leone',
	'SM': 'San Marino',
	'SN': 'Senegal',
	'SO': 'Somalia',
	'SR': 'Suriname',
	'SS': 'South Sudan',
	'ST': 'Sao Tome & Principe',
	'SU': 'Union of Soviet Socialist Republics (no longer exists)',
	'SV': 'El Salvador',
	'SY': 'Syrian Arab Republic',
	'SZ': 'Swaziland',
	'TC': 'Turks & Caicos Islands',
	'TD': 'Chad',
	'TF': 'French Southern Territories',
	'TG': 'Togo',
	'TH': 'Thailand',
	'TJ': 'Tajikistan',
	'TK': 'Tokelau',
	'TM': 'Turkmenistan',
	'TN': 'Tunisia',
	'TO': 'Tonga',
	'TP': 'East Timor',
	'TR': 'Turkey',
	'TT': 'Trinidad & Tobago',
	'TV': 'Tuvalu',
	'TW': 'Taiwan, Province of China',
	'TZ': 'Tanzania, United Republic of',
	'UA': 'Ukraine',
	'UG': 'Uganda',
	'UM': 'United States Minor Outlying Islands',
	'US': 'United States of America',
	'UY': 'Uruguay',
	'UZ': 'Uzbekistan',
	'VA': 'Vatican City State (Holy See)',
	'VC': 'St. Vincent & the Grenadines',
	'VE': 'Venezuela (Bolivarian Republic of)',
	'VG': 'British Virgin Islands',
	'VI': 'United States Virgin Islands',
	'VN': 'Viet Nam',
	'VU': 'Vanuatu',
	'WF': 'Wallis & Futuna Islands',
	'WS': 'Samoa',
	'YD': 'Democratic Yemen (no longer exists)',
	'YE': 'Yemen',
	'YT': 'Mayotte',
	'YU': 'Yugoslavia',
	'ZA': 'South Africa',
	'ZM': 'Zambia',
	'ZR': 'Zaire',
	'ZW': 'Zimbabwe',
	'ZZ': 'Unknown or unspecified country',
}

# Airline Chlorophleth
import requests
import json
import xmltodict

url = "https://timetable-lookup.p.rapidapi.com/airlines/"

headers = {
	"X-RapidAPI-Key": "0a40c53aa2msh11cfe603f01094cp164f18jsn0fb60b6c0e32",
	"X-RapidAPI-Host": "timetable-lookup.p.rapidapi.com"
}

response = xmltodict.parse(requests.get(url, headers=headers).text)

countries_iso={}
for country in countries_raw:
  countries_iso[country['name']]=(country['alpha-3'])

keys=list(countries.keys())
temp={}
for key in keys:
  temp[key]=0
for i in range(len((response['Airlines']['Airline']))):
  if(type(response['Airlines']['Airline'][i]['Country'])==dict):
    if(response['Airlines']['Airline'][i]['Country']['@IATACode'] in temp.keys()):
      temp[response['Airlines']['Airline'][i]['Country']['@IATACode']]+=1
  else:
    for j in range(len(response['Airlines']['Airline'][i]['Country'])):
      if(response['Airlines']['Airline'][i]['Country'][j]['@IATACode'] in temp.keys()):
        temp[response['Airlines']['Airline'][i]['Country'][j]['@IATACode']]+=1

countryStats={'Country':[], 'Airline Count':[], "iso_alpha":[]}
for key in keys:
  if(countries[key] in countries_iso):
    countryStats['Country'].append(countries[key])
    countryStats['Airline Count'].append(temp[key])
    countryStats['iso_alpha'].append(countries_iso[countries[key]])

country_df=pd.DataFrame.from_dict(countryStats)
fig = px.choropleth(country_df, locations='iso_alpha', color='Airline Count',hover_name='Country', range_color=[0, 150])
pyo.plot(fig, filename='airlines.html')


# Airline Bar char
countries=list(country_df['Country'])
airlines=list(country_df['Airline Count'])

for i in range(0,len(countries)):
    temp=0
    minIndex=i
    for j in range(i+1,len(countries)):
      if airlines[j]<airlines[minIndex]:
        minIndex=j
    temp=countries[i]
    countries[i]=countries[minIndex]
    countries[minIndex]=temp

    temp=airlines[i]
    airlines[i]=airlines[minIndex]
    airlines[minIndex]=temp

sorted={"Countries":countries,"Airline Count":airlines}
df=pd.DataFrame(sorted)

# Pie chart
fig=px.bar(df,x="Countries", y="Airline Count")
pyo.plot(fig, filename='airlines_bar.html')

# Create a pandas DataFrame
data = pd.DataFrame({
    "type": ["Personal", "Business", "Instructional", "Agriculture", "Air Medical", "Air Taxi", "Other"],
    "occurance": [30.7, 15.6, 25.1, 3.5, 2.7, 10.8, 11.6]
})

# Create a pie chart using Plotly Express
fig = px.pie(data, values="occurance", names="type")
pyo.plot(fig, filename='sectors.html')