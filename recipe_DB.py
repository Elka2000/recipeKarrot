from copy import copy
import sqlite3
from bs4 import BeautifulSoup
from numpy import integer
import requests
import random

connR = sqlite3.connect('RecipeScrape2.sqlite')
#connR = sqlite3.connect(':memory:')
curR = connR.cursor()

connL = sqlite3.connect('spider.sqlite')
curL = connL.cursor()


#Create Main Recipe Table - (Recipe_ID, Rec_Title, Instructions, Recipe URL, Date_Last, Rating) NOTE MAKE SURE DATE TYPE IS CORRECT
curR.execute('''CREATE TABLE IF NOT EXISTS Recipes_Main 
    (recipe_id INTEGER PRIMARY KEY, recipe_title TEXT UNIQUE, instructions TEXT, recipe_url TEXT, date_last DATE, rating INTEGER)''')

#Create Table for INGREDIENT KEYS ###      First Column figure how to put the id PRIMARY KEY as the same to corresponding Recipe
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Ingredients_Keys
    (ingredient_id INTEGER PRIMARY KEY, ingredient_key TEXT)''')
# #Table for INGREDIENT VALUES -- Do I need to list as primary key? NOTE Keeping Ing_Value as TEXT will prevent altering recipes,
# #  must separate value from measurement.
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Ingredients_Values
    (ingredient_id INTEGER , ingredient_value TEXT,recipe_id INTEGER)''')

# #CREATE TIME KEYS ---- NOTE(REMEMBER TOTAL TIME KEY )
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Time_Keys
    (time_id INTEGER PRIMARY KEY, time_key TEXT)''')
# ### Create time VALUES -- Value is TEXT for now but must be INTEGER to get total time
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Time_Values
    (time_id INTEGER,time_value TEXT, recipe_id INTEGER)''')

# #CREATE Nutrition KEYS ---- 
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Nutrition_Keys
    (nutrition_id INTEGER PRIMARY KEY, nutrition_key TEXT)''')
# ### Create Nutrition VALUES
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Nutrition_Values
   (nutrition_id INTEGER,nutrition_value INTEGER, recipe_id INTEGER)''')

# #CREATE CATEGORY DIET ---- Figure way to take key words from recipe to categories
curR.execute('''CREATE TABLE IF NOT EXISTS Category_Diet
   (category_id INTEGER PRIMARY KEY, category TEXT, diet TEXT, recipe_id INTEGER)''')


print('---------------------------------------------------------------------------')
webs = list()

x = int(input("how many recipes "))
curL.execute('''SELECT Url FROM Pages ORDER BY RANDOM() LIMIT 4''')
for row in curL:
	web1 = row[0] 
	webs.append(str(web1))

webs2 = copy(webs)
print(webs)



