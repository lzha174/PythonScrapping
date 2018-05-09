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

def WriteDictToCSV(csv_columns, dict_data, mode, str_file):
    try:
        currentPath = os.getcwd()
        csv_file = currentPath + "/mysite/polls/" + str_file;
        with open(csv_file, mode) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            if (mode == 'w'):
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
    keywords = ['Queenstown']
    hotels = []
    for keyword in keywords:
        try:
            results = ScrapeBookings.scrape_bookings(keyword)
            for result in results:
                hotels.append({'Title':result['Title'] + ' ' + keyword, 'Price': result['Price']})
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
    coords = []
    for location in interestedLocations:
        results = GoogleMap.geocode(address=location['Title'])
        if (results and results[0]):
            route = results[0]
            location = route['geometry']['location']
            lat, lng = location['lat'], location['lng']
            coords.append({'lat':lat, 'lng':lng});
    print(coords);
    for hotel in hotels:
        print(hotel)
        results = GoogleMap.geocode(address= hotel['Title'])
        route = results[0]
        location = route['geometry']['location']
        lat, lng = location['lat'], location['lng']
        source = "%s,%s" % (lat, lng)
        time.sleep(1)
        print('source is ', source)
        for location in interestedLocations:
            data = GoogleMap.directions(source, location['Title'], **params)

            while data['status'] == 'OVER_QUERY_LIMIT':
                print
                'Pausing for 1 minutes...'
                time.sleep(60)
                data = GoogleMap.directions(source, location['Title'], **params)
            if data['status'] != 'OK':
                print("wrong direction request")
                continue;
            if len(data['routes']) > 0:
                timings, dist = GoogleMap.output_routes('driving', data['routes'])
                #print('Timings:')
                #print(timings)
                #print('Distances:')
                #print(dist)
                totalTravelTime += timings['driving-DRIVING'];
        if (totalTravelTime < minTravelTime):
            minTravelTime = totalTravelTime;
            bestHotel = hotel['Title'];
        print('total travel time is ', totalTravelTime)
        totalTravelTime = 0;
    print('best hotel is ', bestHotel);

    csv_columns = ['Title','Price']

    str_file = 'Locations.csv'
    WriteDictToCSV(csv_columns,interestedLocations, 'w', str_file);

    str_file = 'Coords.csv'
    csv_columns = ['lat', 'lng']
    WriteDictToCSV(csv_columns, coords, 'w', str_file);

    str_file = 'Hotels.csv'
    csv_columns = ['Title', 'Price']
    WriteDictToCSV(csv_columns, hotels, 'w', str_file);

