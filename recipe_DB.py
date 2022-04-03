import sqlite3
from bs4 import BeautifulSoup
import requests
import random



##I want to add all the recipe incredients to this database so that they can then be filtered by ingredients, number of calories, 
# or whatever parameter is needed. File is currently empty.
connR = sqlite3.connect('RecipeScrape2.sqlite')
curR = connR.cursor()

## This is the database of over 900 recipe links that was created using spider.py file.
connL = sqlite3.connect('spider.sqlite')
curL = connL.cursor()

#Create Main Recipe Table - (ID, URL, TITLE, INSTRUCTION NUTRITIONAL, CATEGORY, TIME)
#curR.execute('''CREATE TABLE IF NOT EXISTS Main List
 #   (id INTEGER PRIMARY KEY, url TEXT UNIQUE, Title TEXT, Instructions TEXT, Nutritional TEXT,Category TEXT, TimeAbout TEXT)''')

#Create Table for Ingredients ### First Column figure how to put the id PRIMARY KEY as the same to corresponding Recipe
#curR.execute('''CREATE TABLE IF NOT EXISTS Ingredients
 #   (id INTEGER PRIMARY KEY, url TEXT UNIQUE,Ingredients TEXT, IngAmount INGTEGER, Category TEXT)''')



print('---------------------------------------------------------------------------')
webs = list()

#this connects to Recipe Database and loops through and gets 8 recipes "LIMIT 8"
curL.execute('''SELECT Url FROM Pages ORDER BY RANDOM() LIMIT 8''')
for row in curL:
	web1 = row[0] 
	webs.append(str(web1))

print(webs)


#Selects a random link from the webs list -- Next step is using a copy of the weblist and removing that link fromt 
#he list so it is not selected on the next round. Also add to global filter list so that this recipe is not chosen for the next calendar month.
html_file = requests.get(random.choice(webs)).text


#Soup is the raw htmt. To find the tags you need to inspect the elements in the webpage and see what tags and classes you want to pull.
soup = BeautifulSoup(html_file,'lxml',)
ingredtags = soup.find_all('span', class_='recipe-ingredients__item--ingredient')
ing_amount = soup.find_all('span', class_='recipe-ingredients__item--amount-inner')
instructtags = soup.find_all('div', class_="recipe-method__text-wrapper")
atags = soup.find_all('a')
title = soup.find_all('h2', class_="recipe-intro__title")
time_key = soup.find_all('span', class_="post-hero__stat--key")
time_value = soup.find_all('span', class_="post-hero__stat--value")
nutri_key = soup.find_all('span', class_="recipe-nutrition__item-title")
nutri_amount = soup.find_all('span', class_="recipe-nutrition__item-amount")


#print(soup)
print(title)
#Retrieve Recipe Title
for tit in title:
	print(tit.text)
print("")


print('Time')
#Retrieve Recipe About - Time Length
# IMPROVE - When inputing these in Database create a new variable called combined - so it is the Total Time.
for k, v in zip(time_key,time_value):
	try:
		print(k.text, v.text)
		
	except:
		print(k.text)


print('')

#Retrieve Ingredient List
print('Ingredients')

#print(type(ing_amount))
ingredtags = soup.find_all('span', class_='recipe-ingredients__item--ingredient')
ing_amount = soup.find_all('span', class_='recipe-ingredients__item--amount')
for a, i in zip(ing_amount,ingredtags):
	try:
		print(i.text, a.text)
		
	except:
		print(a.text)


print('')

#Retrieve Instructions
#IMPROVE - using regex to separate the steps to read better
print('Instructions')
for words in instructtags:
	print (words.text)


#IMPROVE - If someone wants to seach for something by calories there must be a way to do this. 
print('Nutritional Information')
for k, v in zip(nutri_key,nutri_amount):
	try:
		print(k.text, v.text)
		
	except:
		print(k.text)


print('')












