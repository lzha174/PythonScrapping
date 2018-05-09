from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import time


# if has Chinese, apply decode()

    



USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
 


def fetch_bookings(search_term):
    assert isinstance(search_term, str), 'Search term must be a string'
    escaped_search_term = search_term.replace(' ', '+')
    booking_url = "https://www.booking.com/searchresults.en-gb.html?aid=337631&sid=dea4a21834d9c9b6ace20b7df8c17fef&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D337631%3Bsid%3Ddea4a21834d9c9b6ace20b7df8c17fef%3Bsb_price_type%3Dtotal%26%3B&ss=Queenstown&ssne=Queenstown&ssne_untouched=Queenstown&dest_id=900039039&dest_type=city&checkin_monthday=25&checkin_month=5&checkin_year=2018&checkout_monthday=26&checkout_month=5&checkout_year=2018&group_adults=2&group_children=0&no_rooms=1&from_sf=1"
    response = requests.get(booking_url, headers=USER_AGENT)

    response.raise_for_status()
    return search_term, response.text

import re
def parse_results(html, keyword):
    soup = BeautifulSoup(html, "lxml")

    found_results = []
    rank = 1
    #result_block = soup.select("[name^=data-hotelid]")
    result_block = soup.select("[data-class^=4]")
    for result in result_block:
        rank = rank + 1
        if rank == 14:
            break
        #print(result)
        title = result.find('span', attrs={'class': 'sr-hotel__name'})
        price = result.find('strong', attrs={'class': 'price availprice no_rack_rate '})
        if title and price:
            title = title.get_text().lstrip().rstrip()
            price = price.get_text().replace("NZD","").lstrip().rstrip()
            found_results.append({'Title': title, 'Price': price})
    return found_results
 
def scrape_bookings(search_term):
    keyword, html = fetch_bookings(search_term)
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
    os.system('clear')  # on linux / os x
    keywords = ['Queenstown']
    data = []
    for keyword in keywords:
        try:
            results = scrape_bookings(keyword)
            for result in results:
                data.append(result)           
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
#    print(data)
    csv_columns = ['Title','Price']

    currentPath = os.getcwd()
    csv_file = currentPath + "/csv/BookingQueenstown.csv"

    WriteDictToCSV(csv_file,csv_columns,data)
