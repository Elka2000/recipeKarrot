import sqlite3
from bs4 import BeautifulSoup
import requests
import random

connR = sqlite3.connect('RecipeScrape2.sqlite')
curR = connR.cursor()

connL = sqlite3.connect('spider.sqlite')
curL = connL.cursor()

#Create Main Recipe Table - (ID, URL, TITLE, INSTRUCTION NUTRITIONAL, CATEGORY, TIME)
#curR.execute('''CREATE TABLE IF NOT EXISTS Main List
 #   (id INTEGER PRIMARY KEY, url TEXT UNIQUE, Title TEXT, Instructions TEXT, Nutritional TEXT,Category TEXT, TimeAbout TEXT)''')

#Create Table for Ingredients ### First Column figure how to put the id PRIMARY KEY as the same to corresponding Recipe
#curR.execute('''CREATE TABLE IF NOT EXISTS Ingredients
 #   (id INTEGER PRIMARY KEY, url TEXT UNIQUE,Ingredients TEXT, IngAmount INGTEGER, Category TEXT)''')

# Find the ids that send out page rank - we only are interested
# in pages in the SCC that have in and out links





print('---------------------------------------------------------------------------')
webs = list()

curL.execute('''SELECT Url FROM Pages ORDER BY RANDOM() LIMIT 8''')
for row in curL:
	web1 = row[0] 
	webs.append(str(web1))

print(webs)
#link = requests.get(random.choice(webs)).text 

linklist=["https://themodernproper.com/dressed-up-baked-beans", 
			 "https://themodernproper.com/chicken-piccata"]



link2 = "https://themodernproper.com/biscuits-and-gravy"
html_file = requests.get(random.choice(webs)).text



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
for k, v in zip(time_key,time_value):
	try:
		print(k.text, v.text)
		
	except:
		print(k.text)


print('')

#Retrieve Ingredient List
# IMPROVE - Regex to separate the number from ingredient - could connect to servings where user adjust servings to adjust recipe.
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


print('Nutritional Information')
for k, v in zip(nutri_key,nutri_amount):
	try:
		print(k.text, v.text)
		
	except:
		print(k.text)


print('')












