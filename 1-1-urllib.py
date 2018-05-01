from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import time
import ScrapeBookings
import GoogleMap


if __name__ == '__main__':
    keywords = ['Queenstown']
    data = []
    for keyword in keywords:
        try:
            results = ScrapeBookings.scrape_bookings(keyword)
            for result in results:
                data.append(result['Title'] + ' ' + keyword)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    eight_am = int(time.mktime(time.struct_time([2014, 7, 14, 8, 0, 0, 0, 0, 0])))
    for name in data:

        results = GoogleMap.geocode(address= name)
        data = results[0]
        location = data['geometry']['location']
        lat, lng = location['lat'], location['lng']
        source = "%s,%s" % (lat, lng)
        params = {
            'mode': 'driving',
            'region': 'sg',
            'alternatives': 'false',
            'departure_time': eight_am,
        }

        data = GoogleMap.directions(source, 'Wanaka', **params)
        if len(data['routes']) > 0:
            timings, dist = GoogleMap.output_routes('driving', data['routes'])
            print('Timings:')
            print(timings)
            print('Distances:')
            print(dist)

        time.sleep(2)