while (x > 0) :
	#file1 is created first to first select a random recipe that is then used to to get the html info using "requests"
	html_file1 = random.choice(webs2)
	html_file = requests.get(html_file1).text

	print('-----------------------------8888888888')
	print('')
	#THIS WILL REMOVE the chosen file from the temporary list.  To avoid repeats long term you will need 
	# to add to a running list of recipes (Possibly another DB or maybe even adding a date coloumn on database
	# to filter out for recently made)
	webs2.remove(html_file1)

	soup = BeautifulSoup(html_file,'lxml',)
	ingredtags = soup.find_all('span', class_='recipe-ingredients__item--ingredient')
	ing_amount = soup.find_all('span', class_='recipe-ingredients__item--amount-inner')
	instructtags = soup.find_all('div', class_="recipe-method__text-wrapper")
	atags = soup.find_all('a')
	title = soup.find('h2', class_="recipe-intro__title")
	time_key = soup.find_all('span', class_="post-hero__stat--key")
	time_value = soup.find_all('span', class_="post-hero__stat--value")
	nutri_key = soup.find_all('span', class_="recipe-nutrition__item-title")
	nutri_amount = soup.find_all('span', class_="recipe-nutrition__item-amount")

	print(title)

	#INSERT into Recipes_Main --- Here #Insert URL
	
	recipe_id = integer
	

	

	print("Title")
	#Retrieve Recipe Title
	for tit in title:
		curR.execute('INSERT OR IGNORE INTO Recipes_Main (recipe_url,recipe_title) VALUES (?,?)',(html_file1,tit))
		connR.commit()
		curR.execute('SELECT recipe_id FROM Recipes_Main WHERE recipe_title =?',(tit,))
		recipe_id = curR.fetchone()
		connR.commit()
		print(recipe_id)
		
		print(tit.text)

	print("")

	print('Time')
	#Insert Recipe About - Time Length NOTE Some time values are listed as integers others as text (ex. 35 min or 4 hr 25 min) 
	#How do you get keep the values separately? Compile list then see what keywords are common. 
	for k, v in zip(time_key,time_value):
		try:

			curR.execute('INSERT OR IGNORE INTO Rec_Time_Keys (time_key) VALUES (?)',(k,))
			time_id = curR.execute('SELECT time_id FROM Rec_Time_Keys WHERE time_key=?',(k,))
			curR.execute('INSERT OR IGNORE INTO Rec_Time_Values (time_id,time_value,recipe_id) VALUES (?,?,?)',(time_id,v,recipe_id))  
			connR.commit()
			print(k.text, v.text)	
		except:
			 
			print(k.text)		
	print('')

	#Retrieve Ingredient List
	# IMPROVE - Regex to separate the number from ingredient - could connect to servings where user adjust servings to adjust recipe.
	print('Ingredients')

	#print(type(ing_amount)) --- Need to figure out how to split measurement from integer (ex. 4 cups, 1/2 lb etc.)
	ingredtags = soup.find_all('span', class_='recipe-ingredients__item--ingredient')
	ing_amount = soup.find_all('span', class_='recipe-ingredients__item--amount')
	for a, i in zip(ing_amount,ingredtags):
		curR.execute('INSERT OR IGNORE INTO Rec_Ingredients_Keys (ingredient_key) VALUES (?)',(i,)) 
		ingredient_id = curR.execute('SELECT ingredient_id FROM Rec_Ingredients_Keys WHERE ingredient_key=?',(i,))
		curR.execute('INSERT OR IGNORE INTO Rec_Ingredients_Values (ingredient_id,ingredient_value,recipe_id) VALUES (?,?,?)',(ingredient_id,a,recipe_id))
		connR.commit()

		try:
			print(i.text, a.text)
			
			
		except:
			print(a.text)
	print('')

	#Retrieve Instructions
	#IMPROVE - using regex to separate the steps to read better
	print('Instructions')
	for words in instructtags:
		curR.execute('INSERT OR IGNORE INTO Recipes_Main (instructions) VALUES (?,)',(words,))
		connR.commit()
		print (words.text)

	print('Nutritional Information')
	for k, v in zip(nutri_key,nutri_amount):
		try:
			print(k.text, v.text)
		except:
			print(k.text)
	

	x= x-1
	print('-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4')
	print('')

	





connL.close()
connR.close()

print(webs2)



##USEFUL STUFF
#INSERT INTO TABLE METHOD 1 -- Uses ? as placeholders then use values in parenthesis. 
# If only 1 value I believe you need a comma after first value reference still ex ((?)',(val1,))
## method1.excute(""" INSERT INTO table1 VALUES (?,?,?) """,(val1,val2,val3))
 
#Method 2 -- uses colon then name describes placeholder. Values listed as dictionary.
#method2.excute(""" INSERT INTO table2 VALUES (:val1,:val2,:val3) """,{'val1':'poppy','val2':'elle','val3':'muria'})

#Connect to test database running on memory to not have to keep deleting database
# conn = sqlite.connect(':memory:')








