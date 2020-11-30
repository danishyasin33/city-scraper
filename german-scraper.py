# import libraries
import requests
from bs4 import BeautifulSoup


def main():
    homeURL = 'https://geographic.org/streetview/germany/'
    homePage = requests.get(homeURL)
    homeSoup = BeautifulSoup(homePage.content, 'html.parser')
    mainList = homeSoup.select("div.listmain li a")
    file = open('streets.txt', 'a')
    for item in mainList:
        cityURL = homeURL + str(item['href'])
        cityPage = requests.get(cityURL)
        citySoup = BeautifulSoup(cityPage.content, 'html.parser')
        print(cityURL)
        centerFont = citySoup.select('div.table > center strong')
        if centerFont:
            centerFont = centerFont[0].get_text()
        else:
            print('Result Page Not Found')
            continue
        isStreets = 'List of streets in'
        if isStreets in centerFont:  # some pages have streets immediately
            streetList = citySoup.select('div.listmain li')
            if streetList:
                print("Street List Found at: " + cityURL)
                for street in streetList:
                    streetText = street.get_text()
                    file.write(streetText + '\n')
            else:
                print('Street List not Found at: ' + cityURL)
                continue
        else:
            cityList = citySoup.select('div.listmain li a')
            if cityList:
                for city in cityList:
                    distURL = cityURL.rstrip('index.html') + city['href']
                    distPage = requests.get(distURL)
                    distSoup = BeautifulSoup(distPage.content, 'html.parser')

                    centerFont = distSoup.select('div.table > center strong')
                    if not centerFont:
                        print('Result Page Not Found')
                        continue
                    centerFont = centerFont[0].get_text()

                    isStreets = 'List of streets in'
                    if isStreets in centerFont:  # some pages have streets immediately

                        streetList = distSoup.select('div.listmain li')
                        if streetList:
                            print("Street List Found at: " + distURL)
                            for street in streetList:
                                streetText = street.get_text()
                                file.write(streetText + '\n')
                        else:
                            print('Street List not Found at: ' + cityURL)
                            continue
                    else:   # some require another iteration
                        localities = distSoup.select('div.listmain li a')
                        for local in localities:
                            localURL = distURL.rstrip(
                                'index.html') + local['href']
                            localPage = requests.get(localURL)
                            localSoup = BeautifulSoup(
                                localPage.content, 'html.parser')

                            streetList = localSoup.select('div.listmain li')
                            if streetList:
                                print("Street List Found at: " + localURL)
                                for street in streetList:
                                    streetText = street.get_text()
                                    file.write(streetText + '\n')
                            else:
                                print('Street List not Found at: ' + cityURL)
                                continue
            else:
                print('City list not found at: ' + cityURL)
                continue
    file.close()


if __name__ == "__main__":
    main()
