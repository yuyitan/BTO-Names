from selenium import webdriver
import bs4 as bs
from urllib.request import Request, urlopen
import requests
import lxml.html

bto_names = []
url = "https://www.teoalida.com/singapore/btolist/"

my_session = requests.session()
for_cookies = my_session.get("https://www.teoalida.com/")
cookies = for_cookies.cookies
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
response = my_session.get(url, headers=headers, cookies=cookies)

soup = bs.BeautifulSoup(response.content)

map = {}

table = soup.find('table')
for tr in table.find_all('tr')[1:]:
 bto_name = tr.find_all('td')[1].get_text()
 bto_names.append(bto_name)

for bto_name in bto_names:
    sep1 = '('
    sep2 = '@'
    sep3 = '['
    sep4 = '&'
    cleaned = bto_name.split(sep1, 1)[0].split(sep2, 1)[0].split(sep3, 1)[0].split(sep4, 1)[0].strip()
    split = cleaned.split(" ")

    last = split[-1]

    if last == "I" or last == "II" or last == "1" or last == "2":
        second_last = split[-2]
        
        if second_last != "":
            if map.get(second_last) == None:
                map[second_last] = 1
            else:
                map[second_last] = map.get(second_last) + 1

    else: 
        if last != "":
            if map.get(last) == None:
                map[last] = 1
            else:
                map[last] = map.get(last) + 1

count = len(map)

for w in sorted(map, key=map.get, reverse=True):
    percentage = round((map[w] / count * 100), 2)
    percentage_string = "(" + str(percentage) + "%)"
    print(w, map[w], percentage_string)