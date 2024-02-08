# from copy import copy
import sqlite3
from bs4 import BeautifulSoup
# from numpy import integer
import requests
import csv
# import random

import numpy as np
import re
# delete_list=['https://themodernproper.com/recipes/courses/brunch', 'https://themodernproper.com/recipes/convenience/sheet-pan-meals/p2', 'https://themodernproper.com/recipes/dietary/whole-30', 'https://themodernproper.com/recipes/courses/salads']


import csv
from datetime import datetime, timedelta
from sqlite3 import Timestamp
import pandas as pd
from calendar import day_abbr, day_name
import http.client
import ssl
import json
from pandas import concat, json_normalize
from google.cloud import storage
import os
import time
from pandas_gbq import to_gbq, read_gbq

start_time = time.time()
# #----------------------------------------------------------------------------------------------------

# 2. Set JSON key as environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/alanochoa/Desktop/Visual Studio Projects/Water Quality/buoyproject-8c821ef570d2.json"

# # 3. Specify a bucket name and other details
# bucket_name = 'buoy_hf_dwq'
# source_file_path = 'MOR_Pies/Parameter_Counts_All_Facilities.csv'
# destination_blob_path = 'subfolder/my_data_on_gcp_bucket.csv'

# 4. Define a special function
def upload_to_storage(bucket_name: str, source_file_path: str, destination_blob_path: str):
  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_path)
  blob.upload_from_filename(source_file_path)
  print(f'The file {source_file_path} has been uploaded to GCP bucket path: {destination_blob_path}')
  return None

apiKey = '1785c9426f8a457690990f3102197630'
start = str(datetime.now() - timedelta(hours=4)).split('.')[0].replace(" ",'%20')#start 4 hours before
end = str(datetime.now()).split('.')[0].replace(" ",'%20') #currenttime

conn = http.client.HTTPSConnection("wqdatalive.com", context = ssl._create_unverified_context())

client = storage.Client()
bucket = client.get_bucket('buoy_hf_dwq')
blob = bucket.get_blob("Site_Specific_Inactive_Removed.csv")
blob.download_to_filename('/tmp/temp.csv')        
paramlist = csv.reader(open('/tmp/temp.csv')) 

#paramlist = csv.reader(open('Buoy_API  - Site_Specific_Parameters.csv')) 
next(paramlist)


# #NOTE: CREATE Dictionary list of parameter and sites
paramdict={} #parameterID: paramNames
siteparams = {} #siteID: paramID
sitedict = {} #siteID: siteName
for row in paramlist:
	sitedict[row[1]] = row[2] #adds siteID:sitename DICT
	paramdict[row[4]]=row[3] #adds to parameterID:name DICT
	if row[1] in siteparams.keys(): #adds to siteID:paramID dict
		siteparams[row[1]] = siteparams[row[1]]+','+row[4] 
	else: siteparams[row[1]]=row[4]
# print('parameterID: paramNames  DICTIONARY')
# print('')
# print(paramdict)
# print('')
# print('siteID: paramID  DICTIONARY')
# print('')
# print(siteparams)
# print('')
# print('siteID: siteName  DICTIONARY')
# print('')
# print(sitedict)
# print('')
parameter= 7286
pname= paramdict[str(parameter)]
print(pname,'- Pname')
for k,v in siteparams.items():
	if str(parameter) in str(v):
		siteid= k #siteid is still string, convert to int when inputing in DF
		print(siteid, '- SiteID') 
		break
sitename=sitedict[siteid]
 #gets the site name of the siteID
print(sitename, '- Sitename')

print("--- %s seconds ---" % (time.time() - start_time))


# file = open('ul_vineyard.csv')
# csvreader = csv.reader(file)

# print(next(csvreader))
# connL = sqlite3.connect('spider.sqlite')
# curL = connL.cursor()

# print('---------------------------------------------------------------------------')

# x=2

# meat = list()

# while (x > 0) :
# 	#file1 is created first to first select a random recipe that is then used to to get the html info using "requests"
# 	html_file1 = 'https://themodernproper.com/tortilla-soup'    #random.choice(webs2)
# 	html_file = requests.get(html_file1).text

	
# 	print('')
# 	print(html_file1)
# 	print('')
# 	#THIS WILL REMOVE the chosen file from the temporary list.  To avoid repeats long term you will need 
# 	# to add to a running list of recipes (Possibly another DB or maybe even adding a date coloumn on database
# 	# to filter out for recently made)
	

