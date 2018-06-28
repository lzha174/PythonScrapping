from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import time

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_planet(search_term):
    assert isinstance(search_term, str), 'Search term must be a string'
    escaped_search_term = search_term.replace(' ', '+')
    planet_url = search_term;
    response = requests.get(planet_url, headers=USER_AGENT)
    response.raise_for_status()
    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    results_block = soup.find_all('div', attrs={'class': 'listing_details'})
    results = [];
    for result in results_block:
        title = result.find('div', attrs={'class':'listing_title'});
        price = result.find('div', attrs={'class':'price_test'});
        if (title and price):
            title = title.get_text()
            if  'Te Anau' in title or 'Glenorchy' in title or 'Auckland' in title:
                continue;
            index = price.get_text().find("$");
            price = price.get_text()[index+1:];
            price = price.replace('*','');
            #print(title.get_text(), price);
            results.append({'Title': title, 'Price': price})


    return results

def scrape_planet(search_term):
    keyword, html = fetch_planet(search_term)
    results = parse_results(html, keyword)
    return results;

def get_intrested_locations():
    urls = ['https://www.tripadvisor.co.nz/Attraction_Products-g255122-zfg12022-Queenstown_Otago_Region_South_Island.html']
    data = []
    for url in urls:
        try:
            results = scrape_planet(url)
            for result in results:
                data.append(result)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    print(data)
    return data;

if __name__ == '__main__':

    data = get_intrested_locations();

