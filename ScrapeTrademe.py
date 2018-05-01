from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import time


# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/list.html").read().decode('utf-8')
print(html)

soup = BeautifulSoup(html, features='lxml')
print(soup.h1)

all_href = soup.find_all('h3', {"class":"rc"})
for l in all_href:
    print('\n', l.get_text())
    



USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
 


def fetch_trademe(search_term):
    assert isinstance(search_term, str), 'Search term must be a string'
    escaped_search_term = search_term.replace(' ', '+')
    trademe_url = 'https://www.trademe.co.nz/Browse/SearchResults.aspx?&cid=0&searchType=&searchString={}&x=0&y=0&type=Search&sort_order=price_desc&redirectFromAll=False&rptpath=all&rsqid=1933ee045fd449f280cc0a1350056792&page=9&user_region=2&user_district=0&generalSearch_keypresses=14&generalSearch_suggested=0&generalSearch_suggestedCategory='.format(escaped_search_term)
    response = requests.get(trademe_url, headers=USER_AGENT)
    response.raise_for_status()
    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'info'})
    for result in result_block:

        title = result.find('div', attrs={'class': 'title'})
        price = result.find('div', attrs={'class': 'listingBidPrice'})
        if title and price:
            price = price.get_text()
            price = price[1:]
            price = price.replace(",","")
            found_results.append({'Title': title.get_text().lstrip().rstrip(), 'Price': price})
    return found_results
def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

def scrape_trademe(search_term):
    keyword, html = fetch_trademe(search_term)
    results = parse_results(html, keyword)
    return results

import csv
import os

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
            print("I/O error({0}): {1}".format(errno, strerror))    
    return            


    
if __name__ == '__main__':
    keywords = ['chair']
    data = []
    for keyword in keywords:
        try:
            results = scrape_trademe(keyword)
            for result in results:
                data.append(result)           
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    print(data)
    csv_columns = ['Title','Price']

    currentPath = os.getcwd()
    csv_file = currentPath + "/csv/Chairs.csv"

    WriteDictToCSV(csv_file,csv_columns,data)
