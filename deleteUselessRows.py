

from copy import copy
import sqlite3
from bs4 import BeautifulSoup
from numpy import integer
import requests
import random
import time



conn = sqlite3.connect('spider.sqlite')
curr = conn.cursor()
curr.execute('''CREATE TABLE IF NOT EXISTS Delete_list 
    (D_url_id INTEGER PRIMARY KEY, D_url TEXT UNIQUE)''')
curr.execute('''CREATE TABLE IF NOT EXISTS scanned_list 
    (url_id INTEGER PRIMARY KEY, url TEXT UNIQUE)''')


print('---------------------------------------------------------------------------')
webs = list()
curr.execute('SELECT COUNT(*) FROM scanned_list')
count = curr.fetchone()
print(count)


btime =time.time()

x = int(input("how many recipes "))
curr.execute('''SELECT Url FROM Pages WHERE Url NOT IN (SELECT url FROM scanned_list) LIMIT 150''')
for row in curr:
	webs.append(str(row[0]))

webs2 = copy(webs)
print(webs)


while (x > 0) :
	#file1 is created first to first select a random recipe that is then used to to get the html info using "requests"
	html_file1 = random.choice(webs2)
	html_file = requests.get(html_file1).text


	#print(html_file1)
	print('')
	#THIS WILL REMOVE the chosen file from the temporary list.  To avoid repeats long term you will need 
	# to add to a running list of recipes (Possibly another DB or maybe even adding a date coloumn on database
	# to filter out for recently made)
	

	soup = BeautifulSoup(html_file,'lxml',)
	title = soup.find('h2', class_="recipe-intro__title")
	
	#print(title.text)
	if title == None: 
		#Delete URLS that do not have titles - Deletes from spider.sqlite file
		print(html_file1)
		curr.execute("DELETE FROM Pages WHERE Url=?",(html_file1,))
		conn.commit()
		curr.execute('INSERT OR IGNORE INTO Delete_list (D_url) VALUES (?)',(html_file1,))
		conn.commit()

		print("No Title - Deleted from DB")
		print()
		webs2.remove(html_file1)
		
	else :
		print('OK - ',html_file1)
		curr.execute('INSERT OR IGNORE INTO scanned_list (url) VALUES (?)',(html_file1,))
		conn.commit()
		x=x-1
		

#curr.execute("SELECT id,url FROM Pages LIMIT 4")
#[print(row) for row in curr.fetchall()]
etime = time.time()
print(etime-btime)


print('done------------------------done')




