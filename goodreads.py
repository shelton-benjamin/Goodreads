import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

# for page in range(1, 51):
#     url = ('https://www.goodreads.com/search?page=' + str(page) 
#     + 'qid=lh83RqgFXk&query=data+science&tab=books')
#     req = requests(url)
#     soup = BeautifulSoup(req.content, 'html.parser')





# page = requests.get('https://www.goodreads.com/search?page=1&qid=lh83RqgFXk&query=data+science&tab=books&utf8=%E2%9C%93')
# soup = BeautifulSoup(page.content, 'html.parser')

book_title = []
author = []

published = []

n_ratings = []

avg_rating = []

editions = []

for page in range(1, 51):
     url = ('https://www.goodreads.com/search?page=' + str(page) 
     + 'qid=lh83RqgFXk&query=data+science&tab=books')
     req = requests.get(url)
     soup = BeautifulSoup(req.content, 'html.parser')
     table = soup.table
     book_list = table.find_all('tr')
     
     for book in book_list:
         
         title = book.find_all('a', class_ = 'bookTitle')
         book_title.append(title[0].text.strip())
         
         authors_for_book = []
         authors_names = book.find_all('a', class_ = 'authorName')
        
         for authors in authors_names:   
             authors_for_book.append(authors.text.strip())
         author.append(authors_for_book)
         
           #published year
         pattern = re.compile(r"published\s*(\d{4})")
         year_pub = pattern.search(book.text)
         published.append(year_pub.group(1) if year_pub else 0)

        #rating
         all_ratings = book.find_all('span', class_ = 'minirating')
         all_ratings_text = all_ratings[0].text.strip()
         pattern_2 = re.compile(r"(\d\.?\d*)\savg")
         avg_rating.append(pattern_2.search(all_ratings_text).group(1))

        #n_ratings
         pattern_4 = re.compile(r"(\d\,?\d*) rating")
         ratings_matches = pattern_4.search(all_ratings_text)
         n_ratings.append(ratings_matches.group(1) if ratings_matches else 0)  

        #editions
         pattern_3 = re.compile(r"(\d+) edition")
         eds = book.find(href=re.compile("editions"))
         editions.append(pattern_3.search(eds.text).group(1))
        
        
df = pd.DataFrame({
    'Title': book_title, 
    'Author(s)': author,
    'Published Year': published,
    'Editions': editions,
    'Avg. Rating': avg_rating,
    'Num. of Ratings': n_ratings})       
         
print(df.info())

df.to_csv('dataScience_book.csv', index=False)