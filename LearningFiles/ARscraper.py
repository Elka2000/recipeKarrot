
from bs4 import BeautifulSoup
import requests

html_file = requests.get("https://www.allrecipes.com/recipe/280376/vegetarian-bourguignon/").text
	
soup = BeautifulSoup(html_file,'lxml',)
ingredtags = soup.find_all('span', class_='ingredients-item-name')
instructtags = soup.find_all('ul', class_="instructions-section")
atags = soup.find_all('a')
title = soup.find_all('h1', class_="headline heading-content elementFont__display")
timeele = soup.find_all('div', class_="recipe-meta-item")

#Retrieve Recipe Title
for tit in title:
	print(tit.text)
print("")


#Retrieve Recipe About - Time Length
print('Time')
for tim in timeele:
	print(tim.text)
print("")

#Retrieve Ingredient List
# IMPROVE - Regex to separate the number from ingredient - could connect to servings where user adjust servings to adjust recipe.
print('Ingredients')
for ingred in ingredtags:
	print (ingred.text)
print('')

#Retrieve Instructions
#IMPROVE - using regex to separate the steps to read better
print('Instructions')
for words in instructtags:
	print (words.text)


