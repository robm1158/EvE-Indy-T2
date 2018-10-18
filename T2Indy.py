import sys
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import esipy
import yaml
import csv
import sqlite3
from sqlite3 import Error

#
# Initial Vars
#----------------------------------------------------------------------------------------------

database = "eve.db"
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
#
#
# Starting Initialization 
#----------------------------------------------------------------------------------------------

try:
    conn = sqlite3.connect(database)
    c = conn.cursor()
except Error as e:
    print(e)

# use creds to create a client to interact with the Google Drive API
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

#
#
# Main
#----------------------------------------------------------------------------------------------



# Extract and print all of the values
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Python Test").sheet1
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
marketurl = "https://api.evemarketer.com/ec/marketstat/json?typeid=&regionlimit={}10000002"
ids = {} #mat to id

with open(r'typeids.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        ids[row[1]] = row[0]

for iter in list_of_hashes:
    print(ids[iter['Orders']])
    print('select typeID from industryActivityProducts where productTypeID='+str(ids[iter['Orders']]))
    c.execute('select typeID from industryActivityProducts where productTypeID='+str(ids[iter['Orders']]))
    itemID = c.fetchone()
    print(f'select * from industryActivityMaterials where typeID={itemID[0]}')
    c.execute(f'select * from industryActivityMaterials where typeID={itemID[0]}')
    itemMats = c.fetchall()
    print(itemMats)