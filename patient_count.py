from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from fuzzywuzzy import fuzz
from datetime import date
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd

#Setup cerdentials for Drive and Sheet API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'ibm-hack-281412-af7fffea1c18.json', scope)
gc = gspread.authorize(credentials)

#Specify spreadsheet
spreadsheet_key = '19sF-7b2j1gT8qQyb-latzv3frro-3KwLHmFDlnfoo68'
wks_name = 'Master'

#Website from which data is do be extracted
url = "https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/"

#df = pd.DataFrame(columns=['District','Total','Cured','Active','Deaths','State','Date'])

#Open already stored sheet
ws = gc.open("Corona Patient").worksheet("Master")
print(ws)
df = pd.DataFrame(ws.get_all_records())
print(df)

#Get names of all states
state_dist = pd.read_excel('State&Districts.xlsx')
all_states = state_dist['State/UT'].unique()
print(all_states)

#get html of the specified website
request = requests.get(url)
soup = BeautifulSoup(request.text,'html.parser')
result = soup.find_all('div', attrs = {'class' : 'skgm-td'})

data = []
state = 'Total'

for district in result:
    if(len(data)!=0):
        district = re.sub(r"\W", "", district.get_text())
    else:
        district = district.get_text()
        district = district.strip()
        if(district in all_states):
            state = district
        


    if(district=='Districts' or district=='Cases' or district=='Cured' or district=='Active' or district=='Deaths' or district=='State/UT'):
        continue

    data.append(district)
    if (len(data)== 5):
        data.append(state)
        data.append(date.today())
        df.loc[len(df)]=data
        print(data)
        data.clear()
     
print(df)
gd.set_with_dataframe(ws, df)

