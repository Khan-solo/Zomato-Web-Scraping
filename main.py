'''
Author: Mursil Khan
Project: Voosh DS Internship Assessment
Tasks: Extract, Analyse, Visualise
Date: 3rd July, 2021
Restaurant: Molecule Air Bar
Status: Live
Location: Lucknow'''

#importing the Libaries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter

# Creating custom header with information from httpbin.org/headers using Chrome browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
           "Accept-Language" : "en-GB,en-US;q=0.9,en-IN;q=0.8,en;q=0.7,hi-IN;q=0.6,hi;q=0.5",
           "Dnt": "1"}

#seding the get request to receive all the data from the webpage
url='https://www.zomato.com/lucknow/molecule-air-bar-gomti-nagar/order' #url for the order page of Molecule Air Bar
html_text = requests.get(url, headers = headers).text
soup = BeautifulSoup(html_text, "lxml") #lxml parser used

# On analysing a general webpage of zomato, Molecule Air Bar, for instance.
# We can find out the "card" containing the relevant data for the task, i.e:
# Name of the Restuarant
# Name of the dish
# Price of the dish
# Must try Tag
# Description of the dish

# The name of the restaurant is an h1 tag of class "sc-7kepeu-0 sc-cpmLhU iywipP"
restaurant_class="sc-7kepeu-0 sc-cpmLhU iywipP"
restaurant_name = soup.find("h1", class_="sc-7kepeu-0 sc-cpmLhU iywipP").text
# Name of the dish is a tag h4 of class "sc-1s0saks-15 iSmBPS"
name_class = "sc-1s0saks-15 iSmBPS"
# Price of the dish is a span tag of class "sc-17hyc2s-1 cCiQWA"
price_class = "sc-17hyc2s-1 cCiQWA"
# Description of the dish is a paragraph of class "sc-1s0saks-12 hcROsL"
desc_class = "sc-1s0saks-12 hcROsL"
# Must Try tag is a div tag of class "sc-2gamf4-0 cRxPpO"
tag_class = "sc-2gamf4-0 cRxPpO"
# finding out dishes
dishes = soup.find_all('div', class_ = "sc-1s0saks-17 bGrnCu") #list of div tags containing dishes

# creating an empty list for dishes
dish_name=[]

#creating an empty list for price
dish_price=[]

#Creating an empty list for description
dish_description= []

# Creating an empty list for tag
dish_tag = []
#variables to keep a count of must try options
must_try_count = 0
# Populating the lists with relevant data
for dish in dishes:
    #adding name of the dish to the list
    dish_name.append(dish.find('h4', class_ = name_class).text)
    #adding price of the dish to the list as integer
    price = dish.find('span', class_ = price_class).text
    dish_price.append(int(price[1:]))
    #adding description of the dish to the list
    dish_description.append(dish.find('p', class_ = desc_class).text)
    #finding if Must Try Tag is there for the dish
    tag = dish.find('div', class_ = tag_class)
    if tag is None:
        dish_tag.append("Tag Not Found")
    else:
        dish_tag.append(dish.find('div', class_ = tag_class).text)
        must_try_count+=1
        #end of loop

'''
Text Analysis:
_____________
Goal: To Find out the frequency of each word used in item description of all items
Patterns in Dish Names: 
    * Size/Quantity of item (if any) mentioned in Square Brackets
    * Values in square brackets follow a pattern: Numeric value + Unit
    * Example: [12 Inches], [5 Pieces]
    * Every word starts with an uppercase character
Patterns in Dish Description:
    * Some descriptions are incomplete, end in "... read more"
    * Can be scraped with advanced scraping techniques
    * Combinations are often used with "+" sign
    * Quantity (if any) mentioned in square brackets    
'''
# Data Preprocessing:
incomplete=0
# Getting rid of all special characters:
for i in range(len(dish_description)):
    if ("+" in dish_description[i]):
        dish_description[i] = dish_description[i].replace("+", " ")
    if ("/" in dish_description[i]):
        dish_description[i] = dish_description[i].replace("/", "")
    if ("[" in dish_description[i]):
        dish_description[i] = dish_description[i].replace("[", "")
    if ("]" in dish_description[i]):
        dish_description[i] = dish_description[i].replace("]", "")
    if ("." in dish_description[i]):
        dish_description[i] = dish_description[i].replace(".", "")
    if ("," in dish_description[i]):
        dish_description[i] = dish_description[i].replace(",", "")
    if ("read more" in dish_description[i]):
        dish_description[i] = dish_description[i].replace("read more", "")
        incomplete+=1

# Getting a list of all the words
# and adding to a single string
word = ""
for description in dish_description:
    word+=" "
    word+= description

#converting every word to lowercase:
word_list = word.lower()

#creating a list of words:
frequency_list = word_list.split()

#Creating a dictionary to store the frequency of each element
dictionary = {}

#function to count the elements:
def count(elements):
    if elements in dictionary:
        dictionary[elements]+=1
    else:
        dictionary.update({elements: 1})
for elements in frequency_list:
    count(elements)

# Writing this data to an excel file using pandas
# Prefferred XlsxWriter for the task (for more flexibility
#df = pd.DataFrame(data=dictionary, index=[0])
#print (df)
#df.to_excel('Molecule Air Bar.xlsx')

#Writing the data to an excel file using XlsxWriter
workbook = xlsxwriter.Workbook(restaurant_name +" Words.xlsx")
worksheet = workbook.add_worksheet("Word Frequency")

worksheet.write("A1", "Word")
worksheet.write("B1", "Frequency")
#row 1 already written for headers
#indexing starts at row 2
row_index=2
for key, value in dictionary.items():
    # concatenating the values to get cell address
    a = ("A" + str(row_index))
    b = ("B" + str(row_index))
    worksheet.write(a, key)
    worksheet.write(b, value)
    row_index+=1
workbook.close()

'''
A workbook named "Molecule Air Bar" is created
First column contains the rows of unique words
Second column contains the row of the frequency of word in column 1
'''

# A visualisation of the words and its frequency can be viewed in
# Tableu Public using the following link
# https://public.tableau.com/views/ZomatoRestauranDishDescriptionsWordFrequency/Sheet1?:language=en-GB&:display_count=n&:origin=viz_share_link
