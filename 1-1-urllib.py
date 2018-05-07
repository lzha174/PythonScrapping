from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import csv
import os
import time
import collections
from  mysite.polls import ScrapeBookings
from  mysite.polls import GoogleMap
from  mysite.polls import ScrapePlanet

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
            print("I/O erroor")
    return


def load_csv():
    mylocations = [];
    with open('mysite/polls/csv/Locations.csv') as f:
        next(f)
        for line in csv.DictReader(f, fieldnames=('Title', 'Price')):
            print(line['Title'], line['Price'])
            mylocations.append({'Title': line['Title']})
    print(mylocations)


if __name__ == '__main__':
    load_csv();
    keywords = ['Queenstown']
    hotels = []
    for keyword in keywords:
        try:
            results = ScrapeBookings.scrape_bookings(keyword)
            for result in results:
                hotels.append(result['Title'] + ' ' + keyword)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)

    eight_am = int(time.mktime(time.struct_time([2018, 7, 14, 8, 0, 0, 0, 0, 0])))
    params = {
        'mode': 'driving',
        'region': 'sg',
        'alternatives': 'false',
        'departure_time': eight_am,
    }

    totalTravelTime = 0;
    minTravelTime = 100000000;
    bestHotel = '';
    interestedLocations = ScrapePlanet.get_intrested_locations();
    for name in hotels:
        print(name)
        results = GoogleMap.geocode(address= name)
        route = results[0]
        location = route['geometry']['location']
        lat, lng = location['lat'], location['lng']
        source = "%s,%s" % (lat, lng)
        time.sleep(1)

        for location in interestedLocations:
            data = GoogleMap.directions(source, location['Title'], **params)
            if len(data['routes']) > 0:
                timings, dist = GoogleMap.output_routes('driving', data['routes'])
                #print('Timings:')
                #print(timings)
                #print('Distances:')
                #print(dist)
                totalTravelTime += timings['driving-DRIVING'];
        if (totalTravelTime < minTravelTime):
            minTravelTime = totalTravelTime;
            bestHotel = name;
        print('total travel time is ', totalTravelTime)
        totalTravelTime = 0;
    print('best hotel is ', bestHotel);

    csv_columns = ['Title','Price']

    currentPath = os.getcwd()
    csv_file = currentPath + "/mysite/polls/csv/Locations.csv"

    WriteDictToCSV(csv_file,csv_columns,interestedLocations);




