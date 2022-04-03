
import random

from numpy import append


recipeList =["recipe1","recipe2", "recipe3","recipe4","recipe5","recipe6",'carrot','carrots', 'onion','apples','garlic', 'tofu','lemongrass', 'broccoli']
ingred = ['carrot','carrots', 'onion','apples','garlic', 'tofu','lemongrass', 'broccoli']
instruct = 'These are the instructions to cook this savory deliciousness of a meal.'

#ingfilter = input("Are there any ingredients you dont want ")
rounds = input("Enter the Number of Recipes you want for the week  ")

weeklist = list()

i=0
#for x in recipeList:
while i <int(rounds):
	
	y = (random.choice(recipeList))
	#print(y)
	if y not in weeklist:
		print(y)
		weeklist.append(y)
		i+= 1
		
## HOW DO YOU MAKE SURE RECIPES ARE NOT REPEATED FOR ATLEAST EVERY THREE WEEKS?