# 	soup = BeautifulSoup(html_file,'lxml',)
# 	ingredtags = soup.find_all(['a','span'], class_='recipe-ingredients__item--ingredient')
# 	ing_amount = soup.find_all(['a','span'], class_='recipe-ingredients__item--amount-inner')
# 	instructtags = soup.find_all('div', class_="recipe-method__text-wrapper")
# 	atags = soup.find_all('a')
# 	title = soup.find('h2', class_="recipe-intro__title")
# 	time_key = soup.find_all('span', class_="post-hero__stat--key")
# 	time_value = soup.find_all('span', class_="post-hero__stat--value")
# 	nutri_key = soup.find_all('span', class_="recipe-nutrition__item-title")
# 	nutri_amount = soup.find_all('span', class_="recipe-nutrition__item-amount")
	
# 	#print(title)
# 	print(len(ingredtags))
# 	print(len(ing_amount)) 
# 	#print((ingredtags))


# 	#for i in  ingredtags :
# 		#print(i.text)
# 		#print(soup)
# 	if title == None: 
# 		#Delete URLS that do not have titles - Deletes from spider.sqlite file
# 		print(html_file1)
# 		curL.execute("DELETE FROM Pages WHERE Url=?",(html_file1,))
# 		connL.commit

# 		print("No Title - Deleted from DB")
	
# 		continue
# 	else:
# 		#INSERT into Recipes_Main --- Here #Insert URL

# 		recipe_id = integer

# 		print("Title")
# 		#Retrieve Recipe Title
# 		for tit in title:

# 			connR.commit()
# 			curR.execute('SELECT recipe_id FROM Recipes_Main WHERE recipe_title =?',(tit,))
# 			recipe_id = curR.fetchone()
# 			connR.commit()
# 			#print(recipe_id[0])
# 			print(tit.text)

# 		print("")

# 		#Retrieve Ingredient List
# 		# IMPROVE - Regex to separate the number from ingredient - could connect to servings where user adjust servings to adjust recipe.
# 		print('Ingredients')

# 		#print(type(ing_amount)) --- Need to figure out how to split measurement from integer (ex. 4 cups, 1/2 lb etc.)
	
# 		for a, i in zip(ing_amount,ingredtags):
# 			try:
# 				curR.execute('INSERT OR IGNORE INTO Rec_Ingredients_Keys (ingredient_key) VALUES (?)',(i.text.strip(),)) 
# 				curR.execute('SELECT ingredient_id FROM Rec_Ingredients_Keys WHERE ingredient_key=?',(i.text,))
# 				ingredient_id = curR.fetchone()
# 				#print(ingredient_id[0])
# 				#must strip it to remove all the extra spaces
# 				curR.execute('INSERT OR IGNORE INTO Rec_Ingredients_Values (ingredient_id,ingredient_value,recipe_id) VALUES (?,?,?)',(ingredient_id[0],a.text.strip(),recipe_id[0]))
# 				connR.commit()
# 				print(i.text, a.text.strip())
# 				#print(i,a)
				
				
# 			except:
# 				print(a.text)
# 				print('error - Ingredient')
# 		print('')
# 		[ ]
			
# 		#Retrieve Instructions
# 		#IMPROVE - using regex to separate the steps to read better
# 		#print('Instructions')
# 		for words in instructtags:
# 			curR.execute('UPDATE Recipes_Main SET instructions=? WHERE recipe_id=?',(words.text.strip(),recipe_id[0]))
# 			connR.commit()
# 			print(words.text,1)
# 			meaty = bool(re.search('meat|fish|chicken|turkey|beef|salmon|bacon|sausage|steak|shrimp|prawns|pork|lamb|duck|seafood', words.text))
# 			print(meaty)
# 			if meaty == True:
# 				meat.append(html_file1)
# 			else: continue
			
	
			

		
# 		x= x-1
# 		print('-RECIPE-ONE-RECIPE-DONE-RECIPE-DONE-RECIPE-DONE-RECIPE-DONE-RECIPE-DONE-')
# 		print('')





# connL.close()
# connR.close()

# print("------------------------------------")
# print(meat)

# #These are just notes

# ##USEFUL STUFF
# #INSERT INTO TABLE METHOD 1 -- Uses ? as placeholders then use values in parenthesis. 
# # If only 1 value I believe you need a comma after first value reference still ex ((?)',(val1,))
# ## method1.excute(""" INSERT INTO table1 VALUES (?,?,?) """,(val1,val2,val3))

# #Method 2 -- uses colon then name describes placeholder. Values listed as dictionary.
# #method2.excute(""" INSERT INTO table2 VALUES (:val1,:val2,:val3) """,{'val1':'poppy','val2':'elle','val3':'muria'})

# #Connect to test database running on memory to not have to keep deleting database
# # conn = sqlite.connect(':memory:')
