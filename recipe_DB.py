from copy import copy
import sqlite3
from bs4 import BeautifulSoup
from numpy import integer
import requests
import random
import re



##These connR variable is making the connection to the SQLite Database file that has the list of ingredients instructions etc.
connR = sqlite3.connect('RecipeScrape3.sqlite')
## This curR is imporant, it can be described as a "cursor" it is used to then execute SQL code like in line 22
curR = connR.cursor()

connL = sqlite3.connect('spider.sqlite')
curL = connL.cursor()

curL.execute('''CREATE TABLE IF NOT EXISTS scanned
	(id_url INTEGER PRIMARY KEY,s_url TEXT)''')


#Create Main Recipe Table - (Recipe_ID, Rec_Title, Instructions, Recipe URL, Date_Last, Rating) NOTE MAKE SURE DATE TYPE IS CORRECT
curR.execute('''CREATE TABLE IF NOT EXISTS Recipes_Main 
    (recipe_id INTEGER PRIMARY KEY, recipe_title TEXT UNIQUE, instructions TEXT, recipe_url TEXT, date_last DATE, rating INTEGER)''')

#Create Table for INGREDIENT KEYS ###      First Column figure how to put the id PRIMARY KEY as the same to corresponding Recipe
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Ingredients_Keys
    (ingredient_id INTEGER PRIMARY KEY, ingredient_key TEXT UNIQUE)''')
# #Table for INGREDIENT VALUES -- Do I need to list as primary key? NOTE Keeping Ing_Value as TEXT will prevent altering recipes,
# #  must separate value from measurement.
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Ingredients_Values
    (ingredient_id INTEGER , ingredient_value TEXT,recipe_id INTEGER)''')

# #CREATE TIME KEYS ---- NOTE(REMEMBER TOTAL TIME KEY )
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Time_Keys
    (time_id INTEGER PRIMARY KEY, time_key TEXT UNIQUE)''')
# ### Create time VALUES -- Value is TEXT for now but must be INTEGER to get total time
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Time_Values
    (time_id INTEGER,time_value TEXT, recipe_id INTEGER)''')

