import pandas as pd
from fuzzywuzzy import fuzz
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

#Specify credentials for drive and sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'ibm-hack-281412-af7fffea1c18.json', scope)
gc = gspread.authorize(credentials)

#get specific sheet
spreadsheet_key = '1yXp18xyRVbTmx0BHCfUhtYc-SD7JPG5qYXGtiJ_VpI4'
wks_name = 'Master'

#get tweets sheet to calculate
ws = gc.open("Tweets").worksheet("Master")
print(ws)
df = pd.DataFrame(ws.get_all_records())

count_df = pd.DataFrame(columns=['State','District','positive_count','negative_count','neutral_count','pfs','pt','pds','pe','po','Date'])

#find all states
state_dist = pd.read_excel('State&Districts.xlsx')
states = state_dist['State/UT'].unique()
print(states)
dates=df['date'].unique()
print(dates)
places = df['district'].unique()
print(places)

for date in dates :
        for state in states:
            total_places=state_dist[state_dist['State/UT']==state]
            locations = total_places['Districts'].unique()
            for district in locations:
                count_positive = 0
                count_neutral = 0
                count_negative = 0
                count_pfs = 0  
                count_pt = 0  
                count_pds = 0  
                count_pe = 0  
                count_po = 0  
                for place in places:
                    #fuzzy matching to avoid mismatch due to whitespace
                    if(fuzz.token_sort_ratio(district,place)>90):
                        total=df[df['district']==place]
                        total = total[total['date']==date]
                        count_positive=len(total[total['sentiment']=='positive'])
                        count_neutral=len(total[total['sentiment']=='neutral'])
                        count_negative=len(total[total['sentiment']=='negative'])
                        count_pfs = len(total[total['problem']=="['Food Shortage']"]) 
                        count_pt = len(total[total['problem']=="['Transpotation']"])  
                        count_pds = len(total[total['problem']=="['Daily Services']"]) 
                        count_pe = len(total[total['problem']=="['Economic']"])  
                        count_po = len(total[total['problem']=="['Others']"])  
                count_df.loc[len(count_df)]=[state,district,count_positive,count_negative,count_neutral,count_pfs,count_pt,count_pds,count_pe,count_po,date]

print(count_df)
d2g.upload(count_df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)


        
    

