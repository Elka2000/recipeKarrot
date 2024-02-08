from copy import copy
from itertools import count
import sqlite3
from bs4 import BeautifulSoup
from numpy import integer
import requests
import random

#lass returnRecipe:
conn=sqlite3.connect('RecipeScrape3.sqlite')
curs = conn.cursor()

print('')
print('-------------------------------------------------')
def rec_return (z):
	#x = 3 #Make this be an input or represent x in loop of eligible recipes
	curs.execute('SELECT recipe_title, instructions FROM Recipes_Main WHERE recipe_id = ?',(z,))
	rmatch = curs.fetchall()
	instructions = ('')
	for x, y in rmatch:
		print (x)
		print('')
		instructions = instructions+y

	#RETURN TIME ELEMENTS
	curs.execute('''SELECT time_key, time_value FROM Rec_Time_Values JOIN Rec_Time_Keys 
		ON Rec_Time_Keys.time_id = Rec_Time_Values.time_id 
		WHERE Rec_Time_Values.recipe_id =?''',(z,))
	times = curs.fetchall()
	for x in times:
		print(x[0],x[1])
	print('')
	print(instructions)

	print('')
	#RETURN INGREDIENT ELEMENTS
	#NOTE Keeping Ing_Value as TEXT will prevent altering recipes,
	curs.execute('''SELECT ingredient_key, ingredient_value FROM Rec_Ingredients_Values JOIN Rec_Ingredients_Keys 
		ON Rec_Ingredients_Keys.ingredient_id = Rec_Ingredients_Values.ingredient_id 
		WHERE Rec_Ingredients_Values.recipe_id =?''',(z,))
	ingred = curs.fetchall()
	for x in ingred:
		print(x[1],x[0])
	print('')

lookup = int(input('type recipe ID here '))
print('')
rec_return(lookup)
