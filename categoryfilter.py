from copy import copy
from itertools import count
import sqlite3
from bs4 import BeautifulSoup
from numpy import integer
import requests
import random
import re
#from returnRecipe import rec_return() 

conn=sqlite3.connect('RecipeScrape3.sqlite')
curs = conn.cursor()

print('')
print('-------------------------------------------------')

#Prints out the categories
curs.execute('SELECT category FROM Cat_Keys ')
categories = curs.fetchall()
index = 0
for x in categories:
	print(x[0],index)
	index = index+1
filt = int(input(" ---- Select Input ----"))
curs.execute('SELECT ingredienrecipe_id, recipe_title FROM Recipes_Main WHERE recipe_id IN (SELECT recipe_id FROM Category_List WHERE cat_key_id =?) LIMIT 500',(filt,))
match = curs.fetchall()
print(len(match))
print('')
print(match)


#GOAL - Filter by Category or Ingredient

#Can you get a compact list of ingredients? 
#Pull 400 recipes combine recipe_id and instructions, search through instructions
		#EXERCISE - How long would it take to search through this? 