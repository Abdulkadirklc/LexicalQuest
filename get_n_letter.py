import requests
from bs4 import BeautifulSoup


def take_word_list(number_of_letter):
    url = f"https://wordfind.com/length/{number_of_letter}-letter-words/#results"  # write which link which will we visit
    response = requests.get(url)  # sends a get request to url
    soup = BeautifulSoup(response.content, "html.parser")  # parses the html content of the website

    word_list = []
    for li in soup.find_all("li", class_="dl"):  # find li that has a class value 'dl' in the source of the page
        word = li.a.text  # take all words between a tag.
        word_list.append(word)  # add it into word_list

    word_list.sort()  # order alphabetically

    with open(f"ordered_{number_of_letter}_lettered.txt", "w") as f:  # open a txt file
        for word in word_list:
            f.write(word + "\n")  # write all words into txt file
    pass


take_word_list(5)

# after lots of try I've finally made it... The problem was about the link that I tried to get so I've found a new website

"""from bs4 import BeautifulSoup
import requests

url = "https://www.wordgamedictionary.com/scrabble-word-finder/" # example.com yerine istediğiniz web sitesini kullanabilirsiniz
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

td = soup.find("table").find_all("tr")[2].find_all("td")[1]
print(td.text)"""

"""
import requests
from bs4 import BeautifulSoup

url = "https://www.wordgamedictionary.com/scrabble-word-finder/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
seven_letter_words = soup.select("table#search_results_table_0 tbody tr td:nth-child(2) a")

with open("words.txt", "w") as f:
    for word in seven_letter_words:
        if len(word.text) == 7:
            f.write(word.text + "\n")

"""

"""
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

url = "https://www.wordgamedictionary.com/scrabble-word-finder/"
driver.get(url)
print(driver.page_source) # sayfa kaynağını yazdır

a_elements = driver.find_elements(By.XPATH, '//*[@id="wrap"]/div[2]/section/div/div/div[7]/table/tbody//a')

for a_element in a_elements:
    print(a_element.text)

driver.quit()
"""

"""
url = 'https://www.wordgamedictionary.com/scrabble-word-finder/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

a_tags = soup.select('html > body > article > div > div:nth-of-type(1) > section > div > div > div:nth-of-type(3) > table > tbody > tr > td:nth-of-type(2) > a')
for a_tag in a_tags:
    print(a_tag.text)"""
"""
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

div = soup.find('div', {'class': 'cd-md-12'})
table = div.find('table')
tbody = table.find('tbody')

for a in tbody.find_all('a'):
    href = a.get('href')
    text = a.text
    print(href, text)
"""

"""
url = 'https://www.wordgamedictionary.com/scrabble-word-finder/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')

table = soup.select_one('#wrap > div:nth-child(1) > section > div > div > div:nth-child(3) > table > tbody')

words = []
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if cols:
        word = cols[1].find('a').text
        words.append(word)

print(words)
"""
