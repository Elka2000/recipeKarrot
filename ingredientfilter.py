from copy import copy
from curses import nl
from distutils.log import error
import sqlite3
from bs4 import BeautifulSoup
from numpy import integer
import requests
import random
import re

conn=sqlite3.connect('RecipeScrape3.sqlite')
curs = conn.cursor()
#ingfilter = input('Input Filter ingredients ')

#pattern = r'ingfilter'
curs.execute('SELECT recipe_id, instructions FROM Recipes_Main ORDER BY RANDOM() LIMIT 500')
instruct = curs.fetchall()
print('--------------------------------------')
print('')
pattern = r'all'
regex = re.compile(pattern, flags=re.IGNORECASE)
count = 0
rec_list = []
for key, value in instruct:
	#print(value)
	try: 
		x = re.findall('ginger',value)
		if len(x)>0:
			print(value)
			count = count + 1
			rec_list.append(key)
		else:
			continue
	except:
		#print("Error On",key)
		#continue
		error


	
	print('-----------------------------------------------------------')
print(count,)

print(rec_list)



# inst_dict = {'name':'joe', 'age':32,'instructions':'The sky is blue so love and appreciate it.'}
# for key,value in inst_dict.items():
# 	print(value)
# ##Retrieve RecipeID and Instructions to create dictionary using Numpy
# ##Loop through

# import re
# def logs():
#     with open("romeo.txt", "r") as file:
#         logdata = file.read()
#     logss=list()
#     ddd = re.finditer(r'(?P<host>\d{3}\.\d{3}\.\d{3}\.\d{3}),(?P<user_name>(?=-\s)-*[\w]+),(?P<time>\d{2}/Jun/\d{4}:\d{2}:\d{2}:\d{2}\s-\d{4}),(?P<request>(?=")[A-Z]{3,}\s[\w.\s/]+(?="))',logdata)
#     for x in ddd:
#         new = ddd.groupdict()
#         logss.append(new)
#     return logss
#     raise NotImplementedError()
# print(len(logs()))