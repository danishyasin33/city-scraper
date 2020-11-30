# import libraries
import requests
from bs4 import BeautifulSoup


homeURL = 'https://geographic.org/streetview/germany/'
mainList = [
    'bavaria/munchen.html']
for item in mainList:
    cityURL = homeURL + str(item)
    cityPage = requests.get(cityURL)
    citySoup = BeautifulSoup(cityPage.content, 'html.parser')

    centerFont = citySoup.select('div.table > center strong')
    centerFont = centerFont[0].get_text()
    isStreets = 'List of streets in'
    if isStreets in centerFont:  # some pages have streets immediately
        streetList = citySoup.select('div.listmain li')
        for street in streetList:
            streetText = street.get_text()
            print(streetText)
    else:
        cityList = citySoup.select('div.listmain li a')
        for city in cityList:
            distURL = cityURL.rstrip('index.html') + city['href']
            distPage = requests.get(distURL)
            distSoup = BeautifulSoup(distPage.content, 'html.parser')

            centerFont = distSoup.select('div.table > center strong')
            centerFont = centerFont[0].get_text()
            isStreets = 'List of streets in'
            if isStreets in centerFont:  # some pages have streets immediately
                streetList = distSoup.select('div.listmain li')
                for street in streetList:
                    streetText = street.get_text()
                    print(streetText)
            else:   # some require another iteration
                localities = distSoup.select('div.listmain li a')
                for local in localities:
                    localURL = distURL.rstrip('index.html') + local['href']
                    localPage = requests.get(localURL)
                    localSoup = BeautifulSoup(localPage.content, 'html.parser')

                    streetList = localSoup.select('div.listmain li')
                    streetText = streetList[0].get_text()
