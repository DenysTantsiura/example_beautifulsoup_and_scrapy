from pprint import pprint

from bs4 import BeautifulSoup
import requests


url = 'https://quotes.toscrape.com/'

x = requests.get(url).text
print(f'text=> {type(x)}')
x = BeautifulSoup(x, 'lxml')
print(x)

print('&'*60)
x = requests.get(url).content
print(f'content=> {type(x)}')
x = BeautifulSoup(x, 'html.parser')
print(x)


