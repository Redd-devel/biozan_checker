import requests
from bs4 import BeautifulSoup
import re
import os

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"}
root_url = "https://biozan.ru"
data = {"_csrf": os.environ.get("CSRF"), "login": os.environ.get("USERLOGIN"), "password": os.environ.get("USERPASS"), "wa_auth_login":"1"}

session = requests.Session()
session.post(root_url+"/login/", headers=headers, data=data, allow_redirects=True)

products = session.get(root_url+"/products/linear/", headers=headers)
gift = session.get(root_url+"/my/account/#gift", headers=headers)

session.close()


soup_products = BeautifulSoup(products.text, "lxml")
data = soup_products.find_all("div", class_="product-wrap")

for item in data:
	name = item.find("div", class_="product-thumbs-name").text.trim()
	price = item.find("div", class_="product-thumbs-price").text
	if name.startswith("Пакет"):
		continue
	print(name, price)
print('-'*30)

soup_gift = BeautifulSoup(gift.text, "lxml")
scraped_score = soup_gift.find("ul", class_="dashboard-tabs").find("li").next_sibling.next_sibling.next_sibling.next_sibling.find("b").text
score = re.search(r'\d+\s?\d*', scraped_score)[0].rstrip()
print("Подарочные баллы: " + score.replace(" ", ""))