# #CREATE Nutrition KEYS ---- 
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Nutrition_Keys
    (nutrition_id INTEGER PRIMARY KEY, nutrition_key TEXT UNIQUE)''')
# ### Create Nutrition VALUES
curR.execute('''CREATE TABLE IF NOT EXISTS Rec_Nutrition_Values
   (nutrition_id INTEGER,nutrition_value INTEGER, recipe_id INTEGER)''')

# #CREATE CATEGORY DIET ---- Figure way to take key words from recipe to categories
curR.execute('''CREATE TABLE IF NOT EXISTS Cat_Keys
   (cat_key_id INTEGER PRIMARY KEY, category UNIQUE) ''')
# #CREATE CATEGORY DIET ---- Figure way to take key words from recipe to categories
curR.execute('''CREATE TABLE IF NOT EXISTS Category_List
   (category_id INTEGER PRIMARY KEY, cat_key_id, recipe_id INTEGER)''')


print('---------------------------------------------------------------------------')
curL.execute('SELECT COUNT(*) FROM scanned')
print(curL.fetchone())
webs = list()

x = int(input("how many recipes "))
curL.execute('''SELECT Url FROM Pages WHERE Url NOT IN (SELECT s_url FROM scanned)ORDER BY RANDOM() LIMIT 20''')
for row in curL:
	web1 = row[0] 
	webs.append(str(web1))

webs2 = copy(webs)
print(webs)
delete_list =list()
meat = list()

while (x > 0) :
	#file1 is created first to first select a random recipe that is then used to to get the html info using "requests"
	html_file1 = random.choice(webs2)
	html_file = requests.get(html_file1).text

	
	print('')
	print(html_file1)
	print('')
	#THIS WILL REMOVE the chosen file from the temporary list.  To avoid repeats long term you will need 
	# to add to a running list of recipes (Possibly another DB or maybe even adding a date coloumn on database
	# to filter out for recently made)
	

	soup = BeautifulSoup(html_file,'lxml',)
	ingredtags = soup.find_all(['a','span'], class_='recipe-ingredients__item--ingredient')
	ing_amount = soup.find_all(['a','span'], class_='recipe-ingredients__item--amount-inner')
	instructtags = soup.find_all('div', class_="recipe-method__text-wrapper")
	title = soup.find('h2', class_="recipe-intro__title")
	time_key = soup.find_all('span', class_="post-hero__stat--key")
	time_value = soup.find_all('span', class_="post-hero__stat--value")
	nutri_key = soup.find_all('span', class_="recipe-nutrition__item-title")
	nutri_amount = soup.find_all('span', class_="recipe-nutrition__item-amount")
	category = soup.find_all('a', class_="post-hero__category--link")

	if title == None: 
		#Delete URLS that do not have titles - Deletes from spider.sqlite file
		print(html_file1)
		curL.execute("DELETE FROM Pages WHERE Url=?",(html_file1,))
		connL.commit()
		delete_list.append(html_file1)

		print("No Title - Deleted from DB")
		webs2.remove(html_file1)
		continue
	else:
		#INSERT into Recipes_Main --- Here #Insert URL

		recipe_id = integer

		print("Title")
		#Retrieve Recipe Title
		for tit in title:
			curL.execute('INSERT OR IGNORE INTO scanned (s_url) VALUES (?)', (html_file1,))
			connL.commit()
			curR.execute('INSERT OR IGNORE INTO Recipes_Main (recipe_url,recipe_title) VALUES (?,?)',(html_file1,tit))
			connR.commit()
			curR.execute('SELECT recipe_id FROM Recipes_Main WHERE recipe_title =?',(tit,))
			recipe_id = curR.fetchone()
			connR.commit()
			#print(recipe_id[0])
			print(tit.text)

		print("")

		print('Time')
		print("")
		
		#Insert Recipe About - Time Length NOTE Some time values are listed as integers others as text (ex. 35 min or 4 hr 25 min) 
		#How do you get keep the values separately? Compile list then see what keywords are common. 
		for k, v in zip(time_key,time_value):
			# print(type(k.text),"-", k.text)
			# print(type(v),"-", v)
			
			try:
				curR.execute('INSERT OR IGNORE INTO Rec_Time_Keys (time_key) VALUES (?)',(k.text,))
				connR.commit()
				curR.execute('SELECT time_id FROM Rec_Time_Keys WHERE time_key=?',(k.text,))
				time_id = curR.fetchone()
				#print(time_id[0])
				#v = v.text
				#v = v.rstrip()
				curR.execute('INSERT OR IGNORE INTO Rec_Time_Values (time_id,time_value,recipe_id) VALUES (?,?,?)',(time_id[0],v.text.strip(),recipe_id[0]))  
				connR.commit()
				print(k.text, v.text)	
			except:
					
				print(k.text)
				print('error - Time ')		
		

		#Retrieve Ingredient List
		# IMPROVE - Regex to separate the number from ingredient - could connect to servings where user adjust servings to adjust recipe.
		print('Ingredients')

		#print(type(ing_amount)) --- Need to figure out how to split measurement from integer (ex. 4 cups, 1/2 lb etc.)
		# # # # ingredtags = soup.find_all('span', class_='recipe-ingredients__item--ingredient')
		# # # # ing_amount = soup.find_all('span', class_='recipe-ingredients__item--amount')
		for a, i in zip(ing_amount,ingredtags):
			try:
				curR.execute('INSERT OR IGNORE INTO Rec_Ingredients_Keys (ingredient_key) VALUES (?)',(i.text.strip(),))
				connR.commit() 
				curR.execute('SELECT ingredient_id FROM Rec_Ingredients_Keys WHERE ingredient_key=?',(i.text,))
				ingredient_id = curR.fetchone()
				#print(ingredient_id[0])
				#must strip it to remove all the extra spaces
				curR.execute('INSERT OR IGNORE INTO Rec_Ingredients_Values (ingredient_id,ingredient_value,recipe_id) VALUES (?,?,?)',(ingredient_id[0],a.text.strip(),recipe_id[0]))
				connR.commit()
				print(i.text, a.text.strip())
				
				
			except:
				print(a.text)
				print('error - Ingredient')
		print('')
		[ ]
			
		#Retrieve Instructions
		#IMPROVE - using regex to separate the steps to read better
		#print('Instructions')
		
		for words in instructtags:
			curR.execute('UPDATE Recipes_Main SET instructions=? WHERE recipe_id=?',(words.text.strip(),recipe_id[0]))
			connR.commit()
			print(words.text,1)
			#meaty = bool(re.search('meat|fish|chicken|turkey|beef|salmon|bacon|sausage|steak|shrimp|prawns|pork|lamb|duck', words.text))
			#print(meaty)
			#if meaty == True:
			#	meat.append(html_file1)
			#else: continue
		

			
	
			

		print('Nutritional Information')
		for k, v in zip(nutri_key,nutri_amount):
			
			try:
				curR.execute('INSERT OR IGNORE INTO Rec_Nutrition_Keys (nutrition_key) VALUES (?)',(k.text.strip(),)) 
				connR.commit()
				curR.execute('SELECT nutrition_id FROM Rec_Nutrition_Keys WHERE nutrition_key=?',(k.text,))
				nutrition_id = curR.fetchone()
				#print(nutrition_id[0])
				curR.execute('INSERT OR IGNORE INTO Rec_Nutrition_Values (nutrition_id,nutrition_value,recipe_id) VALUES (?,?,?)',(nutrition_id[0],v.text.strip(),recipe_id[0]))
				connR.commit()
				
				#print(k.text, v.text)
			except:
				print(k.text, "- Error Nutritional Information")

		# #CREATE CATEGORY DIET ---- Figure way to take key words from recipe to categories
		#curR.execute('''CREATE TABLE IF NOT EXISTS Cat_Keys
   		#	(cat_key_id INTEGER PRIMARY KEY, category TEXT) ''')
		# #CREATE CATEGORY DIET ---- Figure way to take key words from recipe to categories
		#curR.execute('''CREATE TABLE IF NOT EXISTS Category_List
   		#	(category_id INTEGER PRIMARY KEY, cat_key_id, recipe_id INTEGER)''')

		print('Categories')
		#category_list = list()
		print('')
		for cat in category:
			#category_list.append(cat.text)
			print(cat.text)
			curR.execute('INSERT OR IGNORE INTO Cat_Keys (category) VALUES (?)',(cat.text,))
			connR.commit()
			curR.execute('SELECT cat_key_id FROM Cat_Keys WHERE category=?',(cat.text,))
			connR.commit()
			cat_id = curR.fetchone() 
			curR.execute('INSERT OR IGNORE INTO Category_List (cat_key_id,recipe_id) VALUES (?,?)',(cat_id[0],recipe_id[0]))
			connR.commit()
			#print(cat.text)
		
		x= x-1
		print('-RECIPE-ONE-RECIPE-DONE-RECIPE-DONE-RECIPE-DONE-RECIPE-DONE-RECIPE-DONE-')
		print('')

	webs2.remove(html_file1)



connL.close()
connR.close()

#print(webs2)
print("----------------------SCAN COMPLETE-------------------------")
print(delete_list)
#print(meat)

#These are just notes

##USEFUL STUFF
#INSERT INTO TABLE METHOD 1 -- Uses ? as placeholders then use values in parenthesis. 
# If only 1 value I believe you need a comma after first value reference still ex ((?)',(val1,))
## method1.excute(""" INSERT INTO table1 VALUES (?,?,?) """,(val1,val2,val3))

#Method 2 -- uses colon then name describes placeholder. Values listed as dictionary.
#method2.excute(""" INSERT INTO table2 VALUES (:val1,:val2,:val3) """,{'val1':'poppy','val2':'elle','val3':'muria'})

#Connect to test database running on memory to not have to keep deleting database
# conn = sqlite.connect(':memory:')

#what makes more sense - 
#Category List - compact can be retrieved all at once, how does it look to filter through it, MUST BE INDIVIDUAL cells 
