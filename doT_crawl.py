import requests
import json
import pandas as pd

#Request the site
url = "https://api.dotreasury.com/polkadot/stats/weekly"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

#Save the response as a JSON file
with open('data.json', 'w') as f:
    json.dump(response.json(), f)

#Open the file
with open('data.json') as f:
    jsondata = json.load(f)    


#Fetch the file to a pandas DataFrame
df = pd.DataFrame(jsondata[-1])


#Drop the unnecessary columns
df = df.drop(['_id','indexer'], axis=1)
df = df.drop(['blockHeight','blockHash','blockTime'], axis=0)


#Extract Income column
income = df['income'].drop(['slashSeats', 'proposal', 'tip', 'bounty', 'burnt'])


#Extract values from slashSeats row
slashSeats = df.loc['slashSeats', 'income']


# Extract income_2, will be merge with income later (based on the content on doTreasury)
income_2 = pd.DataFrame.from_dict(slashSeats, orient='index')


#Merge income and income_2 to a complete Income dataframe 
income = pd.concat([income, income_2], axis=0)


#Extract Ouput column
output = df['output']
output = output.drop(['inflation','transfer','slash','others','slashSeats'], axis=0)


#Extract Treasury Balance
treasury_balance = df['treasuryBalance'][0]

#Transform Income from a DataFrame to a Series, change the name of the Series 
income = income.squeeze()
income = income.rename('income')

#Output to CSV files
income.to_csv('income', index=True)
output.to_csv('output', index=True)